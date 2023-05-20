from bot import bot
import time, pytz, secrets
from datetime import datetime
from weather import getweather

print('Scheduler Running')


def job():
    time_now = datetime.now(pytz.timezone('Asia/Dhaka'))
    h, m = time_now.hour, time_now.minute
    if h == 6 and m == 0:
        bot.send_message(1467252650, secrets.choice(['Good Morning💙', 'Shuvo sokal jaan😘💙', 'Shuvo sokal🥰']))
    elif h == 17 and m == 0:
        bot.send_message(1467252650, secrets.choice(['Good Afternoon💙', 'Shuvo Bikel babu😘💙', 'Shuvo bikal🥰']))
    elif h == 19 and m == 0:
        bot.send_message(1467252650, secrets.choice(['Good Evening💙', 'Shuvo Sondha babuta😘💙', 'Shuvo Sondha🥰']))
    

def runner():
    while True:
        job()
        time.sleep(60)
