import os
import telebot
import speech_recognition
import urllib
from pydub import AudioSegment


# Ниже нужно вставить токен, который дал BotFather при регистрации
# Пример: token = '2007628239:AAEF4ZVqLiRKG7j49EC4vaRwXjJ6DN6xng8'
token = '6412519167:AAF7XO3aInv3v7pOFgCQXI80Q9RgzqBxXS0'  # <<< Ваш токен

bot = telebot.TeleBot(token)


def oga2wav(filename):
    # Конвертация формата файлов
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


# def recognize_speech(oga_filename):
#     # Перевод голоса в текст + удаление использованных файлов
#     wav_filename = oga2wav(oga_filename)
#     recognizer = speech_recognition.Recognizer()

#     with speech_recognition.WavFile(wav_filename) as source:     
#         wav_audio = recognizer.record(source)

#     text = recognizer.recognize_google(wav_audio, language='ru')

#     if os.path.exists(oga_filename):
#         os.remove(oga_filename)

#     if os.path.exists(wav_filename):
#         os.remove(wav_filename)

#     return text



# Код с проверкой - если речь не была распознана бот вернет ошибку
def recognize_speech(oga_filename):
    # Перевод голоса в текст + удаление использованных файлов
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(wav_audio, language='ru')
    except speech_recognition.UnknownValueError:
        text = "Речь не была распознана."

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text

def download_file(bot, file_id):
    # Скачивание файла, который прислал пользователь
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    bot.send_message(message.chat.id, 'Привет, ' + message.chat.first_name)
    sticker = open('skillbox_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    sticker.close()


# @bot.message_handler(content_types=['voice'])
# def transcript(message):
#     # Функция, отправляющая текст в ответ на голосовое
#     filename = download_file(bot, message.voice.file_id)
#     text = recognize_speech(filename)
#     bot.send_message(message.chat.id, text)


# код с учетом того, что сервер может не отвечать
@bot.message_handler(content_types=['voice'])
def transcript(message):
    try:
        # Функция, отправляющая текст в ответ на голосовое
        filename = download_file(bot, message.voice.file_id)
        text = recognize_speech(filename)
        bot.send_message(message.chat.id, text)
    except Exception as e:
        error_message = "Произошла ошибка при обработке вашего голосового сообщения. Пожалуйста, попробуйте ещё раз позже."
        bot.send_message(message.chat.id, error_message)


# Запускаем бота. Он будет работать до тех пор, пока работает ячейка (крутится значок слева).
# Остановим ячейку - остановится бот
bot.polling()