from io import BytesIO
import aiohttp
from aiogram import types


async def upload_photo(photo: types.photo_size.PhotoSize) -> str:
    async with aiohttp.ClientSession() as session:
        with await photo.download(destination_file=BytesIO()) as file:
            form = aiohttp.FormData()
            form.add_field(
                name='file',
                value=file,
            )
            async with session.post('https://telegra.ph/upload', data=form) as response:
                img_src = await response.json()

    link = 'http://telegra.ph/' + img_src[0]["src"]
    return link
