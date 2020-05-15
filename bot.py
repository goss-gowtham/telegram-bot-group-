import telebot
import random
import requests
import json
import youtube_dl
import tweepy,os
from wholesome import return_pic, pre_proc

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

#           Config vars
token = os.environ['TELEGRAM_TOKEN']
Tconsumer_key = os.environ['TCONSUMER_KEY']
Tconsumer_sec = os.environ['TCONSUMER_SEC']
Taccess_key = os.environ['TACCESS_KEY']
Taccess_key = os.environ['TACCESS_SEC']

bot = telebot.TeleBot(token)
x = bot.get_me()
print(x)
crs = ''
task = {'': ''}

curse_words = ['suck me da', 'Fuck you', 'Bastard', 'Punda', 'Otha', 'Thevdiya', 'Jaya Surya is a bitch', 'Koothi',
               'Jaya Surya Sindhu', 'Nandlal Kandaraoli', 'Baadu', 'Poolu', 'Puluthi', 'Kandaraoli', 'Soothu', 'Sunni']


@bot.message_handler(commands=['curse'])
def command_words(msg):
    global crs
    crs = msg.text.split()
    if len(crs) > 1:
        bot.send_message(msg.chat.id, random.choice(curse_words) + ' ' + ' '.join(crs[1:]))
    else:
        bot.send_message(msg.chat.id, random.choice(curse_words))
    print(msg.message_id)
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.message_handler(commands=['info'])
def command_info(msg):
    bot.reply_to(msg, msg.chat)


@bot.message_handler(commands=['wholesome','wholesome-update'])
def command_info(msg):
        if len(msg.text.split('-'))>1:
                pre_proc()
                bot.send_message(msg.chat.id,'updated..')
        else:
                url = return_pic()
                bot.send_photo(msg.chat.id,url)

@bot.message_handler(commands=['note'])
def command_info(msg):
    li = msg.text.split()
    if len(li) > 1:
        task[li[1]] = ' '.join(li[2:])
    bot.reply_to(msg, 'note added...')


@bot.message_handler(commands=['view'])
def command_info(msg):
    li = msg.text.split()
    if len(li) > 1 and task.get(li[1]):
        bot.reply_to(msg, li[1] + ' - ' + task[li[1]])
    elif len(task) > 1:
        print(len(task))
        bot.reply_to(msg, 'Available: ' + '\n'.join(task.keys()) + '\nMention a note to view')
    else:
        bot.reply_to(msg, 'Try `/note <topic> <note to add>` to create and view notes', parse_mode='MarkdownV2')


@bot.message_handler(commands=['down'])
def down(msg):
    li = msg.text.split()[1]
    try:
        with ydl:
            result = ydl.extract_info(
                li,
                download=False  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        for i in video['formats']:
            s = ''
            link = '<a href=\"' + i['url'] + '\">' + 'Video' + '</a>'

            if i.get('format_note'):
                bot.reply_to(msg, i['format_note'] + link, parse_mode='HTML')
            else:
                bot.reply_to(msg, link, parse_mode='HTML')
    except:
        bot.reply_to(msg, 'No Output available')


@bot.message_handler(commands=['motivate'])
def send_welc(message):
    x = requests.request(url='https://api.quotable.io/random', method='get')
    bot.reply_to(message, x.json()['content'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "HyP0 bot developer for personal usage!")


@bot.message_handler(commands=['twitter'])
def send_trends(message):
    # replace consumer_key, consumer_secret with the below codes
    auth = tweepy.OAuthHandler(Tconsumer_key, Tconsumer_sec)
    # replace access_token, access_secret with below codes
    auth.set_access_token(Taccess_key,
                          Taccess_sec)

    api = tweepy.API(auth)

    # id is the unique id from twitter specific to India
    trending = api.trends_place(23424848)
    text = 'India Trending - Twitter\n\n'
    for i, top_trends in enumerate(trending[0]['trends']):
        tweet_count = ''
        if i < 25:
            if top_trends['tweet_volume'] is not None:
                tweet_count = str(top_trends['tweet_volume']) + ' tweets' + '\n'
            text += str(i + 1) + '. ' + '<a href=\"' + top_trends['url'] + '\">' + top_trends['name'] + '</a>' + \
                    '\n' + tweet_count + '\n'

    bot.reply_to(message, text, parse_mode='html')


'''
@bot.message_handler(func=lambda message: True)
def echo_all(message):
        bot.reply_to(message,'dont spam ')
'''
bot.polling()
