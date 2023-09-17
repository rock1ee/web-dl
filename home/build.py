import os
import requests
from bs4 import BeautifulSoup

# list github repo name
# token: github repo access token for authentication
# page: page number(30 items per page)
def list_repos(token, page=1):
    url = 'https://api.github.com/user/repos'
    header = {'Authorization': f'token {token}'}
    params = {'per_page': 30, 'page': page, 'sort': 'updated'}
    r = requests.get(url, headers=header, params=params)
    repos = r.json()
    repo_name_list = []
    for repo in repos:
        repo_name_list.append(repo['name'])
    return repo_name_list

# generate detail page for each video
# repo: github repository name
def gen_detail_page(repo):
    hls = open("./template/hls.html", 'r')
    page = open(f'./page/{repo}.html', 'a')
    content = hls.read().replace('{name}', repo)
    page.write(content)
    hls.close()
    page.close()
    print(repo, 'page generated!')

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
# owner: github username/account
# index_num: index page number
# video_id_list: a list of video_id(repo name)
# total_page: number of index page(for figuring out number of pagination)
def gen_index_page(owner, index_num, video_id_list, total_page):
    html_name = f"index{index_num}.html"
    exclude_repos = {'web-dl', 'JavSub'}
    html = open(html_name, "wb")
    homepage = open("./template/home.html", "r")
    soup = BeautifulSoup(homepage.read(), "html.parser")
    # add iterm to card-list
    card_list = soup.body.ul
    proxy_url = 'https://fastv.pages.dev'
    for video_id in video_id_list:
        if video_id in exclude_repos:
            continue
        if requests.head(f"https://raw.githubusercontent.com/{owner}/{video_id}/master/img/pic0.jpg").status_code == 200:
            img = f"{proxy_url}/video/{video_id}/online/img/pic0.jpg"
        else:
            img = f"{proxy_url}/video/{video_id}/online/pic0.jpg"
        new_item = gen_card_tag(f"./page/{video_id}.html", img, video_id)
        card_list.append(new_item)
        print(video_id, "had added to index!")
        gen_detail_page(video_id)
    # pagination
    page_list = soup.find("div",{"class": "pagination"}).ul
    # prev
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
    # next
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


def get_public_repo_num(owner)->int:
    url = f"https://api.github.com/users/{owner}"
    return int(requests.get(url).json()["public_repos"])


if __name__ == '__main__':
    token = os.getenv('GH_TOKEN')
    owner = os.getenv('GITHUB_REPOSITORY_OWNER')
    total_page = int(get_public_repo_num(owner)/30) + 1
    for i in range(1, total_page + 1):
        info = list_repos(token, i)
        gen_index_page(owner, i, info, total_page)
