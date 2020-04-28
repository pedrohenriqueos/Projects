from conf.settings import BASE_API_URL
from threading import Thread
import time
import datetime
import requests
import lxml.html as lh

month = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}


class Back(Thread):
    def __init__(self,bot,update,cursor,connection):
        Thread.__init__(self)
        self.flag = True
        self.bot = bot
        self.update = update
        self.cursor = cursor
        self.connection = connection

    def banco(self):
        try:
            url = BASE_API_URL
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
            
            today = datetime.datetime.now()

            sql = 'SELECT `name`,`date` FROM bot_t'
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            #adiciona os novos contests, se existir algum
            insert1plus = False
            for element in filtro:
                insert = True
                for dado in result:
                    if dado["name"] == element[0]:
                        insert = False
                        break
                if insert==True:
                    insert1plus = True
                    sql = "INSERT INTO bot_t (name,date) VALUES(%s,%s)"
                    self.cursor.execute(sql,(element[0],element[1]))
            if insert1plus==True:
                self.connection.commit()
            
            # Remove contests antigos do banco
            for dado in result:
                t = dado["date"]
                if t<today:
                    sql = "DELETE FROM bot_t WHERE date<%s"
                    self.cursor.execute(sql,(today,))
                    self.connection.commit()
                    break

            return True	
        except:
            return False

    def run(self):
        while self.flag == True:
            ## Verificar se existe algum contest proximo, 1 dia ou 1 hora
            if self.banco()==True:
                self.bot.send_message(
                    chat_id = self.update.message.chat_id,
                    text = "Banco de dados atualizado"
                )
                today = datetime.datetime.now()
                val = today.hour*3600+today.minute*60+today.second
                val = 86400 - val
                time.sleep(val)
            else:
                self.bot.send_message(
                    chat_id = self.update.message.chat_id,
                    text = "Houve algum erro na atualização do banco de dados"
                )
                time.sleep(3600)
