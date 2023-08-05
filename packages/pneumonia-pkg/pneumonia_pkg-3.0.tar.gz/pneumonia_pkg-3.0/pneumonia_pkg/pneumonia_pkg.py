import cv2
import numpy as np
from keras.models import load_model

class prediction:
    def predict(self,image):
        model = load_model('/pneumonia_pkg/cnn_model_xray_vgg16.h5')
        image1 = cv2.resize(image, (224,224))
        image1 = np.array(image1)
        image2 = np.reshape(image1,(1, 224, 224, 3))
        pred = model.predict(image2)
        if pred<0.5:
            label = "Negative"
        else:
            label = "Positive"
        cv2.putText(image1, label,(0,30),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0),2)
        return(image1,label)
        