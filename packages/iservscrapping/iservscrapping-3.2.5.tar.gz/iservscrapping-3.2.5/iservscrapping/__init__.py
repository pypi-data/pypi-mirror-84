"""
This is a scrapper to get some data from iserv servers providing Untis plans.
Copyright (C) Alwin Lohrie / Niwla23, MIT Licensed
"""

import re
from string import Template

import requests
import requests_cache
from bs4 import BeautifulSoup


def remove_duplicates(lis):
    """
    This function removes duplicates from a list.
    """
    y, s = [], set()
    for t in lis:
        w = tuple(sorted(t)) if isinstance(t, list) else t
        if w not in s:
            y.append(t)
            s.add(w)
    return y


numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


class BaseIserv:
    def __init__(self, url, username, password, cache=False):
        self.username = username
        self.password = password
        self.time_to_next_substitution_request = 0
        self.url = url
        self.session = requests.Session()

        if cache:
            print("Cache Enabled")
            requests_cache.install_cache('cache', expire_after=3600)

    def login(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'_username': self.username, '_password': self.password}
        return self.session.post(self.url + '/iserv/login_check', headers=headers, data=payload)


class Task(BaseIserv):
    def __init__(self, url, username, password):
        super().__init__(url, username, password)
        self.title = None
        self.start_date = None
        self.end_date = None
        self.done = None
        self.corrections = None
        self.id = None

        self.author = None
        self.description = None
        self.provided_files = []

    def get_details(self, path="/iserv/exercise/show/"):
        res = self.session.get(self.url + path + str(self.id))
        soup = BeautifulSoup(res.text, 'lxml')
        task_rows = soup.find("table", {"class": "table"}).find_all("tr")
        task_details = []
        for row in task_rows:
            task_details.append(row.find_all("td"))
        self.author = task_details[0][0].find("a").text
        self.description = task_details[3][0].text
        try:
            provided_files = task_details[5][0].find("ul").find_all("li")
            provided_files_list = []
            for file in provided_files:
                provided_files_dict = {"filename": file.find("a").text.split("\n")[0].strip(),
                                       "size": file.find("a").text.split("\n")[1].strip(),
                                       "link": file.find("a")["href"],
                                       }
                try:
                    provided_files_dict["description"] = file.text.split("\n")[1].strip().split("-")[1].strip()
                except IndexError:
                    provided_files_dict["description"] = ""
                provided_files_list.append(provided_files_dict)
            self.provided_files = provided_files_list
        except IndexError:
            pass
        return self


class Iserv(BaseIserv):
    def get_home(self):
        return self.session.get(f"{self.url}/iserv")

    def get_untis_substitution_plan(self, path, courses):
        """
        Gets untis substitution plan data for a given class.
        """
        # self.session.post(self.url + '/iserv/login_check', headers=headers, data=payload)
        res = self.session.get(self.url + path)
        plan_soup = BeautifulSoup(res.text, 'lxml')
        rows_collection = {}
        for schoolclass in courses:
            rows = []
            for row in plan_soup.find_all('tr', class_='list'):
                pattern = Template('(.*|^)$number.*$char.*$')
                rowlist = []
                for i in row:
                    rowlist.append(i.text)
                if len(rowlist) < 2:
                    continue
                currentclass = rowlist[4].strip()
                patternresult = re.search(pattern.safe_substitute(number=schoolclass[0], char=schoolclass[1]),
                                          currentclass)
                if patternresult and currentclass[0] in numbers or currentclass == schoolclass:
                    text = []
                    for cell in row.find_all('td'):
                        if schoolclass not in cell.text and cell.text.isspace() is not True:
                            temptext = ""
                            for test in cell.children:
                                try:
                                    for test2 in test.children:
                                        temptext = temptext + str(test2)
                                except AttributeError:
                                    temptext = temptext + test
                            text.append(temptext)
                    rows.append(text)
                rows = list(filter(lambda x: x, rows))
            rows_collection[schoolclass] = remove_duplicates(
                i if isinstance(i, list) else i for i in remove_duplicates(rows))
        date = plan_soup.find('div', class_="mon_title").text.split(" ")[0]
        week = plan_soup.find('div', class_="mon_title").text.split(" ")[-1]
        return rows_collection, date, week

    def get_next_tests_formatted(self, path="/iserv"):
        """
        Same as get_next_tests() but does not parse the data, just gives a string per test, not a dict
        """

        test_list = []

        res = self.session.get(self.url + path)
        soup = BeautifulSoup(res.text, 'lxml')

        tests = soup.find("ul", "pl mb0")

        for i in tests.find_all("li"):
            test_list.append(i.text)
        return test_list

    def get_next_tests(self, path="/iserv"):
        """
        Returns the next classtests from iserv. path is the url to search for the box.
        """
        test_list = []

        res = self.session.get(self.url + path)
        soup = BeautifulSoup(res.text, 'lxml')

        tests = soup.find("ul", "pl mb0")

        for i in tests.find_all("li"):
            entry = {}
            parsed = i.text.split(" - ")
            entry['date'] = parsed[0].strip()
            entry['time'] = parsed[1].strip()
            entry['class'] = parsed[2].strip()
            entry['subject'] = parsed[3].strip()
            test_list.append(entry)
        return test_list

    def get_tasks(self, path="/iserv/exercise?filter[status]=current"):
        """
        Returns a dict of tasks for the current user
        """

        tasks = []

        res = self.session.get(self.url + path)
        soup = BeautifulSoup(res.text, 'lxml')
        task_table = soup.find("table", {"id": "crud-table"})
        rows = task_table.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) == 6:
                task = Task(self.url, self.username, self.password)
                task.title = columns[0].find("a").text
                task.id = int(columns[0].find("a")["href"].split("/")[-1])
                task.start_date = columns[1].text
                task.end_date = columns[2].text
                if columns[3].find("span", {"class": "glyphicon-ok"}):
                    task.done = True
                else:
                    task.done = False
                task.corrections = columns[4].text
                tasks.append(task)
        return tasks
