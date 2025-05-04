from pathlib import Path
from pillow_heif import register_heif_opener
from PIL import Image
import numpy as np
import cv2
import pillow_heif





class ImageReformater:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self):
        register_heif_opener()  # Register HEIF/HEIC opener for Pillow
        for file in self.input_dir.glob("*.heic"):
            file_name = file.stem
            heif_file = pillow_heif.open_heif(str(file), convert_hdr_to_8bit=False, bgr_mode=True)
            np_array = np.asarray(heif_file)
            cv2.imwrite(str(self.output_dir / f"{file_name}.png"), np_array)
