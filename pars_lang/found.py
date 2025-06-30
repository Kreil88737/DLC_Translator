import os

def find_en_us_lang_files(start_folder):
    found_files = []
    for root, dirs, files in os.walk(start_folder):
        for file in files:
            if file == "en_US.lang":
                full_path = os.path.join(root, file)
                found_files.append(full_path)
    return found_files