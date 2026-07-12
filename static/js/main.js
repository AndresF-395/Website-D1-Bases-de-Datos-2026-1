document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Ocultar automáticamente los mensajes Flash de Flask después de 5 segundos
    const alertList = document.querySelectorAll('.alert-dismissible');
    alertList.forEach(function(alert) {
        setTimeout(function() {
            // Usando la API de Bootstrap 5 para cerrar alertas
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5000 milisegundos = 5 segundos
    });

    // 2. Inicializar todos los Tooltips de Bootstrap (si se usan)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // 3. Confirmación global para botones de eliminación
    const deleteForms = document.querySelectorAll('form.form-delete');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const confirmMessage = form.getAttribute('data-confirm') || '¿Está seguro de que desea eliminar este registro? Esta acción no se puede deshacer.';
            if (!confirm(confirmMessage)) {
                e.preventDefault(); // Detiene el envío del formulario si el usuario cancela
            }
        });
    });
});