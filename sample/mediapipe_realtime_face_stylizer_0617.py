import mediapipe as mp
import cv2
import time
import math

model_path = 'cv_model/face_stylizer_color_sketch.task'
# model_path = 'cv_model/face_stylizer_color_ink.task'
# model_path = 'cv_model/face_stylizer_oil_painting.task'
image_path = 'image.jpg'

BaseOptions = mp.tasks.BaseOptions
Facestylizer = mp.tasks.vision.FaceStylizer
FacestylizerOptions = mp.tasks.vision.FaceStylizerOptions

# Create a face stylizer instance with the image mode:
options = FacestylizerOptions(
    base_options=BaseOptions(model_asset_path=model_path)
)

def resize_and_show(image, size=(640, 480)):
    DESIRED_WIDTH, DESIRED_HEIGHT = size
    h, w = image.shape[:2]
    if h < w:
        img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    else:
        img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
    cv2.imshow("Stylized Image", img)


frame_delay_in_ms = 30
with Facestylizer.create_from_options(options) as stylizer:
    
    capture = cv2.VideoCapture(0)
    time.sleep(3)
    if capture.isOpened():
        while True:
            success, frame = capture.read()
            if success:
                # # Load the input image from a numpy array.
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                try:
                    face_stylizer_result = stylizer.stylize(mp_image)
                    stylized_image = cv2.cvtColor(face_stylizer_result.numpy_view(), cv2.COLOR_RGB2BGR) 
                    resize_and_show(stylized_image)
                except AttributeError:
                    resize_and_show(stylized_image)
            else:
                print('Capture Read Fail.....')
                time.sleep(2)

            if cv2.waitKey(frame_delay_in_ms) == ord('q'):
                cv2.destroyAllWindows()
                capture.release()
                break
    else:
        print("Camera Not Found")

