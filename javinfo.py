#!/usr/bin/python3
import sys
import requests
from urllib import parse
from bs4 import BeautifulSoup

# video_id SSIS-835
def javbus_info(video_id):
    video_id = video_id.replace('-C','')
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}
    r = requests.get(f"https://www.javbus.com/{video_id}", headers=header)
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.find('div', {'class': 'container'})
    title = content.h3.text.strip()
    poster = "https://www.javbus.com/" + soup.find('div', {'class': 'screencap'}).a['href']
    r = requests.get(poster, headers=header)
    with open("x86_64-unknown-linux-musl.tar.gz", 'wb') as pic:
        pic.write(r.content)
    print(title, "video info had been saved!")

#video_id SSIS835
def dmm_info(video_id):
    video_id = video_id.replace('-C','').replace('-','')
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0', 'X-Forwarded-For': '104.28.243.105'}
    url = f"https://www.dmm.co.jp/mono/dvd/-/detail/=/cid={video_id}/"
    age_check = f"https://www.dmm.co.jp/age_check/=/declared=yes/?rurl={parse.quote(url)}"
    s = requests.session()
    s.get(age_check, headers=header)
    r = s.get(url, headers=header)
    soup = BeautifulSoup(r.text, "html.parser")
    poster = soup.find('a', {'name': 'package-image'})['href']
    r = requests.get(poster, headers=header)
    with open("x86_64-unknown-linux-musl.tar.gz", 'wb') as pic:
        pic.write(r.content)
    print(poster, " had been saved!")


if __name__ == '__main__':
    video_id = sys.argv[1]
    try:
        javbus_info(video_id)
    except:
        dmm_info(video_id)