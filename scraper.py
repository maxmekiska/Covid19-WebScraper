import bs4, requests
import numpy as np
from prettytable import PrettyTable


class Data():
    def __init__(self, url):
        self.url = url
    def get_beautiful_soup(self):
        soup = bs4.BeautifulSoup(requests.get(self.url).text)
        table = soup.find_all('table')[0]
        return table

    def tableDataText(self, table):
        """Parses a html segment started with tag <table> followed
        by multiple <tr> (table rows) and inner <td> (table data) tags.
        It returns a list of rows with inner columns.
        Accepts only one <th> (table header/data) in the first row.

        Source
        ------
        https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
        """
        def rowgetDataText(tr, coltag='td'): # td (data) or th (header)
            return [td.get_text(strip=True) for td in tr.find_all(coltag)]
        rows = []
        trs = table.find_all('tr')
        headerow = rowgetDataText(trs[0], 'th')
        if headerow:
            rows.append(headerow)
            trs = trs[1:]
        for tr in trs:
            rows.append(rowgetDataText(tr, 'td'))
        return rows

class Out():
    def __init__(self, table):
        self.table = table
    def userinput(self):
        user = input("Country: ")
        result = np.where(self.table == f'{user}')
        self.country = result[0][0]
    def new_cases(self):
        print(f'New Cases: {self.table[self.country][3]}')
    def death(self):
        print(f'New Deaths: {self.table[self.country][5]}')
    def total_cases(self):
        print(f'Total Cases: {self.table[self.country][2]}')
    def active_cases(self):
        print(f'Active Cases: {self.table[self.country][8]}')
    def print_all(self):
        t = PrettyTable([self.table[0][1], self.table[0][3], self.table[0][5], self.table[0][8], self.table[0][2]])
        #t.hrules = True
        for i in range(1,len(self.table)):
            t.add_row(self.table[i,[1, 3, 5, 8, 2]])
        print(t)


def main():
    while(input('Continue [y/n]? ') != 'n'):
      data = Data('https://www.worldometers.info/coronavirus/')
      raw_table = data.get_beautiful_soup()
      table = data.tableDataText(raw_table)
      search_table = np.array(table)
      out = Out(search_table)
      print ("\n Menu:")
      print ("**********")
      print (" 1. Display data of a specific country")
      print (" 2. Display all data")

      __choose_menu = int(input("Enter your choice: "))
      if __choose_menu == 1:
        out.userinput()
        out.new_cases()
        out.death()
        out.active_cases()
        out.total_cases()
      elif __choose_menu == 2:
        out.print_all()

if __name__ == "__main__":
    main()
