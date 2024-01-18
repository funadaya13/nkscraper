# -*- coding: utf-8 -*-
""" netkeiba HTTP Requests通信モジュール
"""

# nkscraper
from nkscraper.utils import NKScraperLogger, NetkeibaRequestsError

# build-in
import time
import asyncio

# OSS
from bs4 import BeautifulSoup
import aiohttp

# for type declaration only
from nkscraper.common import NetkeibaContents
from nkscraper.url import NetkeibaURL
from logging import Logger


class NetkeibaRequests():
    """ netkeiba HTTP Requests通信クラス
    """

    __ERR_MESSAGE_01: str = 'netkeiba Webページの読み込みに失敗しました. URL: {}'

    def __init__(self) -> None:
        """ コンストラクタ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)

    def get(self, url: NetkeibaURL) -> NetkeibaContents:
        """ netkeiba HTTP通信 GET API

        Args:
            url (NetkeibaURL): netkaiba URL

        Returns:
            NetkeibaContents: netkeiba Webページコンテンツ
        """
        return asyncio.run(self.__get_process([url]))[0]

    def get_by_list(self, url_list: list[NetkeibaURL]) -> list[NetkeibaContents]:
        """ netkeiba HTTP通信 GET API

        Args:
            url_list (list[NetkeibaURL]): NetkaibaURL配列

        Returns:
            list[NetkeibaContents]: netkeiba Webページコンテンツ配列
        """
        return asyncio.run(self.__get_process(url_list))

    async def __get_process(self, url_list: list[NetkeibaURL]) -> list[NetkeibaContents]:
        """ netkeiba HTTP通信 GET関数

        引数に渡された全ての netkeiba Webページコンテンツを非同期に取得する.

        Args:
            url_list (list[NetkeibaURL]): NetkaibaURL配列

        Returns:
            list[NetkeibaContents]: netkeiba Webページコンテンツ配列
        """

        async def __async_process(session: aiohttp.ClientSession, url: NetkeibaURL) -> NetkeibaContents:
            """ 非同期処理
            """
            try:
                async with session.get(url.url) as response:
                    html_byte = await response.read()
                    soup = BeautifulSoup(html_byte, 'lxml')

                    return NetkeibaContents(url, soup)

            except Exception as e:
                message: str = NetkeibaRequests.__ERR_MESSAGE_01.format(url.url)
                self.__logger.error(message)
                raise NetkeibaRequestsError(message) from None

        process_start: float = time.perf_counter()

        async with aiohttp.ClientSession() as session:
            # 実行関数を定義
            tasks = [
                asyncio.ensure_future(
                    __async_process(session, url)) for url in url_list
            ]

            netkeiba_contents_list: list[NetkeibaContents] = await asyncio.gather(*tasks)

        process_end: float = time.perf_counter()
        process_time: float = process_end - process_start
        self.__logger.info(f'{len(url_list)} requests. Time: {process_time} [sec]')

        return netkeiba_contents_list
