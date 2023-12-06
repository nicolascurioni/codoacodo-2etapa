(function () {
  'use strict';

  window.addEventListener('load', function () {
    var forms = document.getElementsByClassName('needs-validation');

    Array.prototype.filter.call(forms, function (form) {
      form.addEventListener('submit', function (event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        } else {
          // Recopilar los valores de los campos del formulario
          var nombre = document.getElementById('firstName').value;
          var apellido = document.getElementById('lastName').value;
          var email = document.getElementById('email').value;
          var telefono = document.getElementById('telephone').value;
          var direccion = document.getElementById('address').value;
          var ciudad = document.getElementById('ciudad').value;
          var provincia = document.getElementById('provincia').value;
          var cp = document.getElementById('cp').value;
          var destino = document.getElementById('destino').value;
          var fecha = document.getElementById('datepicker').value;

          // Enviar correo utilizando EmailJS
      
          emailjs.send("service_qz19lhm", "template_5zrvtvk", {
            nombre: nombre,
            apellido: apellido,
            email: email,
            telefono: telefono,
            direccion: direccion,
            ciudad: ciudad,
            provincia: provincia,
            cp: cp,
            destino: destino,
            fecha: fecha
          })
          .then(function(response) {
            console.log("Correo enviado con éxito", response);
            alert("¡Correo enviado con éxito!");
            form.reset();
            form.classList.remove('was-validated');
          })
          .catch(function(error) {
            console.log("Error al enviar el correo", error);
            alert("Ocurrió un error al enviar el correo. Por favor, inténtalo de nuevo más tarde.");
          });
        }

        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();


