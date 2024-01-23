# -*- coding: utf-8 -*-
""" nkscraper ヘルパーモジュール
"""

# nkscraper
from nkscraper.utils import NKScraperLogger, InvalidValueError
from nkscraper.common import NetkeibaFieldID

# build-in
import re

# for type declaration only
from logging import Logger


class NKScraperHelper():
    """ nkscraper ヘルパークラス
    """

    def __init__(self) -> None:
        """ コンストラクタ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)

    def arrange_string(self, string: str) -> str:
        """ 文字列を整形する

        Args:
            string (str): 文字列

        Returns:
            str: 整形された文字列
        """
        return string.replace(' ', '').replace('\n', '')

    def get_id_from_url(self, url: str) -> int:
        """ netkeiba URL から ID を取得する.

        Args:
            url (str): netkeiba URL

        Returns:
            int: netkeiba ID
        """
        match = re.findall(r'\d+', url)
        return int(match[-1])
