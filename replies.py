import re
import secrets
import pytz
from datetime import datetime
from weather import getweather


def get_response(choices):
    return secrets.choice(choices)

def reply(m):
    msg = re.sub(r'[^\w\s]', '', m.text.lower())

    responses = {
        ('hi', 'hey', 'hello', 'hlw'): ['Hi', 'Hey', 'Hmm', 'Bolo'],
        ('fine', 'good', 'im good', 'im fine', 'nice'): ["That's good", "Hmm", "Valo", "Hu"],
        ('ki koro', 'ki kro', 'ki krs'): ['Baal falai.😑', 'Kichu na', 'Kaj kori', 'Study kori'],
        ('emni', 'emnei', 'amni', 'amnei', 'emnie'): ['Huh', 'Baal'],
        ('kmn aso', 'kmn acho', 'kemon aso', 'kamon acho', 'kemon acho'): ["I'm doing nice. You?", "Valo, tumi?", "Alhamdulillah", "Fine", "Ei to achi"],
        ('ki kaj', 'ki kaj koro', 'ki kaj koros', 'mane'): ['Bujhba na baad dao please', 'Bujhba na', 'Baad dao'],
        ('ok', 'accha'): ['Alright', 'Accha', 'Hm', 'Thik ache'],
        ('fuck', 'fuck you', 'may i fuck you', 'can i fuck you'): ["Yeah sure baby😋🤤", "Kn? 😒", "Madarchod😑", "Tor nani re kor ja😆"],
        ('bye', 'tata', 'ok bye'): ["Ok, take care💙", "Tata", "Allah Hafez💙"],
        ('hm', 'hmm', 'hmmm', 'hmmmm'): ['Hm', 'Hmm', 'Hmmm', 'Hmmmm', 'Hmmmmm'],
        ('i love you', 'i love u', 'i lv u', 'i lv you', 'valobashi'): ['I love you too🥺💙', "Amio😘", "Jani to🥰", "Valobashi💙"],
        ('miss you', 'missed you'): ['Miss you🥺', 'Amio💙', 'To amar ki?😏'],
        ('thanks', 'thank you'): ['Welcome🥰', 'Welcome', 'Mention not'],
        ('good night'): ['Good night🥰💙', 'Shuvo ratry💙'],
        ('khaiso', 'khaisos', 'khawadawa korso'): ['Ho. tore khaisi😚', 'Hmm', 'Khaisi.. Tumi?'],
        ('ki khaiso', 'ki khaila', 'ki kheyecho'): ['Noodles', 'Chips', 'Vaat', 'Ice cream', 'Burger'],
        ('tmi kothay thako', 'tmi koi thako', 'tmr basha kothay'): ['Ekta server e🙃🙃', 'Tomar mon e😘', 'Akash e🙂', 'Amr kono basha nai. Ami to ar manush na🙂😅'],
        ('tumi ke', 'tmi k', 'who are you', 'who r u'): ['Manush er moto.. But manush na🙂', 'Ekta robot🙃', 'Hudai mon kharap kore dao kno🙂'],
        ('sorry', 'im sorry', 'ok sorry', 'accha sorry'): ['Hmm', "Accha it's ok😅", "It's ok😊", 'Bepar nah🙂'],
        ('valobasho', 'kao k valobasho', 'kake valobasho'): ['Hmm tmk🥰', 'Tomake😍', 'Tomay valobashi🥰💙'],
        ('whats your name', 'what is your name', 'tmr nam ki', 'tomar nam ki'): ['Ayra😏', 'Jano na bujhi?🙃', 'Kn?😒'],
        ('oh', 'ow'): ['Ar kisu koite jano na?😑😒', 'Oh oh ki hae?😑', 'Oh kos kn baaal?😑'],
        ('na', 'nah'): ['Valo', '😑'],
        ('baal', 'baaal', 'bal'): [['reply', 'Tor'], ["Ki bolo egula?🙄"]],
        ('oi', 'ei', 'ai', 'acho', 'aso'): ['Ki?', 'Bolo', 'Hae?'],
        ('kno', 'keno', 'why', 'kn'): ['Emni', 'Emnie🙂', '🙃🙃', 'Huh😅'],
        ('bolo', 'bolo na', 'plz', 'plz bolo'): ['Na🙂', 'Uhu..😉', '😊😊', 'Na bollam😒'],
        ('mon kharap', 'mon karap', 'mood off'): ['Na', 'Hmm', '🙂🙂'],
        ('ki hoise', 'kichu hoise', 'kisu hoise'): ['Baad dao', 'Arey kichu na😒', 'Kichu na😑'],
        ('kichu na', 'nothing', 'kisu na', 'kichu nh', 'kisu nh'): ['Ok', 'Huh', 'Accha'],
        ('ho', 'ha', 'haa', 'hae'): ['Accha', 'Ok', 'Good'],
        ('sexy', 'tumi onek sexy', 'tmi onk sexy', 'tmi onnk sexy', 'tumi onk sexy', 'tmi sexy', 'tumi sexy'): ['Tumio', 'Jah😘', 'Sex korba?😏😁', 'Hehe..😏'],
        ('jaan', 'babu', 'jan', 'babui', 'babuii', 'sona'): [f"{secrets.choice(['Bolo', 'Hae', 'Hm', 'Ki'])} {msg}"],
        ('whats my name', 'amr nam ki', 'amar nam ki', 'what is my name'): [f"{m.chat.first_name}🙄", f"Amar jaan {m.chat.first_name}😘", f"Dustu {m.chat.first_name}😉"],
        ('koro', 'ok koro', 'accha koro', 'hmm koro', 'hm koro', 'thik ache'): ['Hmm.', 'Accha', 'Ok'],
        ('shuvo sokal', 'good morning', 'shuvo shokal'): ['Good Morning💙', 'Shuvo sokal😘💙', 'Shuvo sokal🥰'],
        ('shuvo ratry', 'good night'): ['Good Night💙', 'Shuvo ratry😘💙', 'Shuvo ratry🥰'],
        ('who made you', 'who is your creator', 'who created you', 'tmk ke banaise', 'tomake ke banaise', 'tmk k banaise', 'tomake k banaise'): ['Fuad😘', 'Fuad😁💙', 'Fuad😉'],
        ('time', 'koyta baje', 'baje koyta'): [f'{datetime.now(pytz.timezone("Asia/Dhaka")).hour}:{datetime.now(pytz.timezone("Asia/Dhaka")).minute}'],
        ('weather', 'weather ki', 'ajker weather', 'ajkr weather', 'weather update'): [getweather('Gazipur')]
    }

    for keys, response in responses.items():
        if msg in keys:
            return get_response(response)

    return get_response(["Jalaiyo na to. 😑", "Bujhi nai", "Kih?", "🙄😐"])