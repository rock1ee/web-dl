## Configure

Login Github and go to  account setting to create a peasonal  access token:

Settings -> Developer settings -> Personal access tokens -> Generate new token

And then add the token to the repo’s secrets

repo -> setting -> Secrets -> Action secrets -> New repository secret

name: ACCESS_TOKEN

value: content of the token

## BT Downloader Compared

Aria2: Best download performent but poor upload performent.Download speed is almost the fastest with popular torrent. Download speed increase fast and do not decrease when download is about to be finished. But it only announce to one tracker, so it maybe can not find seeder with unpopular torrent. It almost does not upload.

qBittorrent: Good download and upload performent. Download speed mostly slower than aria2 but faster than transmission with popular torrent.Download speed increase slow , max download speed is lower than aria2's , and decrease when download is about to be finished. It can announce to all trackers, so it can download unpopular torrent most of the time. It's upload speed faster than aria2.

Transmission: Poor download performent but best upload performent. Download speed mostly slower than aria2 and qBittorrent. mostly slower than aria2 but faster than transmission with popular torrent.Download speed increase slow , max download speed is lower than aria2's , and decrease when download is about to be finished. It can announce to tracker but seem to always failed. It's upload speed faster than aria2 and qbittorrent.
