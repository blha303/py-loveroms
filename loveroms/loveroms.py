#!/usr/bin/env python
from __future__ import print_function
import requests
import sys
import time
import math
from bs4 import BeautifulSoup as Soup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
ROOT = "https://www.loveroms.com/"

search_params = {
        "sEcho": 3,
        "iColumns": 5,
        "sColumns": "%2C%2C%2C%2C",
        "iDisplayStart": 0,
        "iDisplayLength": 15,
        "mDataProp_0": 0,
        "sSearch_0": "",
        "bRegex_0": "false",
        "bSearchable_0": "true",
        "bSortable_0": "true",
        "mDataProp_1": 1,
        "sSearch_1": 0,
        "bRegex_1": "false",
        "bSearchable_1": "true",
        "bSortable_1": "true",
        "mDataProp_2": 2,
        "sSearch_2": "",
        "bRegex_2": "false",
        "bSearchable_2": "true",
        "bSortable_2": "true",
        "mDataProp_3": 3,
        "sSearch_3": "",
        "bRegex_3": "false",
        "bSearchable_3": "true",
        "bSortable_3": "true",
        "mDataProp_4": 4,
        "sSearch_4": "",
        "bRegex_4": "false",
        "bSearchable_4": "true",
        "bSortable_4": "true",
        "sSearch": "",
        "bRegex": "false",
        "iSortCol_0": 4,
        "sSortDir_0": "desc",
        "iSortingCols": 1
}

def get_parser():
    if sys.version_info < (2,7,3) and sys.version_info < (3,2,2):
        return "lxml"
    return "html.parser"

class Result:
    def __init__(self, data):
        self._info, self.platform, self.genre, self.rating, self.download_count, self._unknown1, self._unknown2 = data
        self._info = Soup(self._info, get_parser())
        try:
            self.flag = [_ for _ in self._info.find("span", {"class": "flags"}).attrs["class"] if _ != "flags"][0].upper()
        except IndexError:
            self.flag = "??"
        self.name = self._info.find("a").text.strip()
        self.download = "https:" + self._info.find("a").attrs["href"]

    def __repr__(self):
        return "[{}] {} ({}) - {} ({})".format(self.flag, self.name, self.platform, self.download_count, self.rating)

def search(term):
    search_params.update({"sSearch": term, "_": math.floor(time.time()*1000)})
    print("Getting results... (this can take a while)", file=sys.stderr)
    data = requests.get(ROOT + "query.php", params=search_params).json()["aaData"]
    print("Processing results...", file=sys.stderr)
    results = [Result(d) for d in data]
    return results

def get_download_url(page_url):
    page = Soup(requests.get(page_url).text, get_parser())
    return page.find("div", {"id": "didnt-work"}).a.attrs["href"]

def get_download_cmd(page_url):
    page = Soup(requests.get(page_url).text, get_parser())
    dl_redir = page.find("div", {"id": "didnt-work"}).a.attrs["href"]
    dl = requests.get(dl_redir, allow_redirects=False)
    dl_url = dl.headers["Location"]
    cookies = dl.headers["Set-Cookie"]
    return ["curl", dl_url, "-g", "--cookie", cookies, "-H", "User-Agent: " + UA, "-H", "Referer: " + ROOT, "-o", page.table.findAll('td')[1].text.strip()]

def prompt(question, response_type=int):
    if not sys.stdout.isatty():
        sys.exit(2)
    index = None
    while index is None:
        try:
            index = response_type(input(question))
        except ValueError:
            print("Try again. Has to be a number.", file=sys.stderr)
        except IndexError:
            print("Check your input. Ctrl-C to back out", file=sys.stderr)
        except KeyboardInterrupt:
            print("\nAborted", file=sys.stderr)
            sys.exit(127)
    return index

def main():
    from argparse import ArgumentParser
    import subprocess
    parser = ArgumentParser(prog="loveroms")
    parser.add_argument("search", help="Search term")
    args = parser.parse_args()
    results = search(args.search)
    print("\n".join("{0}: {1}".format(n, result) for n, result in enumerate(results)))
    result = results[prompt("enter your choice: ")]
    cmd = get_download_cmd(result.download)
    print("Downloading " + cmd[-1], file=sys.stderr)
    process = subprocess.Popen(get_download_cmd(result.download))
    process.wait()
    return 0

if __name__ == "__main__":
    sys.exit(main())
