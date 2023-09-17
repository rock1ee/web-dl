import requests
from time import sleep


def convert_size(fsize):
    if fsize < 1024:
        rest = f'{fsize}B'
    elif fsize < 1024*1024:
        rest = f'{fsize/1024:.1f}KB'
    elif fsize < 1024*1024*1024:
        rest = f'{fsize/1024/1024:.1f}MB'
    else:
        rest = f'{fsize/1024/1024/1024:.1f}GB'
    return rest

def convert_time(eta):
    if eta < 60:
        rest = f'{eta}s'
    elif eta < 60*60:
        min = eta // 60
        sec = eta % 60
        rest = f'{min}min{sec}s'
    elif eta < 60*60*24:
        hour = eta // 3600
        min = (eta % 3600) // 60
        sec = eta % 60
        rest = f'{hour}h{min}min{sec}s'
    else:
        rest = '>1d'
    return rest

def torrents_info(addr):
    url = addr + '/api/v2/torrents/info'
    with requests.get(url) as r:
        info = r.json()[0]
    name = info['name']
    hash = info['hash']
    state = info['state']
    progress = info['progress']
    seeds = info['num_seeds']
    leechs = info['num_leechs']
    size = convert_size(info['size'])
    dlspeed = convert_size(info['dlspeed'])
    upspeed = convert_size(info['upspeed'])
    completed = convert_size(info['completed'])
    ratio = info['ratio']
    eta = convert_time(info['eta'])
    print(state, f'{completed}/{size}({progress*100:.1f}%) CN:{leechs} SD:{seeds} DL:{dlspeed} UL:{upspeed} {ratio:.1f} ETA:{eta}',flush=True)
    return progress


def get_maindata(addr, rid):
    url = addr + f'/api/v2/sync/maindata?{rid}'
    r = requests.get(url)
    rid = r.json()['rid']
    dht_nodes = r.json()['server_state']['dht_nodes']
    peers = r.json()['server_state']['total_peer_connections']
    return rid,dht_nodes,peers
    

if __name__ == '__main__':
    progress = 0
    addr = 'http://localhost:8080'
    while progress != 1:
        try:
            progress = torrents_info(addr)
        except Exception as e:
            print(e)
        sleep(2)
