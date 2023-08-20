import cv2
import time
from send_email import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
object_status = []

while True:
    status = 0
    checker, frame = video.read()

    # Convert frame into gray color for less memory consumption
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur image for less memory
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    # cv2.imshow('Test video', gray_frame_gau)

    # Create a frame on which is Frame Differencing being done
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # If I want to see difference on the frames
    # cv2.imshow('Test video', delta_frame)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # cv2.imshow('Test video', dil_frame)

    # Show contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        # Change variable status if there is an object
        if rectangle.any():
            status = 1

    # Check if there is 1 to 0 change in the list - means object left the camera
    object_status.append(status)
    object_status = object_status[-2:]

    if object_status[0] == 1 and object_status[1] == 0:
        send_email()

    cv2.imshow('Video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
