from . import download_middleware
from . import cityname
from collections import namedtuple
from time import sleep
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TrainMeta = namedtuple("TrainMeta", "fromStation, destinyStation, detailList")


def crawling(fav, session, date):
    for i in fav:
        for j in fav:
            if i == j:
                continue
            else:
                assert isinstance(i, cityname.Station)
                assert isinstance(j, cityname.Station)
                queryurl_t = download_middleware.querystring_t(date, i.Attr, j.Attr)
                resp = session.get(queryurl_t, verify=False)
                print("[INFO-Price] [GET {}] URL : {}\n".format(resp.status_code, queryurl_t))
                if resp.status_code != 200:
                    print("Faild, going to continue")
                dres = []
                for train in download_middleware.parsejson_t(resp.text):
                    if not train:
                        continue
                    print("\r[Train]->{}".format(train))
                    queryurl_p = download_middleware.querystring_p(train.lno, train.ps, train.pd, train.date, train.stype)
                    try:
                        tx = session.get(queryurl_p, verify=False).text
                        print("[INFO-Price] [GET 200] URL : {}\n".format(queryurl_p))
                        train.price = download_middleware.parsejson_p(tx)
                        print("\r[Price]->{}\n".format(train.price))
                    except Exception:
                        print("[ERROR] Falid to parse the json file.\n")
                    dres.append(train)
                    # Prevent bing banned
                    sleep(0.15)
                yield TrainMeta(i, j, dres)


def printlist(res_list):
    for i in res_list:
        assert isinstance(i, TrainMeta)
        print(i.fromStation, i.destinyStation)
        for j in i.detailList:
            print(j)


def savetxt(session, fav, date, path="/root/stations.txt"):
    with open(path, 'w') as fp:
        for i in crawling(fav, session, date):
            fp.write("*\n")
            assert isinstance(i, TrainMeta)
            fp.write("{} {}\n".format(i.fromStation.Attr, i.destinyStation.Attr))
            for j in i.detailList:
                assert isinstance(j, download_middleware.Train)
                if isinstance(j.price, int):
                    continue
                ls = list(j.price)
                if isinstance(ls, list):
                    for t, v in enumerate(ls):
                        if isinstance(v, str):
                            ls[t] = float(v.split('¥')[-1])
                    small = 9999.0
                    for v in ls:
                        if 0 < v < small:
                            small = v
                    fp.write("{} {} {}\n".format(j.code, j.duration, small))
            fp.write("*\n")

    return 1
