from threading import Thread
import time
import datetime
import requests
import lxml.html as lh

month = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
urls = {'codeforces':'https://codeforces.com/contests/','atcoder':'https://atcoder.jp/'}

class Back(Thread):
    def __init__(self,bot,update,cursor,connection):
        Thread.__init__(self)
        self.flag = True
        self.bot = bot
        self.update = update
        self.cursor = cursor
        self.connection = connection
        self.dayprint = []
        self.hourprint = []
        today = datetime.datetime.now()
        self.meianoite = today - datetime.timedelta(hours=today.hour,minutes=today.minute,seconds=today.second) + datetime.timedelta(days=1)
        
    def day_contests(self,today,result):
        for dado in result:
            date = dado["date"]
            if (date - today).total_seconds()<=86401.0 and (date - today).total_seconds()>=86399.0:
                self.dayprint.append(dado)

    def hour_contests(self,today,result):
        for dado in result:
            date = dado["date"]
            if (date - today).total_seconds()<=3601.0 and (date - today).total_seconds()>=3599.0:
                self.hourprint.append(dado)

    def codeforces(self,url):
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')
        out = []
        for element in tr_elements[:-6]:
            out.append([t.text_content() for t in element])

        filtro = []
        for element in out[1:]:
            if element[0].replace("\r","").replace("\n","").replace(" ","")=='Name':
                break
            text = element[2].replace("\r","").replace("\n","").replace(" ","")
            date = text[:-5]
            time = text[11:]
            d = datetime.datetime(year=int(date[7:]),month=month[date[:3]],day=int(date[4:6]),hour=int(time[:2]),minute=int(time[3:])) - datetime.timedelta(hours=3)
            filtro.append([element[0].split("\r\n")[1], d ])

        return filtro  

    def atcoder(self,url):
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')
        out = []
        fl = False
        for element in tr_elements:
            out.append([t.text_content() for t in element])

        filtro = []
        for element in out:
            if element[0]=='Start Time':
                if fl==True:
                    break
                fl = True
                continue
            if fl==True:
                date = element[0]
                d = datetime.datetime(year=int(date[:4]),month=int(date[5:7]),day=int(date[8:10]),hour=int(date[11:13]),minute=int(date[14:16]),second=int(date[17:19])) - datetime.timedelta(hours=12)
                filtro.append([element[1][2:], d ])

        return filtro

    def insert_banco(self,filtro,result,cod):
        insert1plus = False
        for element in filtro:
            insert = True
            for dado in result:
                if dado["name"] == element[0]:
                    insert = False
                    break
            if insert==True:
                insert1plus = True
                sql = "INSERT INTO bot_t (cod,name,date) VALUES(%s,%s,%s)"
                self.cursor.execute(sql,(cod,element[0],element[1]))
        if insert1plus==True:
            self.connection.commit()

    def add_banco(self):
        sql = 'SELECT `name`,`date` FROM bot_t'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        filtro = self.codeforces('https://codeforces.com/contests/')
        self.insert_banco(filtro,result,'codeforces')

        filtro = self.atcoder('https://atcoder.jp/')
        self.insert_banco(filtro,result,'atcoder')
            
    def rmv_banco(self,today,result):
        for dado in result:
            t = dado["date"]
            if t<today:
                sql = "DELETE FROM bot_t WHERE date<%s"
                self.cursor.execute(sql,(today,))
                self.connection.commit()
                break

    def day_print(self,today,result):
        self.day_contests(today,result)
        if len(self.dayprint)!=0:
            resp = ""
            for dado in self.dayprint:
                resp += "["+dado['name']+"]("+urls[dado['cod']]+") Acontecerá em 1 dia"
            self.bot.send_message(
                chat_id = self.update.message.chat_id,
                text = resp
            )
            self.dayprint.clear()

    def hour_print(self,today,result):
        self.hour_contests(today,result)
        if len(self.hourprint)!=0:
            resp = ""
            for dado in self.hourprint:
                resp += "["+dado['name']+"]("+urls[dado['cod']]+") Acontecerá em 1 hora"
            self.bot.send_message(
                chat_id = self.update.message.chat_id,
                text = resp
            )
            self.hourprint.clear()

    def att_banco(self,today,result):
        self.rmv_banco(today,result)
        self.add_banco()
        print("banco atualizado")

    def set_sleep(self,today,result):
        if self.meianoite<today:
            self.meianoite = self.meianoite + datetime.timedelta(days=1)
        val = (self.meianoite - today).total_seconds()
        for dado in result:
            if dado['date']>=today+datetime.timedelta(hours=1):
                val = min(val,(dado['date']-(today+datetime.timedelta(hours=1))).total_seconds())
            if dado['date']>=today+datetime.timedelta(days=1):
                val = min(val,(dado['date']-(today+datetime.timedelta(days=1))).total_seconds())
        return val

    def run(self):
        today = datetime.datetime.now()
        sql = "SELECT `name`,`date`,`cod` FROM bot_t"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.att_banco(today,result)
        val = self.set_sleep(today,result)
        print(val)
        time.sleep(val)

        while self.flag == True:
            today = datetime.datetime.now()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            
            self.day_print(today,result)
            self.hour_print(today,result)            
            self.att_banco(today,result)

            today = datetime.datetime.now()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            val = self.set_sleep(today,result)
            print(val)
            time.sleep(val)