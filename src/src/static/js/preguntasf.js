const preguntas = document.querySelectorAll('.preguntas .contenedor-pregunta');
preguntas.forEach((pregunta)=>{
    pregunta.addEventListener('click', (e)=>{
        e.currentTarget.classList.toggle('activa');
        const respuesta = pregunta.querySelector('.respuesta');
        const alturarealder = respuesta.scrollHeight;
        console.log(alturarealder)
        if(!respuesta.style.maxHeight){
			respuesta.style.maxHeight = alturarealder + 'px';
		} else {
			respuesta.style.maxHeight = null;
		}
		preguntas.forEach((elemento) => {
			if(pregunta !== elemento){
				elemento.classList.remove('activa');
				elemento.querySelector('.respuesta').style.maxHeight = null;
			}
		});
    });
});

function checkEmptyText() {
    const texto = document.getElementById("mensaje").value.trim();

    if (texto === '') {
		
        document.getElementById('emptyTextAlert').style.display = 'block';
    } else {
       
        $('#confirmModal').modal('show');
        document.getElementById('emptyTextAlert').style.display = 'none';
    }
}



document.getElementById('confirmSubmit').addEventListener('click', function() {
    // Envía el formulario después de hacer clic en "Enviar" en la ventana modal
    document.getElementById('myForm').submit();
});


