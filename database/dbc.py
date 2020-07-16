from pymysql import connect
from database.dbconfig import DB_API_TEST

class Pymysql_dbc():
    def get_conn(self):
        # 连接数据库
        conn = connect(**DB_API_TEST)
        return conn

    def query(self, conn, sql):
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def insert(self, conn, sql):
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("insert ok")

    def is_data_exis(self, conn, sql):
        cur = conn.cursor()
        res = cur.execute(sql)
        if res:
            return True
        else:
            return False


if __name__ == '__main__':
    title = "肖申克的救赎"
    url = "https://movie.douban.com/subject/1292052/ "
    m_year = "1994"
    country = "美国"
    type = " 犯罪剧情"
    score = "9.7"
    db = Pymysql_dbc()
    conn = db.get_conn()
    sql = "select title from movies where title = '%s'" %title
    sql1 = "INSERT INTO movies(title, url, m_year, country, type, score) VALUES('%s', '%s', '%s', '%s','%s', '%s')" % (title, url, m_year, country, type, score)

    if db.is_data_exis(conn, sql):
        print("数据已存在")
    else:
        db.insert(conn, sql1)

    conn.close()