import datetime

__author__ = 'daivq'


def convert(month):
    return '%02d' % (datetime.datetime.strptime(month, '%B').month)
