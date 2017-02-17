# -*- coding: utf-8 -*-

import pynayzr
import time
import json
import multiprocessing
import datetime
from io import BytesIO
from contextlib import closing
from mongoengine import connect, fields
from mongoengine.document import Document


class News(Document):
    timestamp = fields.DateTimeField(require=True, default=datetime.datetime.utcnow)
    news = fields.StringField()
    info = fields.DictField()
    img = fields.ImageField()


def fetch(news):
    connect('news_data', host='localhost', port=27017)

    m = pynayzr.analyze(news)
    news = News()
    news.info = json.loads(m.to_json())
    news.news = m.news

    b = BytesIO()
    m.img.save(b, format='PNG')
    news.img.put(b)
    news.save()

    del m


def main():
    pynayzr.set_google_credentials('/home/grd/Project/Pynayzr/pynayzr-monitor/key.json')

    collective_list = ['tvbs', 'cti', 'ebc', 'ftv']

    with closing(multiprocessing.Pool(4)) as p:
        p.map(fetch, collective_list)


if __name__ == '__main__':
    print('Start PyNayzr Monitor')
    count = 0
    while True:
        count += 1
        print('\r>>> % 4d' % (count), end='')
        main()
        time.sleep(10)
