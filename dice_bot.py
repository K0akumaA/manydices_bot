import telebot
import random
import os

TOKEN = '8905864437:AAHsmIv4z24OqdUoVQCK3fAYeesiALDdgYs'
bot = telebot.TeleBot(TOKEN)


# === Вспомогательная функция для броска кубиков ===
def roll_dice(message, sides, dice_name, emoji):
    """Универсальная функция броска кубиков."""
    parts = message.text.split()
    num_dice = 1

    # Если пользователь указал количество (например, /roll20 3)
    if len(parts) > 1:
        try:
            num_dice = int(parts[1])
            if num_dice > 20:
                num_dice = 20
                bot.reply_to(message, "⚠️ Слишком много кубиков! Бросаю максимум 20.")
        except ValueError:
            bot.reply_to(message, " Пожалуйста, укажи число кубиков (например, /roll20 3).")
            return

    # Бросаем кубики
    results = [random.randint(1, sides) for _ in range(num_dice)]
    total_sum = sum(results)

    # Формируем красивое сообщение
    if num_dice == 1:
        result_text = f"{emoji} **{dice_name}**: выпало **{results[0]}**"
    else:
        rolls_str = ", ".join(map(str, results))
        result_text = (
            f"{emoji} **{dice_name}** ({num_dice} шт.):\n"
            f"🎲 Броски: {rolls_str}\n"
            f"📊 Сумма: **{total_sum}**"
        )

    bot.reply_to(message, result_text, parse_mode='Markdown')


# === Команды приветствия ===
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "🎲 **Бот для настольных игр**\n\n"
        "**Кубики:**\n"
        "/roll — бросить d6 (по умолчанию)\n"
        "/roll4 — бросить d4 🔺\n"
        "/roll6 — бросить d6 🎲\n"
        "/roll10 — бросить d10 🔟\n"
        "/roll12 — бросить d12 🔷\n"
        "/roll20 — бросить d20 ⭐\n"
        "/roll100 — бросить d100 💯\n\n"
        "**Монетка:**\n"
        "/coin — подбросить монетку 🪙\n\n"
        "💡 Можно указать количество кубиков:\n"
        "/roll20 3 — бросить три d20"
    )
    bot.reply_to(message, help_text, parse_mode='Markdown')


# === Обычный /roll (по умолчанию d6) ===
@bot.message_handler(commands=['roll'])
def roll_default(message):
    roll_dice(message, 6, "d6", "🎲")


# === Команды для разных кубиков ===
@bot.message_handler(commands=['roll4'])
def roll_d4(message):
    roll_dice(message, 4, "d4", "🔺")


@bot.message_handler(commands=['roll6'])
def roll_d6(message):
    roll_dice(message, 6, "d6", "")


@bot.message_handler(commands=['roll10'])
def roll_d10(message):
    roll_dice(message, 10, "d10", "🔟")


@bot.message_handler(commands=['roll12'])
def roll_d12(message):
    roll_dice(message, 12, "d12", "🔷")


@bot.message_handler(commands=['roll20'])
def roll_d20(message):
    roll_dice(message, 20, "d20", "⭐")


@bot.message_handler(commands=['roll100'])
def roll_d100(message):
    roll_dice(message, 100, "d100", "💯")


# === Монетка ===
@bot.message_handler(commands=['coin'])
def flip_coin(message):
    sides = ['Орёл ', 'Решка 👑']
    result = random.choice(sides)
    bot.reply_to(message, f"🪙 Монетка подброшена...\n\n✨ Выпало: **{result}**", parse_mode='Markdown')


# === Запуск бота ===
if __name__ == '__main__':
    print(" Бот запущен и ждёт команд...")
    bot.infinity_polling()