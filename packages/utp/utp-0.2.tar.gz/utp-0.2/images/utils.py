

import cv2 as cv
from pathlib import Path
from typing import Union


def read_image(path: Union[str, Path]):
    return cv.imread(path)
