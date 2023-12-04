const nombre = document.getElementById("nombre")
const email = document.getElementById("email")
const mensaje = document.getElementById("mensaje")
const formulario = document.getElementById("formulario")
const regexEmail = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,4})+$/

formulario.onsubmit = evento => {
    evento.preventDefault(); // Detenemos el comportamiento predeterminado
    const valor_nombre = nombre.value
    const valor_mensaje = mensaje.value
    // Validacion que campo "nombre" no este vacio
    if (valor_nombre === ""){
        alert("Debe ingresar su nombre y apellido");
        return;
    }
    // Validacion de email
    if (!regexEmail.test(email.value)){
        alert("Debe ingresar un correo electrónico válido");
        return;
    }
    // Validacion que campo "nombre" no este vacio
    if (valor_mensaje === ""){
        alert("Por favor, ingrese un mensaje");
        return;
    }
    // El formulario se envia si logra llegar el codigo a esta parte. Si se cumple alguna condicion anterior, la funcion termina por el "return"
    formulario.submit();
};

//Consumo de API para las direcciones y telefonos de la seccion turnos
fetch('https://jsonplaceholder.typicode.com/users')
  .then(response => response.json())
  .then(data => {
    const elemento = document.getElementById("container-turnos");
    for (let i = 0; i < 3; i++) {
        elemento.innerHTML += `
            <p>Direccion: ${data[i].address.suite}</p>
            <p>Telefono: ${data[i].phone}</p><hr>
        `;
    }
  }).catch(error => console.log("Error", error));
