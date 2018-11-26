import face_recognition
import cv2
import time
import sys
import numpy as np
from PIL import Image, ImageDraw

class img:
    def __init__(self, val):
        self.val = val
	#self.image = face_recognition.load_image_file(self.val)

    def setVal(self, val):
        self.val = val
        #self.image = face_recognition.load_image_file(self.val)
    
    def getVal(self):
        return self.val

   # def getImage(self):
       # return self.image

    def recognize_landmarks(self):
        return face_recognition.face_landmarks(self.getVal()) 

    def edit_landmarks(self):
        pil = 0
        for face_landmarks in self.recognize_landmarks():
            pil = Image.fromarray(self.val)
            d   = ImageDraw.Draw(pil, 'RGBA')
    #fill
         
    #forehead
            fore = []
            len_chin = (len(face_landmarks['chin']))
            len_eye = len(face_landmarks['right_eye'])
            len_lip = len(face_landmarks['top_lip'])
            fore.append(face_landmarks['chin'][0])
            Yinv  = face_landmarks['chin'][0][1]
            Xinv  = face_landmarks['chin'][0][0]
            forefactor  = 0.65
            yforefactor = face_landmarks['chin'][len_chin-1][0] - face_landmarks['chin'][len_chin-2][0]
       
            if face_landmarks['chin'][3][0] - face_landmarks['chin'][0][0] > 0:
                if yforefactor > 0:
                    for i in range(1, len_chin-1):
                        fore.append((face_landmarks['chin'][i][0], face_landmarks['left_eye'][0][1] - forefactor*(face_landmarks['chin'][i][1] - Yinv)))
                    fore.append(face_landmarks['chin'][len_chin-1])
                    for i in range(len_eye // 2, -1, -1):
                        fore.append(face_landmarks['right_eye'][i])
                    for i in range(len_eye // 2, -1, -1):
                        fore.append(face_landmarks['left_eye'][i])
                    d.polygon(fore, fill=(0,233,255,128))
    #Hair
                    hair = []
                    for i in range(0, len_chin-1):
                        hair.append(fore[i])
                    for i in range(1, 10):
                        hair.append((fore[len_chin-i][0]+(10+(10*i)), fore[len_chin-i][1])) 
                    for i in range(4, 17):
                        hair.append((fore[len_chin-i][0]+(5+(2*i)), fore[len_chin-i][1]-(45+(5*i))))
                    for i in range(14, 18):
                        hair.append((fore[len_chin-i][0]-(10+(1.5*i)), fore[len_chin-i][1]-(3*i)))
                    hair.append(face_landmarks['chin'][0]) 
                    d.line(hair, fill=(60, 180, 207, 128), width=3)
                    d.polygon(hair, fill=(60, 180, 207,200))
    #face
                    len_chin = len(face_landmarks['chin'])
                    len_eye  = len(face_landmarks['right_eye'])
                    len_lip  = len(face_landmarks['top_lip'])

                    y = []
                    x = []
                    for i in range(0, 1+ len_chin//3):
                        y.append(face_landmarks['chin'][i])
                    for i in range(0, 1+ len_lip//2):
                        y.append(face_landmarks['top_lip'][i])
                    for i in range(11, len_chin):
                        y.append(face_landmarks['chin'][i])
                    for i in range(len_eye//2, len_eye):
                        y.append(face_landmarks['right_eye'][i])
                    y.append(face_landmarks['right_eye'][0])
                    for i in range(len_eye//2, len_eye):
                        y.append(face_landmarks['left_eye'][i])
                    y.append(face_landmarks['left_eye'][0])
                    d.polygon(y, fill=(0,233,255,128))
                    for i in range(5, len_chin-5):
                        x.append(face_landmarks['chin'][i])
                    for i in range(0, 1+ len_lip//2):
                        x.append(face_landmarks['bottom_lip'][i])
                    d.polygon(x, fill=(0,233,255,128))
                    d.line(face_landmarks['chin'], fill=(0,233,255,128), width=3)

    #Eyebrows
                    d.polygon(face_landmarks['left_eyebrow'], fill=(0,200,230,150))
                    d.polygon(face_landmarks['right_eyebrow'], fill=(0,200,230,150))
                    d.line(face_landmarks['left_eyebrow'], fill=(0,200,230,150), width=2)
                    d.line(face_landmarks['right_eyebrow'], fill=(0,200,230,150), width=2)

   #Lips
                    d.polygon(face_landmarks['top_lip'], fill=(59, 181, 207, 128))
                    d.polygon(face_landmarks['bottom_lip'], fill=(59, 181, 207, 128))
                    d.line(face_landmarks['top_lip'], fill=(59, 181, 207, 128), width=2)
                    d.line(face_landmarks['bottom_lip'], fill=(59, 181, 207, 128), width=2)

   #Eyes
                    d.polygon(face_landmarks['left_eye'], fill=(153, 247, 255, 128))
                    d.polygon(face_landmarks['right_eye'], fill=(153, 247, 255, 128))
   
                    if face_landmarks['bottom_lip'][4][1] - face_landmarks['top_lip'][10][1] > 20:
                       # d.line((face_landmarks['bottom_lip'][4], face_landmarks['top_lip'][10]), fill=(0,0,0,128), width =3)
                        d.polygon(face_landmarks['left_eye'], fill=(0,0,255,200))
                        d.polygon(face_landmarks['right_eye'], fill=(0,0,255,200))
      
        return pil 



camera = cv2.VideoCapture(0)
while True:
    r, I = camera.read()
    #image = I[:,:,::-1]
    tse = img(I)
    x =  cv2.waitKey(1)
    if x == 27:
        break
    pic = tse.edit_landmarks()
    if pic:
        I = np.array(pic)
    cv2.imshow('y', I)

camera.release()

cv2.destroyAllWindows()

sys.exit(0)
