from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from conf.settings import BASE_API_URL, TELEGRAM_TOKEN, PASSWORD, HOST_DB, USER_DB, PASSWORD_DB, DB
import requests
import lxml.html as lh
import pandas as pd
import datetime
import pymysql.cursors

month = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}



def start(bot,update):
	response_message = "Comandos do bot:\n/nexts - Mostra os próximos contests\n/today - Mostra os contests de hoje\n"
	bot.send_message(
		chat_id = update.message.chat_id,
		text = response_message
	)

def nexts(bot,update):
	sql = "SELECT `name`,`date` FROM bot_t"
	cursor.execute(sql)
	result = cursor.fetchall()
	response_message = "Próximos contests:\n"
	for dado in result:
		response_message += str(dado["name"])+" "+str(dado["date"])+"\n"
	if response_message=="Próximos contests:\n":
		response_message = "Não há contests próximos"
	else:
		response_message = response_message[:-1]

	bot.send_message(
		chat_id = update.message.chat_id,
		text = response_message
	)


def today(bot,update):
	sql = "SELECT `name`,`date` FROM bot_t WHERE DAY(date)=%s AND MONTH(date)=%s"
	today = datetime.datetime.now()
	cursor.execute(sql,(today.day,today.month))
	result = cursor.fetchall()
	

	
	response_message = "Contests de hoje:\n"
	
	for dado in result:
		response_message += str(dado["name"])+" "+str(dado["date"])+"\n"	
	
	if response_message == "Contests de hoje:\n":
		response_message = "Não há contests hoje"
	else:
		response_message = response_message[:-1]

	bot.send_message(
		chat_id = update.message.chat_id,
		text = response_message
	)

def banco():
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
			filtro.append([element[0].replace("\r","").replace("\n","").replace(" ",""), d ])

		today = datetime.datetime.now()

		sql = 'SELECT `name`,`date` FROM bot_t'
		cursor.execute(sql)
		result = cursor.fetchall()

		#adiciona os novos contests, se existir algum
		insert1plus = False
		for element in filtro:
			insert = True
			for dado in result:
				if dado["name"] == element[0]:
					insert = False
					break
			if insert==True:
				sql = "INSERT INTO bot_t (name,date) VALUES(%s,%s)"
				cursor.execute(sql,(element[0],element[1]))
		if insert1plus==True:
			connection.commit()

		# Remove contests antigos do banco
		for dado in result:
			t = dado["date"]
			if t<today:
				sql = "DELETE FROM pass WHERE date<%s"
				cursor.execute(sql,(str(today),))
				connection.commit()
		return True
	except:
		return False

def attbot(bot,update,args):
	response_message = ""
	if args[0]==PASSWORD:
		attend = banco()
		if attend==True:
			response_message = "Banco atualizado com sucesso!"
		else:
			response_message = "Houve algum erro na atualização do bot :("
	else:
		response_message = "Comando desconhecido"
	bot.send_message(
		chat_id=update.message.chat_id,
		text=response_message
	)

def unknown(bot, update):
	response_message = "Comando desconhecido"
	bot.send_message(
		chat_id=update.message.chat_id,
		text=response_message
	)

def main():
	updater = Updater(token=TELEGRAM_TOKEN)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(
		CommandHandler('start',start)
	)
	
	dispatcher.add_handler(
		CommandHandler('nexts',nexts)
	)
	
	dispatcher.add_handler(
		CommandHandler('today',today)
	)

	dispatcher.add_handler(
		CommandHandler('attbot',attbot,pass_args=True)
	)

	dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )

	updater.start_polling()
	updater.idle()

if __name__=='__main__':
	print("press CTRL + C to cancel.")
	connection = pymysql.connect(host=HOST_DB,
	                             user=USER_DB,
	                             password=PASSWORD_DB,
                                 db=DB,
                                 charset='utf8',
	                             cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	main()


