# -*- coding: utf-8 -*-
"""Copy of Copy of sub MLP pake asistol (brusaha ngecilin memori).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1opKj_5v1_q1Tiz5WCY90h1EGYUQpuNQD
"""

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from glob import glob
from google.colab import drive
import collections
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from tensorflow import keras

drive.mount('/content/drive',force_remount = True)

data_training1 = pd.read_csv("/content/drive/MyDrive/Tugas_Akhir/Dataset_Fix_Banget2/Training1.csv",delimiter=",")
data_training1

data_training0 = pd.read_csv("/content/drive/MyDrive/Tugas_Akhir/Dataset_Fix_Banget2/Training0.csv",delimiter=",")
data_training0

data_testing1 = pd.read_csv("/content/drive/MyDrive/Tugas_Akhir/Dataset_Fix_Banget2/Testing1.csv",delimiter=",")
data_testing1

data_testing0 = pd.read_csv("/content/drive/MyDrive/Tugas_Akhir/Dataset_Fix_Banget2/Testing0.csv",delimiter=",")
data_testing0

datatrainingall = data_training1.merge(data_training0,how='outer')
datatestingall = data_testing1.merge(data_testing0,how='outer')

y_train = datatrainingall['Label']
X_train = datatrainingall.drop(['Label'],axis=1)
y_test = datatestingall['Label']
X_test = datatestingall.drop(['Label'],axis=1)

#ANN Setting

model = tf.keras.Sequential([
                             tf.keras.layers.InputLayer(3),
tf.keras.layers.Dense(60,name="Hidden_1"),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(40, name="Hidden_2"),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(20, activation='relu', name="Hidden_3"),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(1, activation='sigmoid',name="Output")
],
name="Sequential")
# model.summary()

model.compile(optimizer='nadam',
            loss="binary_crossentropy",
            metrics=['accuracy'])
# "binary_crossentropy"
# model.compile(optimizer='adam',
#             loss="mean_squared_error",
#             metrics=['accuracy'])


#Checkpoint to save the best accuracy
checkpoint_filepath = '/content/checkpoint'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='accuracy',
    mode='max',
    save_best_only=True)

# model = get_basic_model()
history=model.fit(X_train,y_train, epochs=900, validation_data=(X_test,y_test), batch_size=16,callbacks=model_checkpoint_callback)
model.summary()

# my_callbacks = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

# history = model.fit(
#     X_train,y_train,
#     validation_data=(X_test, y_test),
#     batch_size=8,
#     epochs=600,
#     callbacks=[my_callbacks]
# )

my_acc = history.history['accuracy']
my_val_acc = history.history['val_accuracy']

# plot accuracy
plt.figure(figsize=(25, 5))
plt.subplot(2,1,1)
plt.plot(my_acc, label='Train')
plt.plot(my_val_acc, label='Validation')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
# plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

# visualize the loss training history
my_loss = history.history['loss']
my_val_loss = history.history['val_loss']

# plot loss
plt.figure(figsize=(25, 5))
plt.subplot(2,1,1)
plt.plot(my_loss, label='Train')
plt.plot(my_val_loss, label='Validation')
plt.legend(loc='upper right')
plt.ylabel('Loss')
# plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Loss')

for i in model.layers:
  print(i)

# model.load_weights(checkpoint_filepath) #To load the checkpoint
print(model.layers[0].weights) #Print Weight and Bias in Hidden Layer 1
print(model.layers[1].weights) #Print Weight and Bias in Hidden Layer 2
print(model.layers[2].weights) #Print Weight and Bias in Hidden Layer 3
print(model.layers[3].weights) #Print Weight and Bias in Hidden Layer 3

import sys
np.set_printoptions(threshold=sys.maxsize)

simpanweight = model.layers[0].weights
np.savetxt('Weights1.txt', simpanweight ,fmt='%s')

simpanweight1 = model.layers[2].weights
np.savetxt('Weights2.txt', simpanweight1 ,fmt='%s')

simpanweight2 = model.layers[4].weights
np.savetxt('Weights3.txt', simpanweight2 ,fmt='%s')

simpanweight3 = model.layers[6].weights
np.savetxt('Output_Layer.txt', simpanweight3 ,fmt='%s')

#Prediction using data test
prediction = model.predict(X_test)
prediction

#Change the result of prediction into binary
for i in range(len(prediction)):
    if prediction[i] >= 0.5:
      prediction[i]=1
    else: prediction[i]=0
    print(prediction[i])

import seaborn as sns
#Confussion Matrix

conmat=confusion_matrix(y_test,prediction)
sns.heatmap(conmat.T, square=True, annot=True, fmt='d', cbar=False) 
plt.xlabel('true class') 
plt.ylabel('predicted class')
print(classification_report(y_test,prediction))

print('data testing')
accuracy = (conmat[0,0]+conmat[1,1])/(conmat[0,0]+conmat[0,1]+conmat[1,0]+conmat[1,1])
print('akurasi :', accuracy)

sensitivity1 = conmat[0,0]/(conmat[0,0]+conmat[0,1])
print('sensitivitas : ', sensitivity1 )

specificity1 = conmat[1,1]/(conmat[1,0]+conmat[1,1])
print('spesifisitas : ', specificity1)

precision1 = conmat[0,0]/(conmat[0,0]+conmat[1,0])
print('presisi : ', precision1 )

#Prediction using data test
prediction2 = model.predict(X_train)
prediction2

#Change the result of prediction into binary
for i in range(len(prediction2)):
    if prediction2[i] >= 0.5:
      prediction2[i]=1
    else: prediction2[i]=0
    print(prediction2[i])

#Confussion Matrix Training Data

conmat2=confusion_matrix(y_train,prediction2)
sns.heatmap(conmat2.T, square=True, annot=True, fmt='d', cbar=False) 
plt.xlabel('true class') 
plt.ylabel('predicted class')
print(classification_report(y_train,prediction2))

print('data training')
accuracy2 = (conmat2[0,0]+conmat2[1,1])/(conmat2[0,0]+conmat2[0,1]+conmat2[1,0]+conmat2[1,1])
print('akurasi :', accuracy2)

sensitivity2 = conmat2[0,0]/(conmat2[0,0]+conmat2[0,1])
print('sensitivitas : ', sensitivity2 )

specificity2 = conmat2[1,1]/(conmat2[1,0]+conmat2[1,1])
print('spesifisitas : ', specificity2)

precision2 = conmat2[0,0]/(conmat2[0,0]+conmat2[1,0])
print('presisi : ', precision2 )

gabung = datatrainingall.merge(datatestingall,how='outer')

y = gabung['Label']
X = gabung.drop(['Label'],axis=1)

prediction3 = model.predict(X)

for i in range(len(prediction3)):
    if prediction3[i] >= 0.5:
      prediction3[i]=1
    else: prediction3[i]=0

#Confussion Matrix Training Data

conmat3=confusion_matrix(y,prediction3)
sns.heatmap(conmat3.T, square=True, annot=True, fmt='d', cbar=False) 
plt.xlabel('true class') 
plt.ylabel('predicted class')
print(classification_report(y,prediction3))

