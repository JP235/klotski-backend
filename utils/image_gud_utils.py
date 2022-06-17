import os
import base64
import random
import string
import pathlib
from django.core.files.base import ContentFile

from .constants import IMG_CURR, IMG_CURR_PATH, IMG_WIN, IMG_WIN_PATH


def file_path_curr(instance, filename) -> str:
    fpath = pathlib.Path(filename)
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return f'{IMG_CURR_PATH}{instance.code}-{randname}{fpath.suffix}'

def file_path_win(instance, filename) -> str:
    fpath = pathlib.Path(filename)
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return f'{IMG_WIN_PATH}{instance.code}-{randname}{fpath.suffix}'


def get_ContentFile_from_b64_image(b64str):
    """
    Returns a ContentFile from a base64 encoded string image
    got help from https://stackoverflow.com/a/39587386/15088227
    """
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    try:
        format, imgstr = b64str.split(';base64,') 
        ext = format.split('/')[-1] 
        return ContentFile(base64.b64decode(imgstr), name=f'{randname}.' + ext)
    except AttributeError:
        print("Error: b64str is not a string")
        return None

def update_game_img(sender, **kwargs) -> None:
    """
    Deletes the old image from the filesystem
    """
    
    instance = kwargs["instance"]

    if not hasattr(instance , "id") or isinstance(instance.id, type(None)):
        return

    try:
        old_img_curr = instance.__class__.objects.get(id=instance.id).img_curr.path
        if os.path.exists(old_img_curr):
            os.remove(old_img_curr)
    except ValueError :
        pass

def delete_game_img(sender, **kwargs) -> None:
    """
    Deletes the image from the filesystem
    # https://techincent.com/how-to-delete-file-when-models-instance-is-delete-or-update-in-django/
    """
    
    instance = kwargs["instance"]
    if hasattr(instance, IMG_CURR):
        instance.img_curr.delete(save=False)

    if hasattr(instance, IMG_WIN):       
        instance.img_win.delete(save=False)

