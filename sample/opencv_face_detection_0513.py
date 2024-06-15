import cv2
import os

# 創建人臉偵測物件
face_detector = cv2.CascadeClassifier(
    "../cv_model/haarcascade_frontalface_default.xml")

image_dir_path = "./images/"
for image_file_name in os.listdir(image_dir_path):
    image_path = image_dir_path + image_file_name

    print("Image Name: ", image_file_name)
    image = cv2.imread(image_path)  # 讀取圖片的像素資訊
    # Convert Color "to" Gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'outputs/{image_path}_gray.jpg', gray_image)  # 儲存灰階圖片
    faces = face_detector.detectMultiScale(
        gray_image, minNeighbors=4, minSize=(33, 33))  # 偵測臉部

    for x, y, width, height in faces:
        print((x, y), "-->", (x+width, y+height),
              '--> (w, h) =', (width, height))
        cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 4)
        cv2.circle(image, (x, y), 5, (255, 0, 0), 10)  # POINT 1: BLUE
        cv2.circle(image, (x+width, y+height), 5,
                   (0, 0, 255), 10)  # POINT 2: RED

    # 顯示圖片
    windows_name = f'{image_file_name} Window'
    cv2.imshow(windows_name, image)
    cv2.imwrite(f"outputs/{image_path}_faces.jpg", image)

# 關閉所有的windows
cv2.waitKey(0)
cv2.destroyAllWindows()
