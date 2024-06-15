import cv2

face_detector = cv2.CascadeClassifier(
    "cv_model/haarcascade_frontalface_default.xml")


def detect_faces(image_path, is_show_img=False):
    # Read file
    image = cv2.imread(image_path)  # 讀取圖片的像素資訊
    # Convert Color "to" Gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect
    faces = face_detector.detectMultiScale(
        gray_image, minNeighbors=4, minSize=(33, 33))  # 偵測臉部
    for x, y, width, height in faces:
        print((x, y), "-->", (x+width, y+height),
              '--> (w, h) =', (width, height))
        cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 4)
        cv2.circle(image, (x, y), 5, (255, 0, 0), 10)  # POINT 1: BLUE
        cv2.circle(image, (x+width, y+height), 5,
                   (0, 0, 255), 10)  # POINT 2: RED

    if is_show_img:
        # 顯示圖片
        windows_name = f'Window'
        cv2.imshow(windows_name, image)
        # 關閉所有的windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    cv2.imwrite(image_path.replace(".jpg", "_faces.jpg"), image)

    return len(faces)


if __name__ == '__main__':
    detect_faces('./images/test.jpg')
    detect_faces('./images/test_2.jpg')
    detect_faces('./images/test_3.jpg')
