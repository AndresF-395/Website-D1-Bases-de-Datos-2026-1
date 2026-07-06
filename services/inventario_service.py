class InventarioService:
    @staticmethod
    def calcular_estado_stock(cantidad_disponible, demanda_diaria):
        # Como demanda_diaria no existe en BD, se inyecta desde la vista/controlador
        if demanda_diaria <= 0: return 'SEGURO'
        
        dias_stock = cantidad_disponible / demanda_diaria
        if dias_stock == 0:
            return 'AGOTADO'
        elif dias_stock < 5:
            return 'CRÍTICO'
        elif 5 <= dias_stock <= 15:
            return 'ALERTA'
        else:
            return 'SEGURO'