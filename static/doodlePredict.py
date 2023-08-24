from PIL import Image, ImageOps
from io import BytesIO
import base64
import math
import numpy as np

import tensorflow as tf
from tensorflow import keras
import cv2

model = tf.keras.models.load_model("static/model.keras")


#Convert image data with is in base64 to numpy image
def img_conversion(img_url):
    base64_decoded = base64.b64decode(img_url)
    image = Image.open(BytesIO(base64_decoded))
    image = image.convert("L")
    image_np = np.array(image)

    return image_np


#Crop out excessive white space from numpy image
def img_crop(img_np):
    mask = cv2.inRange(img_np, 220, 255)
    black = np.where(mask==0)
    x_min, y_min, x_max, y_max = np.min(black[1]), np.min(black[0]), np.max(black[1]), np.max(black[0])

    x_diff = x_max - x_min
    y_diff = y_max - y_min

    diff = x_diff - y_diff

    if x_diff > y_diff:
        diff = x_diff - y_diff
        y_min -= math.floor(diff / 2)
        y_max += math.ceil(diff / 2)
    else:
        diff = y_diff - x_diff
        x_min -= math.floor(diff / 2)
        x_max += math.ceil(diff / 2)


    crop = img_np[y_min-50:y_max+50, x_min-50:x_max+50]

    return crop

    

def predict(img_url):
    image_np = img_conversion(img_url)
    image_cropped = img_crop(image_np)

    #convert numpy image to pillow image to use pillow.resize function
    image = Image.fromarray(image_cropped.astype('uint8'), 'L')
    image = image.resize((28,28))

    #for some reason converting image to "L" or grayscale causes inversion so we need to invert the image back
    image = image.convert("L")
    image = ImageOps.invert(image)

    #image.save("test.png")

    #change image back to numpy image and reshape to fit in our model
    image_np = np.array(image)
    image_np = image_np.reshape(1, 28, 28, 1)

    #predict using image_np and sort the predictions
    predict = model.predict(image_np)
    classes = np.argsort(predict)
    classes = np.flip(classes)
    predict[0] = predict[0] * 100

    predict.sort()
    predict = np.flip(predict)
    result = np.c_[classes[0],predict[0]]
    return result

