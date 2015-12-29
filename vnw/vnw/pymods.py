__author__ = 'daivq'

def xtract(response, xpath):
    li = []
    xtracts = response.xpath(xpath).extract()
    for xts in xtracts:
        xts = xts.strip()
        li.append(xts)
    return u'|'.join(li)

