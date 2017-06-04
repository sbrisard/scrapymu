import scrapy

BASE_URL = 'http://physics.nist.gov/PhysRefData/XrayMassCoef'
TABLE3_URL = '/'.join([BASE_URL, 'ElemTab/z{:02d}.html'])


def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


class Table3Spider(scrapy.Spider):
    name = 'table3'

    start_urls = [TABLE3_URL.format(z) for z in range(1, 93)]

    def parse(self, response):
        # Retrieving the atomic number from the URL
        z = int(response.url[-7:-5])

        pre = response.css('pre').extract_first()
        lines = pre.splitlines()
        all_rows = ([x for x in line.split() if is_float(x)]
                    for line in lines[6:-1])
        rows = [r for r in all_rows if r is not None and r != []]
        yield {z: rows}
