from AccidentDetection.preprocessing.aspectawarepreprocessor import AspectAwarePreprocessor
from AccidentDetection.preprocessing.imagetoarrayprocessor import ImageToArrayProcessor
from AccidentDetection.preprocessing.meanpreprocessor import MeanPreprocessor
from AccidentDetection.preprocessing.patchpreprocessor import PatchPreporcessor
from AccidentDetection.preprocessing.simpleProcessor import SimplePreprocessor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import  train_test_split
from AccidentDetection.dataset.simpleDatasetLoader import  SimpleDatasetLoader
from AccidentDetection.nn.cnn.vgg import MiniVGGNet
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from imutils import paths
import numpy as np
import argparse
import cv2



aug = ImageDataGenerator(rotation_range=20,zoom_range=0.15,width_shift_range=0.2,height_shift_range=0.2,
                        shear_range=0.15,horizontal_flip=True,fill_mode="nearest")


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
    help="Path to the output loss/accuracy plot")
ap.add_argument("-d", "--dataset", required=True,
    help="Path to the dataset")
args = vars(ap.parse_args())

classLabels = ["damaged","undamaged"]

print("going to load images")
imagePaths = np.array(list(paths.list_images(args["dataset"])))
print("Image paths ",imagePaths)



sp = SimplePreprocessor(32,32)
iap = ImageToArrayProcessor()

sdl = SimpleDatasetLoader(preprocessor=[sp,iap])
(data,label) =sdl.load(imagesPaths,verbose=500)

le = LabelEncoder()
labels = le.fit_transform(label)

data = data.astype("float32")/255.0

datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)


(trainX,testX,trainY,testY) = train_test_split(data,labels,test_size=0.25,random_state=40)

# train_datagen = ImageDataGenerator(
#         rescale=1./255,
#         shear_range=0.2,
#         zoom_range=0.2,
#         horizontal_flip=True)

# test_datagen = ImageDataGenerator(rescale=1./255)

# train_generator = train_datagen.flow_from_directory(
#         'data/train',
#         target_size=(150, 150),
#         batch_size=32,
#         class_mode='binary')
# validation_generator = test_datagen.flow_from_directory(
#         'data/validation',
#         target_size=(150, 150),
#         batch_size=32,
#         class_mode='binary')
# print("INFO loading model")

#callbacks =[LearningRateScheduler(step_decay)]

datagen.fit(trainX)


model.fit_generator(datagen.flow(trainX, trainY, batch_size=32),
                    steps_per_epoch=len(trainX) / 32, epochs=epochs)
opt = SGD(lr=0.01, momentum=0.9, nesterov=True)

model = MiniVGGNet.build(width=32, height=32, depth=3, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt,
    metrics=["accuracy"])

print("[INFO] training the network...")

H = model.fit(trainX, trainY, validation_data=(testX, testY), batch_size=64,
    epochs=20, verbose=1)

print("[INFO] evaluating network...")

predictions = model.predict(testX, batch_size=64)



plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 20), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, 20), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, 20), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, 20), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy on CIFAr-10")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig(args["output"])






