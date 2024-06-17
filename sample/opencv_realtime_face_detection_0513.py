import cv2
import time

capture = cv2.VideoCapture(0)

time.sleep(3)
if capture.isOpened():
    face_detector = cv2.CascadeClassifier(
        "cv_model/haarcascade_frontalface_default.xml")
    while True:
        success, frame = capture.read()
        if success:
            # Convert Color "to" Gray
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(
                gray_frame, minNeighbors=4, minSize=(33, 33))  # 偵測臉部
            for x, y, width, height in faces:
                print((x, y), "-->", (x+width, y+height),
                      '--> (w, h) =', (width, height))
                cv2.rectangle(frame, (x, y), (x+width, y+height),
                              (0, 255, 0), 4)
                cv2.circle(frame, (x, y), 5, (255, 0, 0), 10)  # POINT 1: BLUE
                cv2.circle(frame, (x+width, y+height), 5,
                           (0, 0, 255), 10)  # POINT 2: RED

            windows_name = f'Camera'
            cv2.imshow(windows_name, frame)
        else:
            print('Capture Read Fail.....')
            time.sleep(2)

        if cv2.waitKey(60) == ord('q'):
            cv2.destroyAllWindows()
            capture.release()
            break
else:
    print("Camera Not Found")
