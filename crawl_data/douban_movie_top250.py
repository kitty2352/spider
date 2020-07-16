import requests
from bs4 import BeautifulSoup
import re
from faker import Faker
from database.dbc import Pymysql_dbc

# 获取页面html
def getHTMLText(url):
    faker = Faker()
    headers = {
        'User-Agent': faker.user_agent(),
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        # response.encoding = response.apparent_encoding
        html = BeautifulSoup(response.text, features="lxml")
        return html
    else:
        print("获取失败")

# 获取分页的url
def pageUrl(url):
    # 获取总页数
    html = getHTMLText(url)
    page_url = html.select(".paginator>a")
    page_num = len(html.select(".paginator>a"))
    totleUrl = [url]
    for i in range(0, page_num):
        href = url + page_url[i]["href"]
        totleUrl.append(href)
    return totleUrl


def get_data(url):
    # 获取每个分页的url
    totalUrl = pageUrl(url)

    # 连接数据库
    db = Pymysql_dbc()
    conn = db.get_conn()

    # 循环遍历每个分页，获取每一页中的数据
    for i in totalUrl:
        html = getHTMLText(i)
        # 获取class=grid_view的元素下的所有li元素
        movie_list = html.select(".grid_view > li")
        for movie in movie_list:
            # 得到标签包裹着的文本
            movie_title = movie.select(".item>.info>.hd>a>span")[0].text
            # 得到标签内的属性
            movie_url = movie.select("a")[1]["href"]
            movie_details = str(movie.select(".item>.info>.bd>p")[0]).replace("\n", "").replace("\r", "").replace(" ", "")
            movie_detail = re.findall(r">(.*)<", movie_details)[0]
            movie_year = re.findall(r'\b\d+\b', movie_detail)[0]
            movie_country = movie_detail.split('/')[-2]
            movie_type = movie_detail.split("/")[-1]
            movie_score = movie.select(".item>.info>.bd>.star>span")[1].text
            # print(movie_title, "--", movie_url, "--", movie_year, "--", movie_country, "--", movie_type, "--", movie_score)
            sql = "select title from movies where title = '%s'" % movie_title
            sql1 = "INSERT INTO movies(title, url, m_year, country, type, score) VALUES('%s', '%s', '%s', '%s','%s', '%s')" % (
            movie_title, movie_url, movie_year, movie_country, movie_type, movie_score)

            if db.is_data_exis(conn, sql):
                print("数据已存在")
            else:
                # 将数据写入数据库
                db.insert(conn, sql1)

    # 关闭数据库连接
    conn.close()


if __name__ == '__main__':
    url = "http://movie.douban.com/top250"
    get_data(url)