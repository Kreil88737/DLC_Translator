from translated_metods.google_unoficial import trans_google_trans_unofficial
from translated_metods.GPT_api import translate_api
import os
import asyncio
import concurrent.futures
from pars_lang.extarct import extract_en_us_langs
from pars_lang.save import add_ru_langs_to_zip
from pars_lang.found import find_en_us_lang_files
from pars_lang.patch_laungages_json import patch

def metod():
    show_error = False
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана
        print('Выберите способ перевода:')
        print('1 - Google_translator')
        print('2 - Transformers_local')
        print('3 - Chat_GPT_api')

        if show_error:
            print('\nНеверный выбор. Попробуйте снова.')  # Сообщение об ошибке
            show_error = False  # Сброс флага после вывода

        choice = input('> ')
        if choice in {"1", "2", "3"}:
            return choice
        else:
            show_error = True  # Установка флага ошибки для следующей итерации

# Получение выбора пользователя
m = metod()

# Обработка выбора
if m == "1":
    print('\nВыбран способ перевода - Google_translator')
elif m == "2":
    print('\nВыбран способ перевода - Transformers_local')
elif m == "3":
    print('\nВыбран способ перевода - Chat_GPT_api')

file = input('введите путь к файлу> ')

extract_en_us_langs(file, 'translating')

def translate_lang_file_Google(input_path, output_path, max_workers=20):
    """
    Переводит значения в lang-файле с использованием многопоточности.
    Сохраняет структуру, комментарии и порядок строк.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {input_path} не найден.")
        return

    translated_lines = [''] * len(lines)

    # Заполняем уже известные строки (комментарии, пустые, без '=')
    tasks = []

    for idx, line in enumerate(lines):
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('#'):
            translated_lines[idx] = line
        elif '=' in line:
            equal_index = line.find('=')
            key_part = line[:equal_index + 1].rstrip('\n')
            value_part = line[equal_index + 1:].strip()
            tasks.append((idx, key_part, value_part))
        else:
            translated_lines[idx] = line

    # Параллельный перевод с помощью ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(trans_google_trans_unofficial, value_part): (idx, key_part)
            for idx, key_part, value_part in tasks
        }

        for future in concurrent.futures.as_completed(future_to_task):
            idx, key_part = future_to_task[future]
            try:
                translated_value = future.result()
                translated_lines[idx] = f"{key_part}{translated_value}\n"
            except Exception as e:
                print(f"Ошибка перевода для строки {idx}: {e}")
                translated_lines[idx] = f"{key_part}{value_part}\n"  # Возвращаем оригинал при ошибке

    # Записываем результат в выходной файл
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

    print(f"Файл {output_path} успешно обработан.")

def translate_lang_file_Chat_GPT(input_path, output_path, max_workers=20):
    """
    Переводит значения в lang-файле с использованием многопоточности.
    Сохраняет структуру, комментарии и порядок строк.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {input_path} не найден.")
        return

    translated_lines = [''] * len(lines)

    # Заполняем уже известные строки (комментарии, пустые, без '=')
    tasks = []

    for idx, line in enumerate(lines):
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('#'):
            translated_lines[idx] = line
        elif '=' in line:
            equal_index = line.find('=')
            key_part = line[:equal_index + 1].rstrip('\n')
            value_part = line[equal_index + 1:].strip()
            tasks.append((idx, key_part, value_part))
        else:
            translated_lines[idx] = line

    # Параллельный перевод с помощью ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(translate_api, value_part): (idx, key_part)
            for idx, key_part, value_part in tasks
        }

        for future in concurrent.futures.as_completed(future_to_task):
            idx, key_part = future_to_task[future]
            try:
                translated_value = future.result()
                translated_lines[idx] = f"{key_part}{translated_value}\n"
            except Exception as e:
                print(f"Ошибка перевода для строки {idx}: {e}")
                translated_lines[idx] = f"{key_part}{value_part}\n"  # Возвращаем оригинал при ошибке

    # Записываем результат в выходной файл
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

    print(f"Файл {output_path} успешно обработан.")

def translate_lang_file_Transformers_local(input_path, output_path, max_workers=20):
    from translated_metods.transformers_metod import translate_to_russian
    """
    Переводит значения в lang-файле с использованием многопоточности.
    Сохраняет структуру, комментарии и порядок строк.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {input_path} не найден.")
        return

    translated_lines = [''] * len(lines)

    # Заполняем уже известные строки (комментарии, пустые, без '=')
    tasks = []

    for idx, line in enumerate(lines):
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('#'):
            translated_lines[idx] = line
        elif '=' in line:
            equal_index = line.find('=')
            key_part = line[:equal_index + 1].rstrip('\n')
            value_part = line[equal_index + 1:].strip()
            tasks.append((idx, key_part, value_part))
        else:
            translated_lines[idx] = line

    # Параллельный перевод с помощью ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(translate_to_russian, value_part): (idx, key_part)
            for idx, key_part, value_part in tasks
        }

        for future in concurrent.futures.as_completed(future_to_task):
            idx, key_part = future_to_task[future]
            try:
                translated_value = future.result()
                translated_lines[idx] = f"{key_part}{translated_value}\n"
            except Exception as e:
                print(f"Ошибка перевода для строки {idx}: {e}")
                translated_lines[idx] = f"{key_part}{value_part}\n"  # Возвращаем оригинал при ошибке

    # Записываем результат в выходной файл
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

    print(f"Файл {output_path} успешно обработан.")

langs = find_en_us_lang_files('translating')

print(langs)

if m == "1":
    for lang in langs:
        translate_lang_file_Google(lang, lang, 50)
elif m == "2":
    for lang in langs:
        translate_lang_file_Transformers_local(lang, lang, 50)
elif m == "3":
    for lang in langs:
        translate_lang_file_Chat_GPT(lang, lang, 50)

add_ru_langs_to_zip(file, 'translating', file)

patch(file)

print('СКРИПТ ЗАВЕРШИЛ РАБОТУ' + ' УСПЕШНО ПЕРЕВЕДЕННО ' + file)