import os
import requests
from bs4 import BeautifulSoup

# list github releases tag
# repo: github owner/repo,such as `rock1ee/web-dl`
# page: page number
# per_page: how many items per page(max=100)
def get_tag_list(repo, page, per_page=28):
    tag_list = []
    url = f'https://api.github.com/repos/{repo}/releases'
    params = {'per_page': per_page, 'page': page}
    with requests.get(url, params=params) as r:
        releases = r.json()
    for release in releases:
        tag_list.append(release['tag_name'])
    return tag_list

# repo: github owner/repo,such as `rock1ee/web-dl`
def get_total_page(repo):
    total_page = 1
    while get_tag_list(repo, total_page):
        total_page += 1
    return total_page - 1

# generate detail page for each video
# name: video name(video id)
def gen_detail_page(name, video_src, img_src):
    hls = open("./template/hls.html", 'r')
    page = open(f'./page/{name}.html', 'a')
    content = hls.read().replace('{video_src}', video_src).replace('{img_src}', img_src).replace('{name}', name)
    page.write(content)
    hls.close()
    page.close()
    print(name, 'page generated!')

# generate card tag for each video in index page
# href: url that link to video detail page
# img_src: image url of video poster
def gen_card_tag(href, img_src, title):
    soup = BeautifulSoup("<li class=\"card\"></li>", "html.parser")
    original_tag = soup.li
    style = f"background-image: url({img_src});"
    card_img_tag = soup.new_tag("a", attrs={"class": "card-image", "href": href, "target": "_blank", "style": style})
    img_tag = soup.new_tag("img", attrs={"src": img_src, "alt": title})
    desc_tag = soup.new_tag("a", attrs={"class": "card-description", "href": href, "target": "_blank"})
    text_tag = soup.new_tag("p")
    text_tag.string = title
    card_img_tag.append(img_tag)
    desc_tag.append(text_tag)
    original_tag.append(card_img_tag)
    original_tag.append(desc_tag)
    return original_tag

# generate index page for all video
# repo: github owner/repo,such as `rock1ee/web-dl`
# index_num: index page number
# video_id_list: a list of video_id(repo name)
# total_page: number of index page(for figuring out number of pagination)
def gen_index_page(repo, index_num, tag_list, total_page):
    proxy_url = 'https://ghproxy.com/'
    pre_url = f'https://github.com/{repo}/releases/download'
    html_name = f"index{index_num}.html"
    html = open(html_name, "wb")
    homepage = open("./template/home.html", "r")
    soup = BeautifulSoup(homepage.read(), "html.parser")
    # add iterm to card-list
    card_list = soup.body.ul
    for tag in tag_list:
        img_src = f"{proxy_url}/{pre_url}/{tag}/x86_64-unknown-linux-musl.tar.gz"
        video_src = f"{proxy_url}/{pre_url}/{tag}/x86_64-unknown-linux-musl.zip"
        new_item = gen_card_tag(f"./page/{tag}.html", img_src, tag)
        card_list.append(new_item)
        print(tag, "had added to index!")
        gen_detail_page(tag, video_src, img_src)
    # pagination
    page_list = soup.find("div",{"class": "pagination"}).ul
    # prev_page
    page_tag = soup.new_tag("li")
    page_num = index_num - 1 if index_num - 1 > 0 else index_num
    page_name = f"index{page_num}.html"
    href_tag = soup.new_tag("a", attrs={"href": page_name})
    page_tag.append(href_tag)
    page_list.append(page_tag)
    # page num
    for i in range(1, total_page + 1):
        if i == index_num:
            page_tag = soup.new_tag("li", attrs={"class": "active"})
        else:
            page_tag = soup.new_tag("li")
        page_name = f"index{i}.html"
        href_tag = soup.new_tag("a", attrs={"href": page_name})
        page_tag.append(href_tag)
        page_list.append(page_tag)
    # next_page
    page_tag = soup.new_tag("li")
    page_num = index_num + 1 if index_num + 1 <= total_page else index_num
    page_name = f"index{page_num}.html"
    href_tag = soup.new_tag("a", attrs={"href": page_name})
    page_tag.append(href_tag)
    page_list.append(page_tag)
    # save html
    html.write(soup.encode("utf-8"))
    # if index1.html, add extra index.html
    if index_num == 1:
        with open("index.html", "wb") as f:
            f.write(soup.encode("utf-8"))
    html.close()
    homepage.close()
    print(html_name, "generated!")


if __name__ == '__main__':
    repo = os.getenv('GITHUB_REPOSITORY')
    total_page = get_total_page(repo)
    for i in range(1, total_page + 1):
        tag_list = get_tag_list(repo, i)
        gen_index_page(repo, i, tag_list, total_page)
