import scrapy

BASE_URL = 'http://physics.nist.gov/PhysRefData/XrayMassCoef'
TABLE3_URL = '/'.join([BASE_URL, 'ElemTab/z{:02d}.html'])


class Table3Spider(scrapy.Spider):
    name = 'table3'

    start_urls = [TABLE3_URL.format(z) for z in range(1, 93)]

    def parse(self, response):
        pre = response.css('pre').extract_first()
        lines = pre.splitlines()
        value = [[x for x in line[3:].split()] for line in lines[6:-1]]
        key = response.url.split('/')[-1].split('.')[0]
        yield {key: value}
