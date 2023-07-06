import psutil, requests, asyncio
from config import *
from message import *

battery_info_messages = {
    100: 'battery is fully charged.',
    75: 'battery is at 75%.',
    'unplugged': 'battery is not connected to a power source.',
    'plugged': 'battery is now charging.'
}

battery_warning_messages = {
    50: 'battery is at 50%.',
    25: 'battery is at 25%.',
    20: 'battery is at 20%.'
}

def send_telegram_message(message: Message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": f"{str(message)}",
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=params)
    return response.status_code == 200

async def check_battery():
    previous_power_plugged = True
    previous_percentage = 100

    while True:
        battery = psutil.sensors_battery()
        power_plugged = battery.power_plugged
        status_key = 'plugged' if power_plugged else 'unplugged'
        percentage = battery.percent

        if power_plugged != previous_power_plugged:
            message_to_send = battery_info_messages.get(status_key)
            if message_to_send:
                send_telegram_message(Message(message_to_send, MessageType.INFO))
                previous_power_plugged = power_plugged
        elif percentage != previous_percentage:
            if percentage in battery_info_messages:
                message_to_send = battery_info_messages[percentage]
                send_telegram_message(Message(message_to_send, MessageType.INFO))
            elif percentage in battery_warning_messages:
                message_to_send = battery_warning_messages[percentage]
                send_telegram_message(Message(message_to_send, MessageType.WARNING))
            previous_percentage = percentage

        await asyncio.sleep(60)

async def main():
    await check_battery()

if __name__ == "__main__":
    asyncio.run(main())