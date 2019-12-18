from django.core.management.base import BaseCommand, CommandError
import requests
from bs4 import BeautifulSoup
from patent.models import Patent
from django.conf import settings


class Command(BaseCommand):

    help = 'parse patents and save in to db'
    publication_number = settings.DEFAULT_PATENT_NUMBER
    base_url = settings.GP_BASE_URL
    page_url = settings.GP_PATENT_PAGE_URL.format(patent=publication_number)

    def add_arguments(self, parser):
        parser.add_argument(
            '-pn', '--publication_number',
            type=str,
            help='add a publication number to parse patent page'
        )

    def handle(self, *args, **options):
        publication_number = options['publication_number']
        if publication_number:
            self.publication_number = publication_number

        columns = ['Publication number', 'Priority date', 'Publication date', 'Assignee', 'Title']
        rows = self.parse_data(columns, self.page_url)
        objs = []

        for row in rows:
            objs.append(Patent(
                publication_number=row[0],
                publication_page_url=row[1],
                priority_date=row[2],
                publication_date=row[3],
                assignee=row[4],
                title=row[5],
            ))

        result = Patent.objects.bulk_create(objs, len(objs), ignore_conflicts=True)
        print(result.__len__(), 'records parsed..')

    def parse_data(self, columns, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        table_rows = []

        tables = soup.findAll('table')
        for index, table in enumerate(tables):
            print("Parsing table {}.....".format(index))
            table_rows.extend(self.parse_table(table, columns))

        return table_rows

    def parse_table(self, table, columns):
        parsed_header = table.find('thead')
        parse_table = True
        rows = []

        for column in columns:
            if column not in str(parsed_header):
                parse_table = False

        if parse_table:
            parsed_tbody = table.find('tbody')
            parsed_tr_tags = parsed_tbody.findAll('tr')

            for tr_tag in parsed_tr_tags:
                td_tags = tr_tag.findAll('td')
                row = []
                for index, row_data in enumerate(td_tags):
                    if index == 0:
                        row.append(row_data.text.replace("\n", "").replace("(en)", "").replace("*", "").strip())
                        row.append(self.base_url + row_data.find('a')['href'])
                    elif index == 1 or index == 2:
                        row.append(self.parse_date(row_data.text.replace("\n", "").strip()))
                    else:
                        row.append(row_data.text.replace("\n", "").strip())
                rows.append(row)

        return rows

    def parse_date(self, date_text):
        import datetime as dt
        return dt.datetime.strptime(date_text, '%Y-%m-%d')
