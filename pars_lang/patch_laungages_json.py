import zipfile
import json
import os
import shutil
import tempfile

def patch(archive_path):
    # Проверяем, существует ли архив
    if not os.path.isfile(archive_path):
        print(f"[Ошибка] Файл '{archive_path}' не найден.")
        return

    # Определяем имя архива без расширения и формируем имя выходного файла
    base_name, ext = os.path.splitext(archive_path)
    temp_dir = tempfile.mkdtemp()
    extract_folder = os.path.join(temp_dir, "extracted")
    new_archive_path ="translated" + ext

    try:
        # Распаковываем архив
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        # Ищем все файлы languages.json
        for root, dirs, files in os.walk(extract_folder):
            for file in files:
                if file == "languages.json":
                    file_path = os.path.join(root, file)
                    print(f"[Найден] {file_path}")

                    # Читаем JSON
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            print(f"[Ошибка] Не удалось разобрать JSON в файле: {file_path}")
                            continue

                    # Обновляем только если это массив строк
                    if isinstance(data, list):
                        if "ru_RU" not in data:
                            data.append("ru_RU")
                            print(f"[Добавлено] ru_RU в {file_path}")
                        else:
                            print(f"[Уже есть] ru_RU в {file_path}")

                        # Сохраняем обновлённый JSON
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                    else:
                        print(f"[Пропущено] Формат данных в {file_path} не поддерживается (не массив).")

        # Упаковываем обратно в архив
        print(f"[Сохранение] Новый архив создаётся: {new_archive_path}")
        relroot = os.path.abspath(extract_folder)
        with zipfile.ZipFile(new_archive_path, "w", zipfile.ZIP_DEFLATED) as zipout:
            for root, dirs, files in os.walk(extract_folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, relroot)
                    zipout.write(filepath, relpath)

        print("[Готово] Обработка завершена.")

    finally:
        # Удаляем временную папку
        shutil.rmtree(temp_dir)