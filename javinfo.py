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
        r = requests.get(poster, headers=header)
        with open("x86_64-unknown-linux-musl.tar.gz", 'wb') as pic:
            pic.write(r.content)
        print(title, "video info had been saved!")
    except Exception as err:
        print(err, "don't find anything!")


if __name__ == '__main__':
    video_id = sys.argv[1]
    find_video_info(video_id)