# -*- coding: utf-8 -*-
try:
    import speech_recognition as sr
    import pyttsx3
    import urllib3
    import requests, json
except ImportError:
    input(f'Нажмите Enter для установки библиотек...')
    import os
    os.system('pip install SpeechRecognition==3.8.1')
    os.system('pip install requests')
    os.system('pip install pyttsx3')

client_id = 'твой айди'
client_token = 'токен на базу'

def gigachat_req(query: str):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload={
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': client_id,
        'Authorization': f'Basic {client_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    access_token = response.json()['access_token']

    url1 = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload1 = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False,
        "repetition_penalty": 1
    })
    headers1 = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response1 = requests.request("POST", url1, headers=headers1, data=payload1, verify=False)

    result = response1.json()['choices'][0]['message']['content']
    return result


# Инициализация рекордера для распознавания речи
recognizer = sr.Recognizer()

# Инициализация микрофона как источника аудио
mic = sr.Microphone()

def main():
    print(f'Добро пожаловать в голосового помощника от Флореста!\nГоворите в микрофон и Вам ответит искусственный интеллект.\nПопробуйте!\nСкажите: "хватит" для отключения.')
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Запись аудио и его преобразование в текст
            audio = recognizer.listen(source, 5)
            try:
                # Распознавание текста
                text = recognizer.recognize_google(audio, language='ru-RU')
                if text.lower() != 'хватит':
                    print(f"Вы сказали: {text}")

                    # Создание ответа от GigaChat
                    res = gigachat_req(text)
                    print(f'Ответ от FlorestAI: {res}')

                    # Преобразование текста ответа в аудио
                    engine = pyttsx3.Engine()
                    engine.say(res)
                    engine.runAndWait()
                else:
                    print(f'ОК. До свидания!')
                    break
            except sr.UnknownValueError:
                print("Google Speech Recognition не смог понять аудио.")
            except sr.RequestError as e:
                print(f"Не удалось обратиться к Google Speech Recognition API: {e}")

main()
