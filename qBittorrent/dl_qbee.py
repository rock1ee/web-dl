import requests
import subprocess

def dl_latest(name):
    url = "https://api.github.com/repos/c0re100/qBittorrent-Enhanced-Edition/releases/latest"
    with requests.get(url) as r:
        res = r.json()["assets"]
        for i in res:
            if i["name"] == name:
                dlink = i["browser_download_url"]
    subprocess.run(["wget", "-q", dlink])
    subprocess.run(["unzip", name])
    subprocess.run(["rm", name])

if __name__ == "__main__":
    dl_latest("qbittorrent-enhanced-nox_x86_64-linux-musl_static.zip")