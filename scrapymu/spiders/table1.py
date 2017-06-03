import scrapy

BASE_URL = 'http://physics.nist.gov/PhysRefData/XrayMassCoef'
TABLE1_URL = '/'.join([BASE_URL, 'tab1.html'])


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
