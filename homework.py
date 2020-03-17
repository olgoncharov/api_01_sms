import os
import time
from dotenv import load_dotenv
import requests
from twilio.rest import Client


load_dotenv()


TWILIO_SID = os.getenv('twilio_sid')
TWILIO_TOKEN = os.getenv('twilio_token')
NUMBER_FROM = os.getenv('number_from')
NUMBER_TO = os.getenv('number_to')
VK_TOKEN = os.getenv('vk_token')
VK_API_VER = '5.92'


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'access_token': VK_TOKEN,
        'v': VK_API_VER,
    }
    try:
        response = requests.post('https://api.vk.com/method/users.get', params=params)
        #response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Ошибка при вызове метода users.get', err, sep='\n')
        return None
    except requests.exceptions.RequestException as err:
        print('Ошибка подключения', err, sep='\n')

    user = response.json().get('response')[0]
    return user['online']


def sms_sender(sms_text):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(to=NUMBER_TO, from_=NUMBER_FROM, body=sms_text) 
    return message.sid


if __name__ == "__main__":
    vk_id = input("210700286")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
