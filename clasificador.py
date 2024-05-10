from flask import Flask, request, jsonify
from tensorflow import keras
import numpy as np
from PIL import Image
from flask import render_template
import io

app = Flask(__name__)

# Cargar el modelo pre-entrenado ResNet50V2
model = keras.models.load_model('Model/UltimoEfficeNet.h5')

# Clases de clasificación
clases = ['AltaDensidad', 'Compartida', 'Normal', 'Parking']

@app.route('/')
def index():
    # Esta función podría renderizar la página principal (index.html)
    # o redirigir a otra página si es necesario.
    return render_template('index.html')  # Asegúrate de que render_template esté importado adecuadamente


from PIL import Image

@app.route('/clasificar', methods=['POST'])
def clasificar_imagen():
    imagen_pil = None  # Inicializa la variable fuera del bloque try
    try:
        # Obtener la imagen enviada desde la página web
        imagen = request.files['imagen']

        if imagen is not None:
            # Procesar la imagen y realizar la predicción utilizando el modelo
            imagen_pil = Image.open(imagen)
            
            # Convertir la imagen a RGB si tiene 4 canales
            if imagen_pil.mode == 'RGBA':
                imagen_pil = imagen_pil.convert('RGB')
            
            imagen_pil = imagen_pil.resize((224, 224))  # Asegúrate de que la imagen tenga las dimensiones correctas
            imagen_array = np.array(imagen_pil)
            imagen_array = imagen_array / 255.0  # Normaliza la imagen (si es necesario)
            imagen_array = np.expand_dims(imagen_array, axis=0)  # Agrega una dimensión para el lote
            
            prediccion = model.predict(imagen_array)
            clase_predicha = clases[np.argmax(prediccion)]

            # Devolver la clasificación como una respuesta JSON
            resultado = {"clasificacion": clase_predicha}
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se envió ninguna imagen en la solicitud"}), 400

    except Exception as e:
        if imagen_pil is not None:
            imagen_pil.close()  # Cierra la imagen si se abrió correctamente
        print("Error en la clasificación:", str(e))  # Agregar registro
        return jsonify({"error": str(e)}), 500
    finally:
        if imagen_pil is not None:
            imagen_pil.close()  # Asegúrate de cerrar la imagen en caso de excepción


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
