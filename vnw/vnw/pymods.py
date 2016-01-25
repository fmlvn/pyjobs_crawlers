# -*- coding: utf-8 -*-


def xtract(response, xpath):
    li = []
    xtracts = response.xpath(xpath).extract()
    for xts in xtracts:
        xts = xts.strip()
        li.append(xts)
    return u'|'.join(li)


def parse_datetime(response, xpath):
    try:
        xtracts = response.xpath(xpath).extract()[0].strip()
        if u'-' in xtracts:
            xtracts = xtracts.split('-')
            xtracts.reverse()
            return u'-'.join(xtracts)
        else:
            xtracts = xtracts.split(': ')[1].split('/')
            xtracts.reverse()
            return u'-'.join(xtracts)
    except IndexError:
        return ''
