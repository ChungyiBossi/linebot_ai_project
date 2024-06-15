from imgurpython import ImgurClient
from KEYS import IMGUR_CLIENT_ID, IMGUR_CLIENT_SECERT

imgur_client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECERT)

def upload_image_to_imgur(image_path):
    result = imgur_client.upload_from_path(image_path)
    return result['link']

if __name__ == '__main__':
    print(upload_image_to_imgur('image.jpg'))