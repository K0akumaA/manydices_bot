import telebot
import random

# Вставь сюда токен, который выдал @BotFather
TOKEN = '8905864437:AAHsmIv4z24OqdUoVQCK3fAYeesiALDdgYs'
bot = telebot.TeleBot(TOKEN)

# Обработка команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
        "Привет! 🎲 Я бот для игры в кости.\n"
        "Напиши /roll, чтобы бросить один шестигранный кубик.\n"
        "Или напиши /roll 3, чтобы бросить сразу три кубика!")

# Обработка команды /roll
@bot.message_handler(commands=['roll'])
def roll_dice(message):
    # Разделяем команду на части, чтобы проверить, есть ли аргумент (количество кубиков)
    parts = message.text.split()
    
    # По умолчанию бросаем 1 кубик
    num_dice = 1 
    
    # Если пользователь указал число (например, /roll 3)
    if len(parts) > 1:
        try:
            num_dice = int(parts[1])
            if num_dice > 10: # Ограничим максимум, чтобы не спамить
                num_dice = 10
                bot.reply_to(message, "Слишком много кубиков! Бросаю максимум 10.")
        except ValueError:
            bot.reply_to(message, "Пожалуйста, укажи число кубиков (например, /roll 3).")
            return

    # Бросаем кубики
    results = [random.randint(1, 6) for _ in range(num_dice)]
    total_sum = sum(results)
    
    # Формируем красивое сообщение
    if num_dice == 1:
        result_text = f"🎲 Вам выпало: {results[0]}"
    else:
        result_text = f"🎲 Ваши кубики: {', '.join(map(str, results))}\n📊 Сумма: {total_sum}"
        
    bot.reply_to(message, result_text)

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен и ждет команд...")
    bot.infinity_polling()