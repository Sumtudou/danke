import requests  # 导入requests包
from lxml import etree
import time
import csv
class Location:
    #保存到csv
    def getResult(self,firstUrl,theCity):
        for i in range(1, 10000):  #  最大10000页，显然达不到
            time.sleep(0.5)
            url = firstUrl + str(i)
            strHtml = requests.get(url)
            resp = etree.HTML(strHtml.content.decode('utf-8'))

            print("当前page=",end=" ")
            print(i,end="\n")
            print(url)

            allItem = resp.xpath('//div[@class="r_lbx"]')

            img = self.getResList('./a/img/@src',allItem)
            title = self.getResList('.//div[@class="r_lbx_cena"]/a/text()',allItem)
            traffic = self.getResList('./div[@class="r_lbx_cen"]/div[@class="r_lbx_cena"]/div[@class="r_lbx_cena"]/text()[2]',allItem)
            detail = self.getResList('.//div[@class="r_lbx_cenb"]/text()[2]',allItem)
            price = self.getResList('.//span[@class="ty_b"]/text()',allItem)
            type = self.getResList('.//div[@class="r_lbx_cenb"]/i/text()',allItem)  # 格式不一样，合是 i  整是  em  有毒
            city = theCity
            self.handleType(type)

            detailItemList = []
            #print(detail)
            for item in detail :
                resList = item.split('|',4)
                detailItemList.append(resList)
            #print(detailItemList)
            self.handleHetailItemList(detailItemList)

            # print(detailItemList)
            # print(len(detailItemList))

            if len(img) == 0:
                break
            data = []
                           #['img', 'title', 'price', 'traffic', 'type', 'url', 'city', 'square', 'height', 'roomsum', 'direction']
            for i in range(len(img)):
                data.append([img[i],title[i],price[i],traffic[i],type[i],url,city,detailItemList[i][0],detailItemList[i][1],detailItemList[i][2],detailItemList[i][3]])

            #print(data)
            self.saveTocsv(data)
            #break

    def handleHetailItemList(self,list):
        for item in list:
            item[0] = item[0].replace('建筑面积约','').replace('㎡','')
            item[1] = item[1].replace('楼','')
            item[3] = item[3].replace('朝','')

            res = item[2].split('室',2)  # res[0]  3  res[1]  1厅
            if int(res[0]) >=6 :
                res[0] = "其他"
                item[2] = res[0]+"室"+res[1]
        return list


    def drapPlaceAndPrint(self, list):
        for k in range(len(list)):
            list[k] = list[k].replace("\n", "").replace(' ', '')


    def handleType(self ,list):
        for i in range(len(list)):
            if list[i] == "":
                list[i] = "整"


    def getResList(self, str, allItem):
        list = []
        for item in allItem:
            temp = item.xpath(str)
            if len(temp) == 0:
                list.append('')
            else:
                list.append(temp[0])
        self.drapPlaceAndPrint(list)
        # print(list)
        # print(len(list))
        return list
    #[img[i],title[i],price[i],traffic[i],type[i],url,city,detailItemList[i]
    def saveTocsv(self,data):
        header = ['img', 'title','price','traffic','type','url','city','square','height','roomsum','direction']
        with open('danke.csv', 'a+', encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    # [img[i],title[i],price[i],traffic[i],type[i],url,city,detailItemList[i]
    def saveToCsvHeader(self):
        header = ['img', 'title','price','traffic','type','url','city','square','height','roomsum','direction']
        with open('danke.csv', 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

if __name__ == "__main__":
    gg = Location()
    gg.saveToCsvHeader()
    #gg.truncateTable()
    listCity = ['wh','bj', 'sz', 'sh', 'hz', 'tj', 'nj', 'gz', 'cd', 'gs', 'wx', 'xa', 'cq']
    firUrl = 'https://www.danke.com/room/'
    thrUrl = '?page='
    for item in listCity:
        url = firUrl + item + thrUrl
        gg.getResult(url,item)

    #gg.getResult(wuHan)



