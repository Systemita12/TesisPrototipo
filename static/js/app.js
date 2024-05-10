document.addEventListener("DOMContentLoaded", function () {
    const videoElement = document.getElementById('video');
    const resultElement = document.getElementById('result');
    const modelPath = 'Model/modelo_completo.json';
    const captureInterval = 1500; // Intervalo de captura en milisegundos (1.5 segundos)

    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(function (stream) {
            videoElement.srcObject = stream;
        })
        .catch(function (error) {
            console.error('Error al acceder a la cámara: ', error);
        });

    function updatePrediction(predictionText) {
        const predictionElement = document.getElementById('prediction');
        predictionElement.textContent = predictionText;
    }

    // Función para capturar y enviar la imagen al servidor
    function captureAndSendImage() {
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        // Convertir la imagen del canvas en un Blob para enviarla al servidor
        canvas.toBlob(async function (blob) {
            const formData = new FormData();
            formData.append('imagen', blob, 'imagen.png'); // 'imagen' es el nombre del campo en tu solicitud Flask

            // Enviar la imagen al servidor Flask
            const response = await fetch('/clasificar', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                // Mostrar la clasificación en la página web
                const predictionText = `Predicción: ${data.clasificacion}`;
                resultElement.textContent = predictionText;

                // Actualizar y mostrar la predicción sobre el video
                updatePrediction(predictionText);
            } else {
                console.error('Error al enviar la imagen al servidor.');
            }
        }, 'image/png');
    }


        
        
        

    // Capturar y enviar la imagen automáticamente cada 2.5 segundos
    setInterval(captureAndSendImage, captureInterval);
});
