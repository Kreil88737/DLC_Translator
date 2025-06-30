import requests

api_key = 'sk-OXAFyyGFefu59hgJG0Y41FER5lv3lNuwqUMWlSHmlJfMoT3DCkXUvBJmFwKp'

def translate_api(text):
    json_data = {
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': 'Переведи на русский. Если есть § и буква после — оставь их как есть. Если текст не переводиться, верни его без изменений. Никаких комментариев.: ' + text ,
                    },
                ],
            },
        ],
        'is_sync': True,
        'model': 'gpt-4.1-nano',
        'n': 1,
        'max_tokens': 4096,
        'temperature': 1,
        'top_p': 1,
        'response_format': '{"type":"text"}',
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    url_endpoint = "https://api.gen-api.ru/api/v1/networks/gpt-4-1"
    response = requests.post(url_endpoint, json=json_data, headers=headers)
    json= response.json()
    text2 = json['response'][0]['message']['content']
    print('Chat_gpt: ' + text, '-', text2)
    return text2

translate_api("@")