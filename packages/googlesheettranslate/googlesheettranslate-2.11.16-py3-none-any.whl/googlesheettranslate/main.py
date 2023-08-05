import csv
import time
from typing import Iterable, Any

import requests
from bs4 import BeautifulSoup

from googlesheettranslate.Err import TransformError
from googlesheettranslate.transformers.Jsi18n import Jsi18n
from googlesheettranslate.transformers.itransformer import InterfaceTransform

statement = 'End : {}, IO File {}'


class Reader:
    Transformers: {
        "i18n": Jsi18n
    }

    def __init__(self):
        self.key = "KEY"
        self.column = "CN"
        self.transformerEngine = False
        self._output_file_format = False
        self._defaultEncoding = "utf8"

    def setKey(self, _key: str) -> "Reader":
        self.key = _key
        return self

    def setLang(self, tag: str) -> "Reader":
        self.column = tag
        return self

    def useEngine(self, tag: str) -> "Reader":
        if tag in self.Transformers:
            self.transformerEngine = self.Transformers[tag]
        else:
            self.transformerEngine = self.Transformers["i18n"]
        return self

    def Loop(self, reader: Iterable[Iterable[Any]]):
        if not self.transformerEngine:
            raise TransformError
        if not self._output_file_format:
            if isinstance(self.transformerEngine, InterfaceTransform):
                self._output_file_format = self.transformerEngine.autoFileName()
            else:
                raise TransformError

        for row in reader:
            print(row)

        return self

    def writeFile(self, content, filename):
        fo = open(filename, "w")
        fo.write(content)
        fo.close()
        print(statement.format(time.ctime(), filename))

    def SortAskOut(self):
        """
        self.writeFile("", self.exchange_data_output)
        with opens(self.downline_batch) as lines:
            for line in lines:
                num = line.translate(str.maketrans('', '', ' \n\t\r'))
                self.NewSort().TradeSortByNumber(num)
                file_object = open(self.exchange_data_output, 'a')
                if len(self.list_downline_people) > 0:
                    file_object.write("[{}]:\n".format(num))
                    file_object.write('\n'.join(self.list_downline_people))
                else:
                    file_object.write("[{}]: NO MEMBERS \n".format(num))
                file_object.close()"""


class lib:
    """
    featured translation service does not need to use creditentials
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest'
    }
    proxies = {
        "http": "socks5://127.0.0.1:1086",
        "https": "socks5://127.0.0.1:1086",
    }

    def __init__(self):
        self.exportedSheetUrl = ""
        self.html = ""
        self.tab = ""
        self.engine_name = ""
        self.tab_content = dict()
        self.saveToCvs = False
        self._readerEngine = Reader()

    def builderCvs(self, enabled: bool) -> "lib":
        self.saveToCvs = enabled
        return self

    def builderTransformers(self, engine_name: str) -> "lib":
        self.engine_name = engine_name
        return self

    def builderReader(self, module_reader: Reader) -> "lib":
        self._readerEngine = module_reader
        return self

    def builderMeta(self, url: str, tabname: str) -> "lib":
        self.exportedSheetUrl = url
        self.tab = tabname
        return self

    def run(self, proxies=False):

        if proxies == True:
            self.html = requests.get(
                self.exportedSheetUrl,
                headers=self.headers,
                proxies=self.proxies
            ).text
        else:
            self.html = requests.get(
                self.exportedSheetUrl,
                headers=self.headers
            ).text

        soup = BeautifulSoup(self.html, "lxml")
        tables = soup.find_all("table")
        index = 0
        for table in tables:
            self.tab_content = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")]
            if self.saveToCvs:
                with open(str(index) + ".csv", "w") as f:
                    wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                    wr.writerows(self.tab_content)

            self._readerEngine.useEngine(self.engine_name).Loop(self.tab_content)

            index = index + 1
