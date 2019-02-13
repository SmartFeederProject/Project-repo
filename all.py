import cv2
import os
import time
from datetime import datetime
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from tqdm import tqdm

img_width, img_height = 150, 150

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
model.load_weights('/home/batya/Desktop/weights_4.h5')
test_datagen = ImageDataGenerator(rescale=1. / 255)

camera = cv2.VideoCapture(0)
ret_v, image_old = camera.read()

i = 0
index_1 = 0
index_2 = 0
index_3 = 0
flagged = 0

f = open('qqq.txt', 'a')
t = open('rrr.txt', 'a')

path = '/home/batya/Desktop/Birds'
path_no = '/home/batya/Desktop/NeBirds'
path_idk = '/home/batya/Desktop/IDK'
path_current = '/home/batya/Desktop/Current'

while True:
    time.sleep(0.1)
    ret_v, image = camera.read()
    dimg = cv2.absdiff(image, image_old)
    ds = cv2.sumElems(dimg)
    d = (ds[0] + ds[1] + ds[2])/(1280*720)
    image_old = image
    print(d, flagged)
    tm = datetime.now()
    f.write(str(d) + '\n')
    t.write(str(tm) + '\n')

    pic = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pic_keras = pic / 255.
    pic_keras = cv2.resize(pic_keras, (150, 150))
    probab = model.predict_proba(pic_keras[None, ...], verbose=None)[0][0]

    if i > 30:
        if flagged > 0:
            flagged = flagged - 1
            if probab < 0.5:
                cv2.imwrite(os.path.join(path_no, 'img' + str(index_1) + '.png'), image)
                index_1 += 1
                continue

            if probab > 0.9:
                cv2.imwrite(os.path.join(path, 'img' + str(index_2) + '.png'), image)
                index_2 += 1
                continue
        
            cv2.imwrite(os.path.join(path_idk, 'img' + str(index_3) + '.png'), image)
            index_3 += 1

        if d > 5:
            flagged = 25
            if probab < 0.5:
                cv2.imwrite(os.path.join(path_no, 'img' + str(index_1) + '.png'), image)
                index_1 += 1
                continue

            if probab > 0.9:
                cv2.imwrite(os.path.join(path, 'img' + str(index_2) + '.png'), image)
                index_2 += 1
                continue
        
            cv2.imwrite(os.path.join(path_idk, 'img' + str(index_3) + '.png'), image)
            index_3 += 1
        cv2.imwrite(os.path.join(path_current, 'img.png'), image)
    else:
        i += 1