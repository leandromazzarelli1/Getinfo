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