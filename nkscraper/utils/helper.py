# -*- coding: utf-8 -*-
""" nkscraper ヘルパーモジュール
"""

# nkscraper
from nkscraper.utils import NKScraperLogger
from nkscraper.common import NetkeibaFieldID

# build-in
import re
import sys

# for type declaration only
from logging import Logger


class NKScraperHelper():
    """ nkscraper ヘルパークラス
    """

    __ERR_MESSAGE_01: str = '競馬場名を NetkeibaFieldID に変換できませんでした.'

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

    def convert_field_name_to_id(self, field_name: str) -> NetkeibaFieldID:
        """ 競馬場名を NetkeibaFieldID に変換する.

        Args:
            field_name (str): 競馬場名

        Returns:
            NetkeibaFieldID: NetkeibaFieldID
        """
        if field_name == '札幌':
            return NetkeibaFieldID.SAPPORO
        elif field_name == '函館':
            return NetkeibaFieldID.HAKODATE
        elif field_name == '福島':
            return NetkeibaFieldID.FUKUSHIMA
        elif field_name == '新潟':
            return NetkeibaFieldID.NIIGATA
        elif field_name == '東京':
            return NetkeibaFieldID.TOKYO
        elif field_name == '中山':
            return NetkeibaFieldID.NAKAYAMA
        elif field_name == '中京':
            return NetkeibaFieldID.CHUKYO
        elif field_name == '京都':
            return NetkeibaFieldID.KYOTO
        elif field_name == '阪神':
            return NetkeibaFieldID.HANSHIN
        elif field_name == '小倉':
            return NetkeibaFieldID.KOKURA
        else:
            self.__logger.error(NKScraperHelper.__ERR_MESSAGE_01)
            sys.exit()
