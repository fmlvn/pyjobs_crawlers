# -*- coding: utf-8 -*-

import datetime


def xtract(response, xpath):
    li = []
    xtracts = response.xpath(xpath).extract()
    for xts in xtracts:
        xts = xts.strip()
        li.append(xts)
    return u'|'.join(li)


def parse_datetime(time):
    post_date = str(time)
    post_date = post_date.strip()
    correct_time = datetime.datetime.strptime(post_date, '%d-%m-%Y')
    correct_time = str(correct_time).split(' ')[0]
    return correct_time
