import jieba
import pymysql
import wordcloud
import numpy as np
import matplotlib.pyplot as plt
import PIL
class CutWords:
    def readFromMysql(self):
        # GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'cws+166' WITH GRANT OPTION;
        USERNAME = "root"
        PASSWD = "123456"  # 如果是远程授权访问的话，此选项不必是相应用户(如 root )的登录密码。此时相当于授权码
        ADDR = "localhost"
        DATABASE = "python"
        TABLE = "anjuke"
        # 虽然说 MySQLdb 只支持 Python2 ，但Python3也能用
        db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
        cursor = db.cursor()
        cursor.execute("select title from anjuke ")
        results = cursor.fetchall()
        return results

    def dropPlaceAndN(self,list):
        for i in range(len(list)):
            list[i] = list[i].replace("\n","").replace(" ","")

    def getTheText(self):
        result = []
        with open('txt/notin1.txt', 'r', encoding='utf-8') as f:
            for line in f:
                result.append(line.strip('\n'))

        with open('txt/notin2.txt', 'r', encoding='utf-8') as f:
            for line in f:
                result.append(line.strip('\n'))

        with open('txt/notin3.txt', 'r', encoding='utf-8') as f:
            for line in f:
                result.append(line.strip('\n'))

        return result


if __name__ == '__main__':
    '''
    gg = CutWords()
    resTuple = gg.readFromMysql()
    resList = [word[0] for word in resTuple]
    gg.dropPlaceAndN(resList)

    wordList = []
    for i in range(len(resList)):
        res = jieba.lcut(resList[i])
        wordList+=res

    #print(len(wordList))
    #print(wordList)
    #a = [1, 2, 3, 1, 1, 2]
    dict = {}     #得到键值对的set
    for key in wordList:
        if len(key) > 1:
            dict[key] = dict.get(key, 0) + 1

    items = list(dict.items())  # 将键值对转换成列表
    items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

    notin = gg.getTheText()  #拿到排除的词库
    #print(notin)
    top_word50 = []
    j = 0
    for item in items:
        if item[0] not in notin :
            #print(item)
            top_word50.append(item)
            j+=1
        if j == 50:
            break

    print(top_word50)
        theTxt = " ".join([word[0] for word in top_word50])
    print(theTxt)
    '''
    the_top50 = [('精装', 8177), ('地铁口', 7281), ('业主', 6791), ('三房', 5518), ('花园', 5466), ('看房', 3785), ('首付', 3573), ('学位', 3374), ('红本', 3146), ('物业', 3079), ('急售', 3035), ('户型', 3001), ('地铁', 2771), ('南北', 2559), ('出售', 2495), ('两房', 2442), ('阳台', 2421), ('小区', 2406), ('精装修', 2229), ('装修', 2228), ('楼层', 2217), ('方便', 2197), ('一手', 2151), ('在手', 2113), ('诚心', 2078), ('通透', 2032), ('新房', 2011), ('朝南', 1874), ('深圳', 1793), ('学校', 1668), ('社区', 1618), ('号线', 1581), ('价格', 1555), ('安静', 1553), ('豪宅', 1546), ('采光', 1512), ('税费', 1403), ('万科', 1375), ('光明', 1327), ('高层', 1308), ('满五', 1301), ('外国语', 1290), ('公园', 1267), ('方正', 1247), ('海景', 1238), ('实验', 1231), ('30', 1224), ('赠送', 1185), ('入住', 1179), ('复式', 1177)]

    the_txt = '精装'
    for item in the_top50:
        for i in range(item[1]):
            the_txt  =the_txt+ ' '+item[0]
    print(the_txt)

    image1 = PIL.Image.open(r'image/love.jpg')
    MASK = np.array(image1)
    txt = "life is short, you need python"
    w = wordcloud.WordCloud(background_color="white",font_path="D://pythonRoot//venv//FZZH-RHJW.TTF",repeat=False,collocations=False,mask= MASK)
    w.generate(the_txt)
    w.to_file("image/pywcloud.png")
