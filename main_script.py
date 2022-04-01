import numpy as np
import cv2
import matplotlib.pyplot as plt
import requests


  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.1.18:8080/shot.jpg"

img_resp1 = requests.get(url)
img_arr1 = np.array(bytearray(img_resp1.content), dtype=np.uint8)
img1 = cv2.imdecode(img_arr1, -1)
resized_img1 = cv2.resize(img1,(600,400))

img_resp2 = requests.get(url)
img_arr2 = np.array(bytearray(img_resp2.content), dtype=np.uint8)
img2 = cv2.imdecode(img_arr2, -1)
resized_img2 = cv2.resize(img2,(600,400))
  
# While loop to continuously fetching data from the Url
while True:
    
    diff = cv2.absdiff(resized_img1, resized_img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 900:
            continue
            
        cv2.rectangle(resized_img1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(resized_img1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    image = cv2.resize(resized_img1, (1280,720))
    cv2.imshow("feed", resized_img1)
    resized_img1 = resized_img2
    
    img_resp2 = requests.get(url)
    img_arr2 = np.array(bytearray(img_resp2.content), dtype=np.uint8)
    img2 = cv2.imdecode(img_arr2, -1)
    resized_img2 = cv2.resize(img2,(600,400))

  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()