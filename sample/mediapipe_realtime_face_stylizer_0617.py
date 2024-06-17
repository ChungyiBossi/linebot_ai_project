import mediapipe as mp
import cv2
import time

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
                    stylized_image = face_stylizer_result.numpy_view()
                    stylized_image = cv2.cvtColor(stylized_image, cv2.COLOR_RGB2BGR) 
                    stylized_image = cv2.resize(stylized_image, (640, 480))
                    windows_name = f'Camera'
                    cv2.imshow(windows_name, stylized_image)
                except AttributeError:
                    cv2.imshow(windows_name, frame)
            else:
                print('Capture Read Fail.....')
                time.sleep(2)

            if cv2.waitKey(frame_delay_in_ms) == ord('q'):
                cv2.destroyAllWindows()
                capture.release()
                break
    else:
        print("Camera Not Found")

