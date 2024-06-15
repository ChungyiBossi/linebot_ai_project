import cv2
import numpy as np
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path='blaze_face_short_range.tflite'),
    running_mode=VisionRunningMode.IMAGE)
mediapipe_face_detector = FaceDetector.create_from_options(options)

def detect_faces_with_mediapipe(image_path, is_show_img=False):
    image = cv2.imread(image_path) # 直接讀取圖片
    h, w, _ = image.shape
    
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(image, cv2.COLOR_BGRA2RGB))  # 轉成Mediapipe的格式，他是接受彩圖的
    # mp_image = mp.Image.create_from_file(image_path)

    print(np.all(np.equal(image, mp_image.numpy_view())))
    detection_result = mediapipe_face_detector.detect(mp_image)
    for detection in detection_result.detections:
        # 標示臉部範圍
        bbox = detection.bounding_box
        lx = bbox.origin_x
        ly = bbox.origin_y
        width = bbox.width
        height = bbox.height
        cv2.rectangle(image,(lx,ly),(lx+width,ly+height),(0,0,255),5)

        # 標示五官
        for keyPoint in detection.keypoints:
            print(keyPoint, w, h)
            cx = int(keyPoint.x*w)
            cy = int(keyPoint.y*h)
            print(cx, cy)
            cv2.circle(image, (cx,cy), 10, (0,0,255), -1) 
        print(bbox)

    if is_show_img:
        cv2.imshow('mediapipe_face_detection', image)     # 如果讀取成功，顯示該幀的畫面
        cv2.waitKey(0)
        cv2.destroyAllWindows()                 # 結束所有視窗
    cv2.imwrite(image_path.replace(".jpg", "_faces_mediapipe.jpg"), image)


if __name__ == '__main__':
    detect_faces_with_mediapipe('images7.jpg', is_show_img=True)

