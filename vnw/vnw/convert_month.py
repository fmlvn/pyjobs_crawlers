import datetime

__author__ = 'daivq'


def convert(month):
    try:
        number = datetime.datetime.strptime(month, '%B').month
    except ValueError:
        number = datetime.datetime.strptime(month, '%b').month
    return '%02d' % (number,)
