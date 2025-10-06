import asyncio
import json
from telethon import TelegramClient, events

# Загружаем конфиг
with open('config.json', 'r') as f:
    config = json.load(f)

async def start_user_bot(user_data, user_name):
    try:
        client = TelegramClient(f'session_{user_name}', user_data['api_id'], user_data['api_hash'])
        
        await client.start(phone=user_data['phone'])
        print(f"✅ {user_name} подключен! Номер: {user_data['phone']}")
        
        @client.on(events.NewMessage)
        async def handler(event):
            if event.message.sender_id == (await client.get_me()).id:
                text = event.message.text
                
                if text.startswith('/sp1'):
                    try:
                        parts = text.split()
                        count = int(parts[1])
                        spam_text = ' '.join(parts[2:])
                        
                        await event.message.delete()
                        print(f"🎯 {user_name}: спам {count} раз '{spam_text}'")
                        
                        for i in range(count):
                            await client.send_message(event.chat_id, spam_text)
                            if i < count - 1:
                                await asyncio.sleep(0.12)
                        
                        print(f"✅ {user_name}: спам завершен")
                        
                    except Exception as e:
                        print(f"❌ {user_name}: ошибка - {e}")
                
                elif text.startswith('/sp2'):
                    try:
                        parts = text.split()
                        count = int(parts[1])
                        words = parts[2:]
                        
                        await event.message.delete()
                        print(f"🎯 {user_name}: спам словами {count} циклов")
                        
                        for cycle in range(count):
                            for i, word in enumerate(words):
                                await client.send_message(event.chat_id, word)
                                if not (cycle == count - 1 and i == len(words) - 1):
                                    await asyncio.sleep(0.12)
                        
                        print(f"✅ {user_name}: спам завершен")
                        
                    except Exception as e:
                        print(f"❌ {user_name}: ошибка - {e}")
        
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"❌ Ошибка подключения {user_name}: {e}")

async def main():
    print("🚀 Запуск мульти-бота для 2 пользователей...")
    tasks = []
    for user_name, user_data in config['users'].items():
        task = asyncio.create_task(start_user_bot(user_data, user_name))
        tasks.append(task)
    
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())