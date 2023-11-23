const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


$(document).ready(function () {
    $('#mostrarUsuariosBtn').on('click', function (event) {
        event.preventDefault();
        cargarUsuarios();
    });

    $('.btn-responder').click(function () {
        $('#responderModal').modal('show');
    });
    // respuestas 

    $('#responderForm').submit(function (event) {
        event.preventDefault();
        var respuesta = $('#respuestaTextarea').val();
        var csrfToken = $('#csrf_token').val();

        // Envía los datos al endpoint 'respuesta' mediante una petición AJAX
        $.ajax({
            type: 'POST',
            url: '/respuesta', // Asegúrate de que la URL sea correcta
            headers:{
                'X-CSRFToken': csrfToken
            },
            data: { 
                respuesta: respuesta
            },
            success: function (response) {
                // Maneja la respuesta del servidor si es necesario
                console.log('Respuesta enviada con éxito');
                $('#responderModal').modal('hide'); // Oculta el modal después de enviar la respuesta
            },
            error: function (error) {
                console.error('Error al enviar la respuesta', error);
            }
        });
    });

});


function cargarUsuarios() {
    fetch('/obtener_soporte')
        .then(response => response.json())
        .then(data => {
            const listaUsuarios = document.getElementById('listaUsuarios');
            listaUsuarios.innerHTML = '';

            data.forEach(usuario => {
                const tr = document.createElement('tr');

                const tdIdusuario = document.createElement('td');
                tdIdusuario.textContent = usuario[0];

                const tdNombredeusuario = document.createElement('td');
                tdNombredeusuario.textContent = usuario[2];

                const tdNombrecompleto = document.createElement('td');
                tdNombrecompleto.textContent = usuario[1];

                const tdEsAdmin = document.createElement('td');
                tdEsAdmin.textContent = usuario[3] === 1 ? 'Sí' : 'No';

                const tdBoton_modificar = document.createElement('td');
                const btn_m = document.createElement('button');
                btn_m.textContent = 'Cambiar contraseña';
                btn_m.classList.add('btn', 'btn-primary');
                btn_m.addEventListener('click', function (e) {
                    const fila = e.target.closest('tr');
                    const tdUsuarioId = fila.querySelector('td:first-child');
                    const usuarioId = tdUsuarioId.textContent;

                    $('#modalCambiarContrasena').modal('show');

                    // Enviar los datos actualizados al hacer clic en "Guardar Cambios"
                    $('#formCambiarContrasena').on('submit', function (event) {
                        event.preventDefault();

                        const nuevaContrasena = $('#nuevaContrasena').val();
                        const csrfToken = $('input[name=csrf_token]').val();

                        // Enviar la nueva contraseña al servidor
                        fetch(`/contrasena_soporte/${usuarioId}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken
                            },
                            body: JSON.stringify({ nuevaContrasena: nuevaContrasena })
                        })

                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log('Response data:', data); // Verificar si se obtiene la respuesta del servidor
                                $('#modalCambiarContrasena').modal('hide');
                                $('#modalConfirmacion').modal('show');
                                cargarUsuarios()

                            })
                            .catch(error => {
                                console.error('Error during fetch:', error);
                                // Aquí se puede agregar un mensaje de error específico o cualquier acción de manejo de errores necesaria
                            });

                    });


                });

                tdBoton_modificar.appendChild(btn_m);

                const tdBoton_eliminar = document.createElement('td');
                const btn_e = document.createElement('button');
                btn_e.textContent = 'eliminar';
                btn_e.classList.add('btn', 'btn-danger');
                btn_e.addEventListener('click', function (e) {
                    const fila = e.target.closest('tr');
                    const tdUsuarioId = fila.querySelector('td:first-child');
                    const usuario_id = tdUsuarioId.textContent;

                    $('#modalConfirmarEliminar').modal('show');

                    // Agregar evento al botón 'Eliminar' dentro del modal de confirmación
                    document.getElementById('confirmarEliminarBtn').addEventListener('click', function () {
                        // Ocultar el modal de confirmación
                        $('#modalConfirmarEliminar').modal('hide');

                        // Enviar el pedido al servidor para eliminar el usuario
                        fetch(`/eliminar_soporte/${usuario_id}`, {
                            method: 'DELETE', // Método HTTP DELETE,
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken
                            },
                        })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Error al eliminar el usuario');
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log(data.message); // Mensaje de confirmación del servidor
                                cargarUsuarios()

                            })
                            .catch(error => {
                                console.error('Error:', error);
                            });
                    });

                });

                tdBoton_eliminar.appendChild(btn_e);
                tr.appendChild(tdIdusuario);

                tr.appendChild(tdNombredeusuario);
                tr.appendChild(tdNombrecompleto);
                tr.appendChild(tdEsAdmin);
                tr.appendChild(tdBoton_modificar);
                tr.appendChild(tdBoton_eliminar);

                listaUsuarios.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Error al cargar usuarios:', error);
        });
}

document.getElementById('confirmarEliminarBtn').addEventListener('click', function () {
    $('#modalConfirmarEliminar').modal('hide');

    // Enviar el pedido al servidor para eliminar el usuario
    fetch(`/eliminar_soporte/${usuario_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al eliminar el usuario');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message); // Mensaje de confirmación del servidor

            // Volver a cargar los usuarios después de eliminar uno
            cargarUsuarios();
        })
        .catch(error => {
            console.error('Error:', error);
        });
});






