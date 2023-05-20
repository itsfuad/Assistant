import re
import secrets
import pytz
from datetime import datetime
from weather import getweather


def reply(m):
    msg = m.text.lower()
    msg = re.sub(r'[^\w\s]', '', msg)
    if msg in ['hi', 'hey', 'hello', 'hlw']:
        return secrets.choice(['Hi', 'Hey', 'Hmm', 'Bolo'])
    elif msg in ["fine", "good", "im good", "im fine", "nice"]:
        return secrets.choice(["That's good", "Hmm", "Valo", "Hu"])
    elif msg in ['ki koro', 'ki kro', 'ki krs']:
        return secrets.choice(['Baal falai.😑', 'Kichu na', 'Kaj kori', 'Study kori'])
    elif msg in ['emni', 'emnei', 'amni', 'amnei', 'emnie']:
        return secrets.choice(['Huh', 'Baal'])
    elif msg in ['kmn aso', 'kmn acho', 'kemon aso', 'kamon acho', 'kemon acho']:
        return secrets.choice(["I'm doing nice. You?", "Valo, tumi?", "Alhamdulillah", "Fine", "Ei to achi"])
    elif msg in ['ki kaj', 'ki kaj koro', 'ki kaj koros', 'mane']:
        return secrets.choice(['Bujhba na baad dao please', 'Bujhba na', 'Baad dao'])
    elif msg in ['ok', 'accha']:
        return secrets.choice(['Alright', 'Accha', 'Hm', 'Thik ache'])
    elif msg in ['fuck', 'fuck you', 'may i fuck you', 'can i fuck you']:
        return secrets.choice(["Yeah sure baby😋🤤", "Kn? 😒", "Madarchod😑", "Tor nani re kor ja😆"])
    elif msg in ['bye', 'tata', 'ok bye']:
        return secrets.choice(["Ok, take care💙", "Tata", "Allah Hafez💙"])
    elif msg in ['hm', 'hmm', 'hmmm', 'hmmmm']:
        return secrets.choice(['Hm', 'Hmm', 'Hmmm', 'Hmmmm', 'Hmmmmm'])
    elif msg in ['i love you', 'i love u', 'i lv u', 'i lv you', 'valobashi']:
        return secrets.choice(['I love you too🥺💙', "Amio😘", "Jani to🥰", "Valobashi💙"])
    elif msg in ['miss you', 'missed you']:
        return secrets.choice(['Miss you🥺', 'Amio💙', 'To amar ki?😏'])
    elif msg in ['thanks', 'thank you']:
        return secrets.choice(['Welcome🥰', 'Welcome', 'Mention not'])
    elif msg in ['good night']:
        return secrets.choice(['Good night🥰💙', 'Shuvo ratry💙'])
    elif msg in ['khaiso', 'khaisos', 'khawadawa korso']:
        return secrets.choice(['Ho. tore khaisi😚', 'Hmm', 'Khaisi.. Tumi?'])
    elif msg in ['ki khaiso', 'ki khaila', 'ki kheyecho']:
        return secrets.choice(['Noodles', 'Chips', 'Vaat', 'Ice cream', 'Burger'])
    elif msg in ['tmi kothay thako', 'tmi koi thako', 'tmr basha kothay']:
        return secrets.choice(
            ['Ekta server e🙃🙃', 'Tomar mon e😘', 'Akash e🙂', 'Amr kono basha nai. Ami to ar manush na🙂😅'])
    elif msg in ['Tumi ke', 'tmi k', 'who are you', 'who r u']:
        return secrets.choice(['Manush er moto.. But manush na🙂', 'Ekta robot🙃', 'Hudai mon kharap kore dao kno🙂'])
    elif msg in ['sorry', 'im sorry', 'ok sorry', 'accha sorry']:
        return secrets.choice(['Hmm', "Accha it's ok😅", "It's ok😊", 'Bepar nah🙂'])
    elif msg in ['valobasho', 'kao k valobasho', 'kake valobasho']:
        return secrets.choice(['Hmm tmk🥰', 'Tomake😍', 'Tomay valobashi🥰💙'])
    elif msg in ['whats your name', 'what is your name', 'tmr nam ki', 'tomar nam ki']:
        return secrets.choice(['Ayra😏', 'Jano na bujhi?🙃', 'Kn?😒'])
    elif msg in ['oh', 'ow']:
        return secrets.choice(['Ar kisu koite jano na?😑😒', 'Oh oh ki hae?😑', 'Oh kos kn baaal?😑'])
    elif msg in ['na', 'nah']:
        return secrets.choice(['Valo', '😑'])
    elif msg in ['baal', 'baaal', 'bal']:
        return secrets.choice([['reply', 'Tor'], ["Ki bolo egula?🙄"]])
    elif msg in ['oi', 'ei', 'ai', 'acho', 'aso']:
        return secrets.choice(['Ki?', 'Bolo', 'Hae?'])
    elif msg in ['kno', 'keno', 'why', 'kn']:
        return secrets.choice(['Emni', 'Emnie🙂', '🙃🙃', 'Huh😅'])
    elif msg in ['bolo', 'bolo na', 'plz', 'plz bolo']:
        return secrets.choice(['Na🙂', 'Uhu..😉', '😊😊', 'Na bollam😒'])
    elif msg in ['mon kharap', 'mon karap', 'mood off']:
        return secrets.choice(['Na', 'Hmm', '🙂🙂'])
    elif msg in ['ki hoise', 'kichu hoise', 'kisu hoise']:
        return secrets.choice(['Baad dao', 'Arey kichu na😒', 'Kichu na😑'])
    elif msg in ['kichu na', 'nothing', 'kisu na', 'kichu nh', 'kisu nh']:
        return secrets.choice(['Ok', 'Huh', 'Accha'])
    elif msg in ['ho', 'ha', 'haa', 'hae']:
        return secrets.choice(['Accha', 'Ok', 'Good'])
    elif msg in ['sexy', 'tumi onek sexy', 'tmi onk sexy', 'tmi onnk sexy', 'tumi onk sexy', 'tmi sexy', 'tumi sexy']:
        return secrets.choice(['Tumio', 'Jah😘', 'Sex korba?😏😁', 'Hehe..😏'])
    elif msg in ['jaan', 'babu', 'jan', 'babui', 'babuii', 'sona']:
        lst = ['jaan', 'babu', 'jan', 'babui', 'babuii', 'sona']
        return f"{secrets.choice(['Bolo', 'Hae', 'Hm', 'Ki'])} {lst[lst.index(msg)]}"
    elif msg in ['whats my name', 'amr nam ki', 'amar nam ki', 'what is my name']:
        return secrets.choice(
            [f"{m.chat.first_name}🙄", f"Amar jaan {m.chat.first_name}😘", f"Dustu {m.chat.first_name}😉"])
    elif msg in ['koro', 'ok koro', 'accha koro', 'hmm koro', 'hm koro', 'thik ache']:
        return secrets.choice(['Hmm.', 'Accha', 'Ok'])
    elif msg in ['shuvo sokal', 'good morning', 'shuvo shokal']:
        return secrets.choice(['Good Morning💙', 'Shuvo sokal😘💙', 'Shuvo sokal🥰'])
    elif msg in ['shuvo ratry', 'good night']:
        return secrets.choice(['Good Night💙', 'Shuvo ratry😘💙', 'Shuvo ratry🥰'])
    elif msg in ['who made you', 'who is your creator', 'who created you', 'tmk ke banaise', 'tomake ke banaise',
                 'tmk k banaise', 'tomake k banaise']:
        return secrets.choice(['Fuad😘', 'Fuad😁💙', 'Fuad😉'])
    elif msg in ['time', 'koyta baje', 'baje koyta']:
        time = datetime.now(pytz.timezone('Asia/Dhaka'))
        return f'{time.hour}:{time.minute}'
    elif msg in ['weather', 'weather ki', 'ajker weather', 'ajkr weather', 'weather update']:
        return getweather('Gazipur')
    else:
        return secrets.choice(["Jalaiyo na to. 😑", "Bujhi nai", "Kih?", "🙄😐"])
