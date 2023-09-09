from time import sleep

import cv2
import numpy as np
from Adafruit_IO import Client
from keras.models import load_model

ADAFRUIT_IO_USERNAME = "joseigo"
ADAFRUIT_IO_KEY = "aio_pnbi48Ofk6lmJhgF1Gh4NJId60xS"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
lib = aio.feeds("lib")
ult_est = 0
aio.send_data(lib.key, 0)


def verificar_confidence_score(class_name, confidence_score):
    if class_name != "negado\n":
        acesso = 1
        print(f"Acesso permitido {class_name}")
        print(f"Acesso permitido, acuracia:{confidence_score}")
        aio.send_data(lib.key, acesso)
        sleep(5)  # segundos
        aio.send_data(lib.key, 0)
        return True
    elif ult_est == 1:
        acesso = 0
        print(f"Acesso negado, acuracia:{confidence_score}")
        aio.send_data(lib.key, acesso)
        sleep(3)  # segundos
        return False
    else:
        print(f"Acesso negado, acuracia:{confidence_score}")
        sleep(3)  # segundos
        aio.send_data(lib.key, 0)
        return False


# https://teachablemachine.withgoogle.com

# Configura as opções de impressão do numpy para evitar notação cientifica nos resultados
np.set_printoptions(suppress=True)

# Carrega o modelo previamente treinado
model = load_model("keras_model.h5", compile=False)

# Carrega os rótulos de cada classe
class_names = open("labels.txt", "r").readlines()

# Essa linha cria uma matriz vazia com a forma (shape) de (1, 224, 224, 3). Essa matriz será usada para armazenar a imagem que será alimentada ao modelo.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

url = "http://192.168.0.12:81"
# url = 0
vid = cv2.VideoCapture(url)

while True:
    ret, frame = vid.read()

    if ret:
        # Essa linha abre a imagem do caminho especificado (image_espcam) usando a biblioteca PIL. A imagem é convertida para o modo RGB, se necessário.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Essas linhas redimensionam a imagem para que tenha pelo menos o tamanho de (224, 224) e, em seguida, realiza um corte a partir do centro da imagem, se necessário, para ajustá-la ao tamanho desejado.
        # resizing the image to be at least 224x224 and then cropping from the center
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Essa linha converte a imagem para um array do NumPy.
        # turn the image into a numpy array
        image_array = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Essa linha normaliza o array da imagem, dividindo cada valor por 127,5 e subtraindo 1. Isso é feito para garantir que os valores estejam na faixa correta para o modelo.
        # Normalize the image
        normalized_image_array = (image_array / 127.5) - 1

        # Essa linha atribui o array normalizado da imagem à primeira posição da matriz data.
        # Load the image into the array
        data[0] = normalized_image_array

        # Essas linhas usam o modelo carregado para fazer uma previsão com a imagem fornecida. A função predict() retorna uma matriz de probabilidades para cada classe. np.argmax() é usado para obter
        # o índice da classe com a maior probabilidade. O nome da classe correspondente é obtido a partir da lista de rótulos (class_names). A pontuação de confiança (confidence_score) é obtida a partir da matriz de probabilidades.
        # Predicts the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        # print(class_names)
        confidence_score = prediction[0][index]
        ult_est = verificar_confidence_score(class_name, confidence_score)
        # Listen to the keyboard for presses.

    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
