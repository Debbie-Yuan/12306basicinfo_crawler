import requests
import json
from urllib import parse
from collections import namedtuple


class Train:
    def __init__(self, lno, code, fr, to, start, end, duration, date, ps, pd,
                 stype, price):
        self.lno = lno
        self.code = code
        self.fr = fr
        self.to = to
        self.start = start
        self.end = end
        self.duration = duration
        self.date = date
        self.ps = ps
        self.pd = pd
        self.stype = stype
        self.price = price

    def __str__(self):
        return 'Label No. : {}, Code : {}, From : {}, To : {}, TimeStart : {}, TimeEnd : {}, Date : {},' \
               'Price : {}'.format(self.lno, self.code, self.fr, self.to, self.start, self.end, self.date, self.price)


Price = namedtuple("Price", "A1, A3, A4, WZ, A9, M, O, AI, AJ")

# A1 硬卧 ； A3 高级软卧； A4 一等座  WZ 无座 A9 特等座/商务座 M 一等座 O二等座 AI 软卧/一等卧 AJ 硬卧/二等卧
# Train = namedtuple("Train", 'lno, code, fr, to, start, end, duration, date, ps, pd, stype, bprice, cprice')
# lno -> price query train no tag
# ps -> price query start tag
# pd -> price query end tag

DOMAIN = "kyfw.12306.cn"

START_URLS = {'train': 'https://kyfw.12306.cn/otn/leftTicket/query',
              'price': 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice',
              'main': 'https://www.12306.cn/index/',
              'refer': 'https://kyfw.12306.cn/otn/leftTicket/init',
              }

r_date = "date"
r_flag = "flag"
r_fs = "fs"
r_ts = "ts"
r_ltid = "linktypeid"
t_date = 'leftTicketDTO.train_date'
t_fs = 'leftTicketDTO.from_station'
t_ds = 'leftTicketDTO.to_station'
t_pc = 'purpose_codes'
p_no = 'train_no'
p_fs = 'from_station_no'
p_ds = 'to_station_no'
p_stype = 'seat_types'
# =OM9
p_date = "train_date"


HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/'
                '12.1.1 Safari/605.1.15',
}


def getsession():
    session = requests.sessions.session()
    session.headers = HEADERS
    session.verify = False

    resp = session.get(START_URLS.get('main'))
    if resp.status_code != 200:
        raise requests.exceptions.BaseHTTPError
    return session


def querystring_r(fs, td, date):
    fromstation = "{},{}".format(fs.Name, fs.Attr)
    tostation = "{},{}".format(td.Name, td.Attr)
    qd = {r_ltid: 'dc', r_fs: fromstation, r_ts: tostation, r_date: date, r_flag: r'N,N,Y'}
    pt = parse.urlencode(qd, encoding="gb2312")
    return START_URLS['refer'] + '?' + pt.split("N%2CN%2CY") + "N,N,Y"


def querystring_t(date, fs, td):
    qd = {t_date: date, t_fs: fs, t_ds: td, t_pc: "ADULT"}
    return START_URLS['train'] + '?' + parse.urlencode(qd, encoding="gb2312")


def querystring_p(no, fs, td, date, stype):
    qd = {p_no: no, p_fs: fs, p_ds: td, p_stype: stype, p_date: date}
    return START_URLS['price'] + '?' + parse.urlencode(qd, encoding="gb2312")


def parsejson_t(js):
    ret = json.loads(js)
    dat = ret.get('data')
    for e in dat.get('result'):
        res = e.split('|')
        if res[0] == "列车停运":
            yield None
        if "暂停发" in res[-1]:
            yield None
        datime = res[13]
        datstr = "{}-{}-{}".format(datime[0:4], datime[4:6], datime[6:8])
        yield Train(res[2], res[3], res[4], res[5], res[8], res[9], res[10], datstr, res[16], res[17], res[-4], 0)


def parsejson_p(js):
    ret = json.loads(js)
    dat = ret.get('data')
    return Price(dat.get('A1', 0), dat.get('A3', 0), dat.get('A4', 0), dat.get('WZ', 0), dat.get('A9', 0),
                 dat.get('M', 0), dat.get('O', 0), dat.get('AI', 0), dat.get('AJ', 0))
