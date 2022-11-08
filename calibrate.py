
import numpy as np
import argparse
import cv2
import regions
#X:  1365 Y:  737
# regions.Regions(xIntercept, width, length, yIntercept, rows, columns)
regions = regions.Regions(300, 800, 750, 300,3,3)
videoCapture = cv2.VideoCapture(0)
videoCapture.set(3, 1000)
videoCapture.set(4, 1000)
while True:

	ret, frame = videoCapture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(5,5),0)
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 30, param1= 100, param2=60, minRadius= 60, maxRadius=65)	
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		for (x, y, r) in circles:

			cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			print ("Region", regions.checkRegion(x,y))
			print ("X: ", x, "Y: ", y)


	fontIndex = 0

	for i in range(regions.totalYintercepts-1):
		for ii in range(regions.totalXintercepts-1):
			x1 = regions.xIntercepts()[ii]
			x2 = regions.xIntercepts()[ii + 1]
			y1 = regions.yIntercepts()[i]
			y2 = regions.yIntercepts()[i+1]
			cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),2)
			fontIndex = fontIndex + 1
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,str(fontIndex),(int(x1) +5,int(y1)+25), font, 0.7,(255,255,255),2)

	cv2.imshow('Video',frame)
	cv2.imshow('Video',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

videoCapture.release()
cv2.destroyAllWindows()
