def saveToMysql(self, lens, img, title, price, traffic, datail, type):
    USERNAME = "root"
    PASSWD = "123456"
    ADDR = "localhost"
    DATABASE = "python"
    TABLE = "danke"
    db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
    cursor = db.cursor()  # get cursor

    for i in range(lens):
        sql = """INSERT INTO `{}` (`img`, `title`,`price`,`traffic`,`datail`,`type`) VALUES
        ('{}', '{}', '{}', '{}', '{}', '{}');""".format(
            TABLE, img[i], title[i], price[i], traffic[i], datail[i], type[i]
        )
        # print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()


def truncateTable(self):
    USERNAME = "root"
    PASSWD = "123456"
    ADDR = "localhost"
    DATABASE = "python"
    TABLE = "dou_ban_top250"
    db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
    cursor = db.cursor()  # get cursor
    cursor.execute("truncate table danke;")