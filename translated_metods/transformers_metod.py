from transformers import pipeline

# Инициализируем модель M2M100
translator = pipeline("translation", model="facebook/m2m100_418M")

def translate_to_russian(text):
    # Указываем исходный и целевой язык
    result = translator(text, src_lang="en", tgt_lang="ru", max_length=400)
    return result[0]['translation_text']