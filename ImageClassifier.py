import os
import cv2
import numpy as np

path = "ImagesQuery"
images = []
classNames = []

myList = os.listdir(path)
print(myList)

for cl in myList:
    imgCur = cv2.imread(f"{path}/{cl}", 0) # if we write ,0 it means that magine is bw
    images .append(imgCur)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

orb = cv2.ORB_create()

def findDes(images):
    desList=[]
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList

def FindID(img, desList):
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    if len(matchList) != 0:
        if max(matchList) > 12:
            finalVal = matchList.index(max(matchList))
    return finalVal

desList = findDes(images)
print(len(desList))

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgOriginal = img.copy()
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    id = FindID(img2, desList)
    if id != -1:
        cv2.putText(imgOriginal, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Img", imgOriginal)
    if cv2.waitKey(1) == ord("q"):
        break