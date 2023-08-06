"""
The MIT License (MIT)
Copyright (c) Alwin Lohrie (Niwla23)
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from bs4 import BeautifulSoup, element

from iservscrapping.errors import WrongContentError


class UntisScrapper:
    """
    Args:
        html (str): The HTML to parse
    Attributes:
        html (str): The HTML to parse
        soup (str): The Soup of the HTML
        content_header_list (str): Ordered list of headers to match the fields from the table
    A scrapper to parse Untis substitution plans. you will most of the time want to use
    :exc:`Iserv.get_untis_substitution_plan`
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')
        self.content_header_list = [
            "time",
            "subject",
            "teacher",
            "text",
            "course",
            "room",
        ]

    def scrape(self):
        """
        Raises:
            WrongContentError: The HTML passed was not in the form expected.
        """
        try:
            header = self.soup.select_one(".mon_title").get_text().split(" ")
        except AttributeError as error:
            raise WrongContentError(
                "Content was not parsable."
                "Since Iserv is to dumb to throw a 404, we can only guess about this.") from error
        date = header[0]
        week = header[-1]

        current_class = "0b118b33-d1e4-4579-8055-fa5230d0c34b"
        parsed_plan = {}
        content_table = list(self.soup.select_one(".mon_list"))
        for row in content_table:
            if len(row) == 6:
                parsed_row = {}
                if current_class not in parsed_plan.keys():
                    parsed_plan[current_class] = []
                for i, column in enumerate(row):
                    parsed_row[self.content_header_list[i]] = column.text.strip()
                parsed_plan[current_class].append(parsed_row)
            elif len(row) == 1:
                first_element = list(row)[0]
                if isinstance(first_element, element.Tag):
                    current_class = list(row)[0].text.split(" ")[0]
        try:
            del parsed_plan['0b118b33-d1e4-4579-8055-fa5230d0c34b']
        except KeyError:
            pass
        return parsed_plan, date, week
