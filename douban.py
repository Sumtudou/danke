import requests  # 导入requests包
import pymysql

from lxml import etree

class DouBan:
    def getResult(self):
        url_fir = "https://movie.douban.com/top250?start="
        url_thr = "&filter="
        for i in range(0, 226, 25):
            url = url_fir + str(i) + url_thr
            #print(url)
            Headers = {
                'Cookie': 'bid="IOL6EW/Q0k4"; ll="118269"; __yadk_uid=JXhZSYpp8B4Ni2Kxv7IB58DQc6X8cUy8;'
                          ' trc_cookie_storage=taboola%2520global%253Auser-id%3Ded44f62f-dab3-4edd-aaa5-f03f467fbff7-tuct4bed844;'
                          ' _vwo_uuid_v2=D2BDB883F7DD5FD10B0886B7FDF923E80|45b25101f5483a8c9fdc338259e00312; douban-fav-remind=1;'
                          ' __utma=30149280.1878873378.1573212749.1575464422.1578204798.5;'
                          ' __utmc=30149280; __utmz=30149280.1578204798.5.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
                          ' __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1578204802%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D;'
                          ' _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=223695111.590282347.1573212749.1578204802.1578204984.5;'
                          ' __utmb=223695111.0.10.1578204984; __utmz=223695111.1578204984.5.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
                          ' __utmt=1; regpop=1; __utmb=30149280.4.10.1578204798;'
                          ' _pk_id.100001.4cf6=52abee194aa99a3c.1573212749.4.1578205589.1575464436.',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            }
            strHtml = requests.get(url, headers=Headers)
            resp = etree.HTML(strHtml.content.decode('utf-8'))

            allItem = resp.xpath('//ol[@class="grid_view"]/li')
            titleEnglish = self.getResList('.//div[@class="hd"]/a/span[@class="title"][2]/text()', allItem, 1)
            rank = self.getResList('./div/div[@class="pic"]/em/text()', allItem, 0)
            movieHref = self.getResList('./div/div[@class="pic"]/a/@href', allItem, 0)
            poster = self.getResList('./div/div[@class="pic"]/a/img/@src', allItem, 0)  # 封面海报
            title = self.getResList('.//div[@class="hd"]/a/span[@class="title"][1]/text()', allItem, 0)
            other = self.getResList('.//div[@class="hd"]/a/span[@class="other"]/text()', allItem, 0)
            playable = self.getResList('.//div[@class="hd"]/span/text()', allItem, 0)
            summary = self.getResList('.//div[@class="bd"]/p[1]/text()', allItem, 0)
            quote = self.getResList('.//div[@class="bd"]/p[2]/span/text()', allItem, 0)  # 总结？ 希望使人自由！
            score = self.getResList('.//div[@class="star"]/span[2]/text()', allItem, 0)
            scoreNumber = self.getResList('.//div[@class="star"]/span[4]/text()', allItem, 0)

            self.saveToMysql(25, rank, movieHref, poster, title, titleEnglish, other, playable, summary, quote, score,
                             scoreNumber)
            #break


    def drapPlaceAndPrint(self, list):
        for k in range(len(list)):
            list[k] = list[k].replace("\xa0", "")
            list[k] = list[k].replace("\n", "")
            list[k] = list[k].replace(" ", "")
        # print(list)

    def drapNbspAndGang(self, list):
        for k in range(len(list)):
            list[k] = list[k].replace("\xa0", "")
            list[k] = list[k].replace("/", "")
        # print(list)

    #
    # str  xpath的参数
    # allitem xpath 父级元素
    # flag== 1  去掉/和&nbsp   else  去掉 空格
    def getResList(self, str, allItem, flag):
        list = []
        for item in allItem:
            temp = item.xpath(str)
            if len(temp) == 0:
                list.append('')
            else:
                list.append(temp[0])
        if flag == 1:
            self.drapNbspAndGang(list)
        else:
            self.drapPlaceAndPrint(list)
        print(list)
        print(len(list))
        return list

    # 11个字段  rank,movieHref,poster,title,titleEnglish,other,playable,summary,quote,score,scoreNumber
    def saveToMysql(self, lens, rank, movieHref, poster, title, titleEnglish, other, playable, summary, quote, score,
                    scoreNumber):
        USERNAME = "root"
        PASSWD = "123456"
        ADDR = "localhost"
        DATABASE = "python"
        TABLE = "dou_ban_top250"
        db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
        cursor = db.cursor()  # get cursor

        for i in range(lens):
            sql = """INSERT INTO `{}` (`rank`, `moviehref`,`poster`,`title`,`titleenglish`,`other`,`playable`, `summary`,`quote`,`score`,`scoreNumber`) VALUES
            ("{}", "{}", "{}", "{}", "{}","{}", "{}", "{}", "{}", "{}", "{}");""".format(
                TABLE, rank[i], movieHref[i], poster[i], title[i], titleEnglish[i],
                other[i], playable[i], summary[i], quote[i], score[i], scoreNumber[i]
            )
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()

    def truncateTable(self):
        USERNAME = "root"
        PASSWD = "123456"
        ADDR = "localhost"
        DATABASE = "python"
        TABLE = "dou_ban_top250"
        db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
        cursor = db.cursor()  # get cursor
        cursor.execute("truncate table dou_ban_top250;")


if __name__ == "__main__":
    gg = DouBan()
    gg.truncateTable()
    gg.getResult()