import os
import zipfile

def extract_en_us_langs(zip_path, output_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('en_US.lang'):
                print(f"Извлекаю: {file_info.filename}")
                zip_ref.extract(file_info, output_folder)