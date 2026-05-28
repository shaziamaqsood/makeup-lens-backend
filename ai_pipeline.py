import cv2
import numpy as np
from gfpgan import GFPGANer

restorer = GFPGANer(
    model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
    upscale=2,
    arch='clean',
    channel_multiplier=2
)

def enhance(image):
    _, _, restored = restorer.enhance(image, has_aligned=False, only_center_face=False)
    return restored