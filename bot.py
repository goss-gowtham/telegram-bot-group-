import telebot
import requests
import youtube_dl
import os
from wholesome import return_pic

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

#           Config vars
token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)
x=bot.get_me()
print(x)
crs = ''
task = {'':''}

@bot.message_handler(commands=['curse'])
def command_words(msg):
        global crs
        crs = msg.text.split()
        if len(crs)>1:
                bot.send_message(msg.chat.id, 'suckm ' + ' '.join(crs[1:]))
        else:
                bot.send_message(msg.chat.id, 'suckm da ')
        print(msg.message_id)
        bot.delete_message(msg.chat.id,msg.message_id)

@bot.message_handler(commands=['info'])
def command_info(msg):
        bot.reply_to(msg,msg.chat)
        
@bot.message_handler(commands=['wholesome'])
def command_info(msg):
        url = return_pic()
        bot.send_photo(msg.chat.id,url)


@bot.message_handler(commands=['note'])
def command_info(msg):
        li = msg.text.split()
        if len(li)>1:
                task[li[1]]=' '.join(li[2:])
        bot.reply_to(msg,'note added successmfully..')

@bot.message_handler(commands=['view'])
def command_info(msg):
        li = msg.text.split()
        if len(li)>1:
                if task.get(li[1]):
                        bot.reply_to(msg,li[1]+':\n'+task[li[1]])
                else:
                        bot.reply_to(msg,'noe...')
        else:
                bot.reply_to(msg,'availamble:\n'+ ',\n'.join(task.keys()))


@bot.message_handler(commands=['down'])
def down(msg):
        li = msg.text.split()[1]
        
        with ydl:
            result = ydl.extract_info(
                li,
                download=False # We just want to extract the info
            )
        
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
        
        for i in video['formats']:
            #dct[i['format_note']] = i['url']
            s=''
            if i.get('format_note'):
                s=i['format_note']+': '+ i['url']+'\n'
            else:
                s=i['url']
            bot.reply_to(msg,s)









@bot.message_handler(commands=['motivate'])
def send_welc(message):
        x= requests.request(url='https://api.quotable.io/random',method='get')
        bot.reply_to(message, x.json()['content'])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "spam panalam da pundaigala")
'''
@bot.message_handler(func=lambda message: True)
def echo_all(message):
        bot.reply_to(message,'dont spam ')
'''     
bot.polling()
