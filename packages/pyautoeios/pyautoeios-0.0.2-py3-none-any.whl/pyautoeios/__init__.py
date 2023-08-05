from typing import List
from pyautoeios import eios
from pyautoeios import hexcodes
from pyautoeios import _pyscreeze_remoteinput_patch
from pyautoeios import _pyautogui_remoteinput_patch

import pyscreeze
import pyautogui
pyautogui.platformModule = _pyautogui_remoteinput_patch
pyscreeze.screenshot = _pyscreeze_remoteinput_patch._screenshot_remoteinput

if pyscreeze.useOpenCV:
    from pyautoeios import _pyscreeze_cv2_patch
    pyscreeze._load_cv2 = _pyscreeze_cv2_patch._load_cv2
    pyscreeze._extract_alpha_cv2 = _pyscreeze_cv2_patch._extract_alpha_cv2
    pyscreeze._locateAll_opencv = _pyscreeze_cv2_patch._locateAll_opencv

# Now that things have been patched, import it all 
# into the pyautoeios namespace
from pyautogui import *


clients = []

def inject_clients() -> List[eios.EIOS]:
    try:
        while True:
            clients.append(eios.EIOS())
    except OSError:
        if len(clients) < 1:
            raise

def pair_client(eios_obj: eios.EIOS):
    _pyautogui_remoteinput_patch.eios_obj = eios_obj
    _pyscreeze_remoteinput_patch.eios_obj = eios_obj

__AUTHOR__ = "brett.moan@gmail.com"
__VERSION__ = "0.0.2"
