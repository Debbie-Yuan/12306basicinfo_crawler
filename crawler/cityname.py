import xlrd as reader
from os import path
from collections import namedtuple

Station = namedtuple("Station", "Name, Attr")


def getAllCities():
    raw = input("请输入Excel格式的城市信息 ： ")
    while not path.isfile(raw):
        raw = input("请重新输入Excel格式的城市信息 ： ")

    book = reader.open_workbook(raw)
    all = book.sheet_by_index(0)
    fav = book.sheet_by_index(1)

    allcities = []
    favcities = []

    for i in range(all.nrows):
        t1 = all.cell(i, 0).value
        t2 = all.cell(i, 1).value
        allcities.append(Station(t1.strip(), t2.strip()))

    for i in range(fav.nrows):
        t1 = fav.cell(i, 0).value
        t2 = fav.cell(i, 1).value
        favcities.append(Station(t1.strip(), t2.strip()))
    # return favcities
    return allcities, favcities
#
