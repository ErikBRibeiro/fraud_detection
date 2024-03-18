document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    form.onsubmit = function(event) {
        const isConfirmed = confirm("Você tem certeza que deseja verificar a fraude?");
        if (!isConfirmed) {
            event.preventDefault(); // Impede o envio do formulário
        }
    };
});


document.addEventListener("DOMContentLoaded", function() {
    // Exemplo de código JavaScript para executar após o carregamento da página
    console.log("O documento foi carregado completamente.");
});
