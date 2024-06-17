import mediapipe as mp
import cv2

model_path = 'cv_model/face_stylizer_color_sketch.task'
# model_path = 'cv_model/face_stylizer_color_ink.task'
# model_path = 'cv_model/face_stylizer_oil_painting.task'
image_path = 'images/image.jpg'

BaseOptions = mp.tasks.BaseOptions
Facestylizer = mp.tasks.vision.FaceStylizer
FacestylizerOptions = mp.tasks.vision.FaceStylizerOptions

# Create a face stylizer instance with the image mode:
options = FacestylizerOptions(
    base_options=BaseOptions(model_asset_path=model_path)
)

with Facestylizer.create_from_options(options) as stylizer:
    # Load the input image from an image file.
    mp_image = mp.Image.create_from_file(image_path)

    # # Load the input image from a numpy array.
    # mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_image)
    face_stylizer_result = stylizer.stylize(mp_image)

    stylized_image = face_stylizer_result.numpy_view()
    stylized_image = cv2.cvtColor(stylized_image, cv2.COLOR_RGB2BGR) 
    
    cv2.imshow("Stylized Image: ", stylized_image)
    cv2.waitKey(0)