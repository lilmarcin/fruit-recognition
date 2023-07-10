from keras.models import load_model
import h5py
import requests
import numpy as np
from keras.preprocessing import image
from keras.utils import img_to_array
from PIL import Image, ImageFile
from io import BytesIO

model_path = 'fruit_classifier_model_96.h5'
model = load_model(model_path)

with h5py.File(model_path, 'r') as file:
    labels = file['labels'][:]
    fruit_names = [label.decode() for label in labels]

def preprocess_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img.astype('float32') / 255
    return img

def classify_fruit(image_url):
    img = preprocess_image(image_url)
    fruit_dict = {}

    # Przewidywanie etykiet dla obrazu
    predictions = model.predict(img)[0]

    # Dopasowanie etykiet do przewidywanych wyników
    for i, pred in enumerate(predictions):
        label = fruit_names[i]
        fruit_dict[label] = round(pred * 100, 2)

    # Zaokrąglenie wartości poniżej 0.001 do 0.00
    for label, value in fruit_dict.items():
        if value <= 0.001:
            fruit_dict[label] = 0.00

    # Sortowanie etykiet według prawdopodobieństwa w kolejności malejącej
    sorted_labels = sorted(fruit_dict.items(), key=lambda x: x[1], reverse=True)

    # Wybieranie trzech etykiet z największym prawdopodobieństwem
    top_labels = sorted_labels[:3]

    return img, top_labels



# Przykład użycia:
#image_url = "https://i.ibb.co/QdrSLsF/19-100.jpg"
#image_url = "https://media.istockphoto.com/id/1291262112/photo/banana.jpg?s=170667a&w=0&k=20&c=BrgDCBrH3iCUHI0MXafUnkvz8lmDMelsZfKsXud1fr0=" 
#image_url = "https://100procent-natury.pl/userdata/public/gfx/1586/JABLKO-HONEY.jpg"
#preprocessed_image = preprocess_image(image_url)
#result = classify_fruit(preprocessed_image)
#print(result)