import urllib.request
import requests
import bs4,random
z=[]
def pre_proc():
    url=['https://www.facebook.com/Strannger11/posts',
         'https://www.facebook.com/pages/category/Art/H-o-r-n-y-6-9-105290237679968/posts',
         "https://www.facebook.com/C-u-t-e-G-i-r-l-s-111939930162073/posts/?ref=page_internal",
         'https://www.facebook.com/assesandtiddies/posts/?ref=page_internal',
         'https://www.facebook.com/sadwatr/posts/?ref=page_internal'
         ]
    #url = random.choice(url)
    x=0
    for i in url:     
        data = requests.get(i)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        for i in soup.findAll('img'):
            try:
                z.append(i['data-src'])
            except:
                x+=1
        
def return_pic():
    print(len(z))
    if len(z)==0:
        pre_proc()
    return random.choice(z)


'''
url=['https://www.facebook.com/Strannger11/posts',
     'https://www.facebook.com/pages/category/Art/H-o-r-n-y-6-9-105290237679968/posts'
     ]
x=0
for i in url:     
    data = requests.get(i)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    for i in soup.findAll('img'):
        try:
            z.append(i['data-src'])
        except:
            x+=1
        
print(len(z))
random.choice(z)
'''
