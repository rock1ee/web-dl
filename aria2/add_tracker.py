#!/usr/bin/python3
import requests

def add_tracker(mylist, url):
    with requests.get(url) as r:
        trackers = ','.join( mylist + r.text.split('\n\n') )
    with open('./aria2/aria2.conf', 'a+') as f:
        f.write(f'bt-tracker={trackers}')
    print("tracker added!")


if __name__ == '__main__':
    mylist = ["http://sukebei.tracker.wf:8888/announce",
              "http://tracker.bt4g.com:2095/announce"]
    url = "https://trackerslist.com/best.txt"
    add_tracker(mylist, url)
