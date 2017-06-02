import scrapy

BASE_URL = 'http://physics.nist.gov/PhysRefData/XrayMassCoef'
TABLE1_URL = '/'.join([BASE_URL, 'tab1.html'])
TABLE3_URL = '/'.join([BASE_URL, 'ElemTab/z{:02d}.html'])


def parse_table1_row(row):
    all_cols = (c.strip() for c in row.css('td::text').extract())
    cols = [c for c in all_cols if c != '']
    if cols != []:
        try:
            z = int(cols[0])
            data = {'symbol': cols[1],
                    'name': cols[2],
                    'Z/A': cols[3],
                    'density [g/cm^3]': cols[5]}
            return z, data
        except ValueError:
            return None


class Table1Spider(scrapy.Spider):
    name = 'table1'

    start_urls = [TABLE1_URL]

    def parse(self, response):
        all_rows = (parse_table1_row(r) for r in response.css('tr'))
        rows = (r for r in all_rows if r is not None)
        yield {k: v for k, v in rows}


class Table3Spider(scrapy.Spider):
    name = 'table3'

    start_urls = [TABLE3_URL.format(z) for z in range(1, 93)]

    def parse(self, response):
        # Retrieving the atomic number from the URL
        z = int(response.url[-7:-5])

        pre = response.css('pre').extract_first()
        lines = pre.splitlines()
        all_rows = ([x for x in line[3:].split()] for line in lines[6:-1])
        rows = [r for r in all_rows if r is not None and r != []]
        yield {z: rows}
