import cv2
import os 
from tensorflow.keras.models import load_model
import numpy as np

# Load the pre-trained model
model = load_model("vgg_cans.h5")
class_labels = ["can", "cups", "pets"]

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    img = cv2.resize(frame, (64, 64))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

   
    predictions = model.predict(img)
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_labels[predicted_class_index]
    confidence = np.max(predictions) * 100

    if confidence > 20:  
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        
        largest_contour = max(contours, key=cv2.contourArea)

        
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        
        cv2.putText(frame, f"Prediction: {predicted_class}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Confidence: {confidence:.2f}%", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    
    cv2.imshow("cifar10",frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()