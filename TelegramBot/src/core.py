from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from conf.settings import TELEGRAM_TOKEN, PASSWORD, HOST_DB, USER_DB, PASSWORD_DB, DB
from back import Back
import datetime
import pymysql.cursors

urls = {'codeforces':'https://codeforces.com/contests/','atcoder':'https://atcoder.jp/','teste':'https://google.com/'}

class TelegramCommands():
	def __init__(self):
		self.connection = pymysql.connect(host=HOST_DB,
		                                  user=USER_DB,
		                                  password=PASSWORD_DB,
		                                  db=DB,
		                                  charset='utf8',
		                                  cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connection.cursor()

	def start(self,bot,update):
		self.th1 = Back(bot,update,self.cursor,self.connection)
		response_message = "Comandos do bot:\n/nexts - Mostra os próximos contests\n/today - Mostra os contests de hoje\n/stop - Parar o bot"
		bot.send_message(
			chat_id = update.message.chat_id,
			text = response_message
		)
		self.th1.start()

	def stop(self,bot,update):
		self.th1.flag = False
		bot.send_message(
			chat_id = update.message.chat_id,
			text = "O bot parou"
		)

	def nexts(self,bot,update):
		sql = "SELECT `name`,`date`,`cod` FROM bot_t ORDER BY `date` ASC"
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		response_message = "Próximos contests:\n"

		for dado in result:
			response_message += "["+dado["name"]+"]("+urls[dado['cod']]+")\n"+dado["date"].strftime("%d/%m/%y %H:%M")+"\n"
		if response_message=="Próximos contests:\n":
			response_message = "Não há contests próximos"
		
		bot.send_message(
			chat_id = update.message.chat_id,
			text = response_message,
			parse_mode=ParseMode.MARKDOWN
		)

	def today(self,bot,update):
		sql = "SELECT `name`,`date`,`cod` FROM bot_t WHERE DAY(date)=%s AND MONTH(date)=%s ORDER BY `date` ASC"
		today = datetime.datetime.now()
		self.cursor.execute(sql,(today.day,today.month))
		result = self.cursor.fetchall()		
		response_message = "Contests de hoje:\n"
		
		for dado in result:
			response_message += "["+dado["name"]+"]("+urls[dado['cod']]+")\n"+dado["date"].strftime("%d/%m/%y %H:%M")+"\n"		
		if response_message == "Contests de hoje:\n":
			response_message = "Não há contests hoje"

		bot.send_message(
			chat_id = update.message.chat_id,
			text = response_message,
			parse_mode= ParseMode.MARKDOWN
		)

	def unknown(self,bot, update):
		response_message = "Comando desconhecido"
		bot.send_message(
			chat_id=update.message.chat_id,
			text=response_message
		)

	def main(self):
		updater = Updater(token=TELEGRAM_TOKEN)
		dispatcher = updater.dispatcher
		
		dispatcher.add_handler(
			CommandHandler('start',self.start)
		)
		dispatcher.add_handler(
			CommandHandler('nexts',self.nexts)
		)
		dispatcher.add_handler(
			CommandHandler('today',self.today)
		)
		dispatcher.add_handler(
			CommandHandler('stop',self.stop)
		)
		dispatcher.add_handler(
			MessageHandler(Filters.command, self.unknown)
		)
		updater.start_polling()
		updater.idle()

if __name__=='__main__':
	print("press CTRL + C to cancel.")
	Commands = TelegramCommands()
	Commands.main()