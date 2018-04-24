import cv2

camera = cv2.VideoCapture(1)

while True:
    grabbed, frame = camera.read()
    cv2.imshow("Imagen", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break