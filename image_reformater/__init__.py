from pathlib import Path
from pillow_heif import register_heif_opener
from PIL import Image
import os
from datetime import datetime
from multiprocessing import Pool, cpu_count


class ImageReformater:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self):
        all_images = self._collect_images()
        if all_images:
            # Use multiprocessing Pool for parallel conversion
            with Pool(processes=cpu_count()) as pool:
                pool.starmap(_convert_image, [(image, self.output_dir) for image in all_images])
            
    def _collect_images(self):
        heic_files = list(self.input_dir.glob("*.heic"))
        heif_files = list(self.input_dir.glob("*.heif"))
        hif_files = list(self.input_dir.glob("*.hif"))
        return heic_files + heif_files + hif_files
            
            
def _convert_image(image: Path, output_dir: Path):
    register_heif_opener()  # Register HEIF/HEIC opener in each worker process
    image_name = image.stem
    try:
        exif_data = _extract_exif_data(image)
        
        with Image.open(image) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            output_path = output_dir / f"{image_name}.jpg"
            img.save(output_path, "JPEG", quality=95, optimize=True, exif=exif_data)
            
            current_time = datetime.now()
            _set_modification_time(output_path, current_time)
            
            print(f"Converted: {image.name} -> {image_name}.jpg (metadata preserved)")
    except Exception as e:
        print(f"Error converting {image.name}: {e}")
    
def _extract_exif_data(file_path: Path):
    """Extract EXIF data from the source image file."""
    try:
        with Image.open(file_path) as img:
            # Get EXIF data directly from PIL
            exif_dict = img.getexif()
            if exif_dict:
                # Convert to bytes for saving
                return exif_dict.tobytes()
        return None
    except Exception as e:
        print(f"Warning: Could not extract EXIF data from {file_path.name}: {e}")
        return None

def _set_modification_time(file_path: Path, modification_time: datetime):
    try:
        # Get current access time and set new modification time
        stat = file_path.stat()
        access_time = stat.st_atime
        modification_timestamp = modification_time.timestamp()
        os.utime(file_path, (access_time, modification_timestamp))
    except Exception as e:
        print(f"Warning: Could not set modification time for {file_path.name}: {e}")
