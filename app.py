from flask import Flask, render_template, request
from PIL import Image
import requests
import numpy as np
import process_model
from io import BytesIO
import base64

app = Flask(__name__)

def get_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((224, 224))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_base64


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Pobranie adresu URL obrazu z formularza
        image_url = request.form['image_url']

        # Przetworzenie obrazu do odpowiedniego formatu
        img, labels = process_model.classify_fruit(image_url)

        # Konwersja obrazu na ciąg base64
        img_base64 = get_image_from_url(image_url)

        return render_template('pred.html', img=img_base64, labels=labels)

    return render_template('pred.html')

if __name__ == '__main__':
    app.run(debug=True)
