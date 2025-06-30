import asyncio
from googletrans import Translator

async def translate_to_russian(text):
    translator = Translator()
    translation = await translator.translate(text, dest='ru')
    return translation.text

def trans_google_trans_unofficial(text):
    # Используем asyncio.run() для запуска асинхронной функции
    return asyncio.run(translate_to_russian(text))