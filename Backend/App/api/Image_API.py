
"""
    file : App.API.Image_API.py
    writer : Meohong
    first date : 2024-03-17
    Objective : Image API ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-03-16 |   1   |   first write
     2024-03-17 |   2   |   modify and improve code
     2024-03-17 |   3   |   Classization,  Optimize
     2024-03-24 |   4   |   Function Modify, Optimize
    ========================================================================
"""
import json
import requests
import base64
import io
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from App.Security.config import WebUISetting
from App.Service.Image_Service import ImageService
from App.Service.user_Service import UserService
from App.database.repository import UserRepository
from App.api.user_API import oauth2_scheme


webui_setting = WebUISetting()

app = APIRouter(
    prefix="/webui",
)

image_service = Annotated[ImageService, Depends()]
user_service = Annotated[UserService, Depends()]
user_repository = Annotated[UserRepository, Depends()]

@app.post("/txt2img")
async def text2image(
        image_serv: image_service,
        user_serv: user_service,
        input_prompt: str,
        login_token: Annotated[str, Depends(oauth2_scheme)]
):
    webui_set = image_serv.webui_setting
    payload = {
        "prompt": webui_set.POSITIVE_PROMPT + input_prompt,
        "negative_prompt": webui_set.NEGATIVE_PROMPT,
        "steps": 50,
        "batch_size": 4,
    }
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Logined")

    # 프롬프트에 맞게 생산
    images = image_serv.generate_image(payload=payload)
    if not images:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image not Generate")

    # 이미지 람다 변환 후 리스트 저장
    image_list = list(map(lambda x: image_serv.decode_image(x), images))

    # 결과 출력 확인
    # for image in image_list:
    #    image.show()
    return JSONResponse(images)
    # return images

"""
# 이미지를 저장하는 API
# 로그인이 되어있어야 가능
# 현재 사용하지 않는 기능이다.
@app.post("/saveimage")
async def save_image(
        image_serv: image_service,
        image_repo: image_repository,
        user_serv: user_service,
        user_repo: user_repository,
        save_wanted,
        image_name: str,
        login_token: Annotated[str, Depends(oauth2_scheme)]
):
    webui_set = image_serv.webui_setting
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id
        image_serv.save_image(image_base64=save_wanted, maker_id=user_id, image_name=image_name, image_repo=image_repo)
    except save_wanted is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="save_image is None ")
    except login_token is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="login_token is None ")

# 이미지 삭제 API
# 스토리지에 저장된 이미지와 DB를 삭제
@app.delete("/deleteimage")
async def delete_image(
        image_serv: image_service,
        image_repo: image_repository,
        image_name: str,
        login_token: Annotated[str, Depends(oauth2_scheme)],
        user_serv: user_service,
        user_repo: user_repository,
):
    try:
        # 먼저, 토큰에 담긴 이메일을 얻어, 고객의ID(고유번호)를 얻음.
        maker_email = user_serv.decode_access_token(access_token=login_token)
        maker_id = user_serv.get_user(email=maker_email, user_repo=user_repo)
        if maker_id is None:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="login_token is None")

        # 이미지를 찾아옴. 기준은 이미지를 저장할 때 생성한 이름으로 찾는다.
        wanted_image = image_serv.get_image_by_name(image_name=image_name, image_repo=image_repo)

        # 만약, 이미지 DB에 들어있는 makerid와 현재 로그인 된 사람과 다르다면?
        if wanted_image.makerid != maker_id:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="makerid is not correct")
        image_serv.delete_image_by_id(image_id=wanted_image.imageid, image_repo=image_repo)
        return HTTPException(status_code=status.HTTP_200_OK, detail="Delete Completely")
    except image_name is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="image_name is None")

# 그 아이디가 만든 이미지들을 보여줄려고한다.
#    따라서, 이미지를 전부 불러온다

@app.get("/showimages")
async def showimages(
        user_serv: user_service,
        user_repo: user_repository,
        image_serv: image_service,
        image_repo: image_repository,
        access_token: Annotated[str, Depends(oauth2_scheme)],
):
    maker_email = user_serv.decode_access_token(access_token=access_token)
    maker_id = user_serv.get_user(email=maker_email, user_repo=user_repo).id
    if maker_id is None:
        return HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="Not Login")
    images = image_serv.show_images(user_id=maker_id, image_repo=image_repo)
    if images is None or len(images) == 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There's No Images")
    return images
"""