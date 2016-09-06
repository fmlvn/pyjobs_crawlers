# -*- coding: utf-8 -*-

import datetime


A_DAY_IN_SEC = 86400


def xtract(response, xpath):
    li = []
    xtracts = response.xpath(xpath).extract()
    for xts in xtracts:
        xts = xts.strip()
        li.append(xts)
    return u'|'.join(li)


def parse_datetime(time):
    '''
    Return datetime string in YYYY-mm-dd format
    '''
    correct_time = str(datetime_from(time)).split(' ')[0]
    return correct_time


def datetime_from(time):
    post_date = str(time)
    post_date = post_date.strip()
    return datetime.datetime.strptime(post_date, '%d-%m-%Y')


def has_expired(time):
    now = datetime.datetime.now()
    return (datetime_from(time) - now).total_seconds() < A_DAY_IN_SEC
