import os
from fastapi import HTTPException
from App.Security.config import WebUISetting
import requests
import base64
import io
from PIL import Image

class ImageService:
    def __init__(self):
        self.webui_setting = WebUISetting()

    def generate_image(self, payload):
        response = requests.post(url=f"{self.webui_setting.WEBUI_URL}/sdapi/v1/txt2img", json=payload)
        r = response.json()
        list_image_base64 = list(r['images'])
        return list_image_base64

    def decode_image(self, image_base64):
        image = Image.open(io.BytesIO(base64.b64decode(image_base64)))
        # image = io.BytesIO(base64.b64decode(image_base64))
        return image

    """
    def get_image_by_name(self, image_name: str, image_repo: ImagePathRepository):
        image = image_repo.get_image_by_image_name(image_name=image_name)
        return image if image is not None else None

    def show_images(self, user_id: int, image_repo: ImagePathRepository):
        images = image_repo.get_images_by_makerid(makerid=user_id)
        return images if len(images) > 0 else []
    
    def save_image(self, image_base64, maker_id: int, image_name: str, image_repo: ImagePathRepository):
        save_path = self.webui_setting.SAVE_PATH

        save_image_wanted = Image.open(io.BytesIO(base64.b64decode(image_base64)))
        save_image_wanted.show()
        image_path = save_path + image_name + '.png'
        print(os.getcwd())
        save_image_wanted.save(image_path, format='png')

        save_image = ImagePATH(
            makerid=maker_id,
            imagename=image_name,
            imagepath=save_path+image_name+".png"
        )
        image_repo.save_image(save_image)
        return save_image.imageid if save_image is not None else None

    def delete_image_by_name(self, image_name: str, image_repo: ImagePathRepository):
        try:
            rm_image = image_repo.get_image_by_image_name(image_name=image_name)
            image_path = rm_image.imagepath
            os.remove(f"{image_path}")
            image_repo.delete_image(rm_image.imageid)
        except OSError as e:
            print("Error while Delete! name : %s : %s" % (image_name, e.strerror))
            return

    def delete_image_by_id(self, image_id: int, image_repo: ImagePathRepository):
        try:
            rm_image = image_repo.get_image_by_id(image_id=image_id)
            image_path = rm_image.imagepath
            os.remove(f"{image_path}")
            image_repo.delete_image(rm_image.imageid)
        except OSError as e:
            print("Error while Delete! id : %s : %s" % (image_id, e.strerror))
            return
    """