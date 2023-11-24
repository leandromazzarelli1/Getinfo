$(document).ready(function () {
    
    $('.calificar-btn').click(function () {
        $('#calificarModal').modal('show');
    });

    $('#calificarForm').submit(function (event) {
        event.preventDefault();
        const formData = $(this).serializeArray();
        const csrfToken = $('input[name="csrf_token"]').val();
        
    
        
        $.ajax({
            type: 'POST',
            url: '/calificar',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify(formData),  
            success: function (response) {
                $('#calificarModal').modal('hide');
            },
            error: function (error) {
                console.error('Error al calificar la respuesta', error);
            }
        });
    });
    
});
