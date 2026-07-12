import math

def paginate_query(base_query, page, per_page, count_query, search_params=None):
    """
    Calcula el OFFSET, ejecuta la consulta paginada y devuelve los metadatos necesarios 
    para el macro render_pagination en Jinja2.
    """
    from utils.db import execute_query
    
    # 1. Calcular total de registros
    total_records_result = execute_query(count_query, search_params)
    total_records = total_records_result[0]['total'] if total_records_result else 0
    
    # 2. Calcular total de páginas
    total_pages = math.ceil(total_records / per_page)
    if total_pages == 0:
        total_pages = 1
        
    # Asegurar que la página actual esté en un rango válido
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    # 3. Calcular el OFFSET para SQL
    offset = (page - 1) * per_page
    
    # 4. Construir consulta final
    paginated_query = f"{base_query} LIMIT {per_page} OFFSET {offset}"
    
    # 5. Ejecutar la consulta con los datos
    items = execute_query(paginated_query, search_params)
    
    return items, total_pages, page