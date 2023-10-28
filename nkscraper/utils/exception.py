# -*- coding: utf-8 -*-
""" nkscraper 例外モジュール
"""

# nkscraper
from nkscraper.utils import NKScraperLogger

# for type declaration only
from logging import Logger


class NKScraperException(Exception):
    """ nkscraper 例外クラス
    """

    __CRITICAL_MESSAGE: str = '予期せぬエラーが発生しました.'

    def __init__(self, *args) -> None:
        """ コンストラクタ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__logger.critical(NKScraperException.__CRITICAL_MESSAGE)
        super().__init__(*args)
