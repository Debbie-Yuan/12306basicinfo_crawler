from crawler.crawl import *
from crawler.cityname import getAllCities, Station
from crawler.download_middleware import getsession


if __name__ == '__main__':
    al, fav = getAllCities()
    # fav = getAllCities()
    for i in fav:
        assert isinstance(i, Station)
        print(i.Name + '-' + i.Attr)
    session = getsession()
    print(session)
    date = "2019-07-02"
    # location = input("请输入数据存储的文件 ：")
    # while not path.isfile(location):
    #     location = input("请重新输入一个地址 ： ")

    savetxt(session, fav, date, "/Users/debbie/a.dat")
