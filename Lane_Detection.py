from cv2 import cv2
import numpy as np
from math import sqrt

image=cv2.imread("test.jpg")
h=image.shape[0]
w=image.shape[1]

if w%2==1:
    whalf=(w-1)/2
else:
    whalf=w/2
if h%2==1:
    hhalf=(h-1)/2
else:
    hhalf=h/2
hhalf=int(hhalf)
whalf=int(whalf)

beyaz = []
j=0
for x in range(0,h):#siyah noktaları buldum
    for y in range(0,w):
        #renk=img[x,y]
        a=image[x,y,0]
        b=image[x,y,1]
        c=image[x,y,2]
        if a>200 and b>200 and c>200:
            beyaz.append((x,y))
            j=j+1
imgyeni=np.zeros((h, w, 1), np.uint8)
for i in range(j):#Okuma yaparken beyaz noktalara baktığı için beyazlatma yaptım
    imgyeni[beyaz[i][0],beyaz[i][1]]=[255]
w3=w*4/100
kernel = np.ones((5,5),np.uint8)
imgyeni=cv2.morphologyEx(imgyeni,cv2.MORPH_OPEN,kernel)
imgright1=imgyeni[hhalf:h, whalf:w]
imgleft1=imgyeni[hhalf:h, 0:whalf]
cnt=0
contours, npaHierarchy = cv2.findContours(imgright1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
listofpossbileright=[]
for contour in contours:
    boundingRect = cv2.boundingRect(contour)
    [intX, intY, intWidth, intHeight] = boundingRect
    if intWidth>w3:
        listofpossbileright.append(boundingRect)
        sayi1=sqrt(((0-intX)**2)+((imgright1.shape[0]-intY)**2))#imgright1.shape[1]
        if cnt==0:
            sonucright=sayi1
            lanelinesright=boundingRect
            cnt=1
        if cnt ==1 and sayi1<sonucright:
            sonucright=sayi1
            lanelinesright=boundingRect
[intX1 ,intY1, intWidth1, intHeight1] = lanelinesright
#cv2.circle (imgright1,(intX,intY),30,(255,255,255),-1)
h11=imgright1.shape[0]
oran=intHeight1/intWidth1
deger1=h11-intY1
weight1=deger1/oran
cnt=0
contours, npaHierarchy = cv2.findContours(imgleft1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
listofpossbileleft=[]
for contour in contours:
    boundingRect = cv2.boundingRect(contour)
    [intX, intY, intWidth, intHeight] = boundingRect
    if intWidth>w3:
        listofpossbileleft.append(boundingRect)
        sayi2=sqrt(((imgright1.shape[1]-intX)**2)+((imgright1.shape[0]-intY)**2))
        if cnt==0:
            sonucleft=sayi2
            lanelinesleft=boundingRect
            cnt=1
        if cnt ==1 and sayi1<sonucleft:
            sonucleft=sayi1
            lanelinesleft=boundingRect
[intX, intY, intWidth, intHeight] = lanelinesleft
#cv2.circle (imgleft1,(intX,intY),30,(255,255,255),-1)
h1=imgright1.shape[0]
oran=intHeight/intWidth
deger1=h1-intY
weight=deger1/oran
print(lanelinesleft)
pts = np.array([[intX-int(weight),hhalf+int(h1)],[intX,hhalf+intY],[whalf+intX1,hhalf+intY1],[whalf+int(weight1)+intX,hhalf+int(h11)]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.polylines(image,[pts],True,(140,130,17))
font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.circle (imgleft1,(intX+intWidth,intY),30,(255,255,255),-1)
#print(listofpossbileleft)
#beyaz yerlerin arabaya yakınlığını bulmak için 2 nokta arasındaki uzaklıktan buluruz.
#noktayı sol tarafta ise sağ alt köşe, sağ tarafta ise sol alt noktadan çıkarırız.

pts = np.array([[50,160],[125,160],[160,230],[10,230]], np.int32)


cv2.imshow("resim",image)
cv2.waitKey()