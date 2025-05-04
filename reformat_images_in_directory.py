import argparse
from image_reformater import ImageReformater
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description='Convert HEIC images to JPG format')
    parser.add_argument('input_dir', type=str, help='Input directory containing HEIC images')
    parser.add_argument('output_dir', type=str, help='Output directory for JPG images')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory '{input_path}' does not exist")
        sys.exit(1)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    reformater = ImageReformater(input_path, output_path)
    reformater.run()

if __name__ == "__main__":
    main()