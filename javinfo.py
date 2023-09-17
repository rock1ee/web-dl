#!/usr/bin/python3
import sys
import requests
from bs4 import BeautifulSoup

def find_video_info(video_id):
    video_id = video_id.replace('-C','')
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}
        r = requests.get(f"https://www.javbus.com/{video_id}", headers=header)
        print(f"https://www.javbus.com/{video_id}")
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find('div', {'class': 'container'})
        title = content.h3.text.strip()
        poster = "https://www.javbus.com/" + soup.find('div', {'class': 'screencap'}).a['href']
        img_links = [poster]
        img = soup.find('div', id='sample-waterfall')
        if img:
            for i in img.find_all('a'):
                img_links.append(i['href'])
        for i, url in zip(range(len(img_links)), img_links):
            r = requests.get(url, headers=header)
            with open(f"pic{i}.jpg", 'wb') as pic:
                pic.write(r.content)
        print(title, "video info had been saved!")
    except Exception as err:
        print(err, "don't find anything!")

def gen_index(video_id):
    with open('index.html') as f:
        text = f.read().replace('{name}', video_id)
    with open('index.html', 'w') as f:
        f.write(text)

if __name__ == '__main__':
    video_id = sys.argv[1]
    gen_index(video_id)
    find_video_info(video_id)