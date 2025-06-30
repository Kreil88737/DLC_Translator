import os
import zipfile
import tempfile
import shutil


def add_ru_langs_to_zip(original_zip, extracted_langs_dir, output_zip):
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Распаковываем оригинальный архив во временную папку
        with zipfile.ZipFile(original_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 2. Копируем переведённые ru_RU.lang поверх существующих или добавляем новые
        for root, dirs, files in os.walk(extracted_langs_dir):
            if "en_US.lang" in files:
                en_path = os.path.join(root, "en_US.lang")
                relative_path = os.path.relpath(root, extracted_langs_dir)
                target_dir = os.path.join(temp_dir, relative_path)
                ru_path = os.path.join(target_dir, "ru_RU.lang")

                print(f"Добавляю/Заменяю: {ru_path}")
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy(en_path, ru_path)  # Предполагается, что вы уже изменили содержимое файла

        # 3. Упаковываем всё обратно в новый ZIP
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    new_zip.write(file_path, arcname)

        print(f"Готово! Обновлённый архив сохранён как: {output_zip}")