# -*- coding: utf-8 -*-
""" レース検索結果スクレイピングAPIモジュール
"""

from __future__ import annotations

# nkscraper
from nkscraper.utils import NKScraperException, NKScraperLogger, NKScraperHelper
from nkscraper.common import NetkeibaCategory, NetkeibaContents, NetkeibaRequests, NetkeibaFieldID
from nkscraper.url import SearchedRaceURL

# build-in
from datetime import datetime
import sys

# for type declaration only
from nkscraper.url import NetkeibaURL
from logging import Logger
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import date


class SearchedRaceAPI():
    """ レース検索結果スクレイピングAPIクラス
    """

    __ERR_MESSAGE_0501: str = 'NetkeibaContentsがレース検索結果ではありません.'
    __ERR_MESSAGE_0502: str = '該当するレースが見つかりませんでした.'

    def __init__(self, contents: NetkeibaContents) -> None:
        """ コンストラクタ

        Args:
            contents (NetkeibaContents): netkeiba Webページコンテンツ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__helper: NKScraperHelper = NKScraperHelper()

        if contents.category != NetkeibaCategory.SEARCHED_RACE:
            self.__logger.error(SearchedRaceAPI.__ERR_MESSAGE_0501)
            sys.exit()

        self.__soup: BeautifulSoup = contents.soup
        self.__race_table: list[Tag] = self.__scrape_race_table()

    @staticmethod
    def create(race_name: str, field_id: NetkeibaFieldID, 
               distance: int, corse_type: str, start_year: int,
               start_month: int, end_year: int, end_month: int) -> SearchedRaceAPI:
        """ レース検索結果スクレイピングAPIを作成する

        Args:
            race_name (str): レース名
            field_id (NetkeibaFieldID): netkeiba 競馬場ID
            distance (int): 距離
            corse_type (str): '芝' or 'ダ'
            start_year (int): 検索開始年
            start_month (int): 検索開始月
            end_year (int): 検索終了年
            end_month (int): 検索終了年

        Returns:
            SearchedRaceAPI: レース検索結果スクレイピングAPI
        """
        # SearchedRaceURLの作成
        url: NetkeibaURL = SearchedRaceURL(race_name, field_id, distance, corse_type,
                                           start_year, start_month, end_year, end_month)
        # レース検索結果 NetkeibaContents の作成
        reqests: NetkeibaRequests = NetkeibaRequests()
        contents: NetkeibaContents = reqests.get(url)
        # レース検索結果スクレイピングAPIを作成して返却
        return SearchedRaceAPI(contents)

    # Public API Functions ----------------------------------------------------
    def get_num_race(self) -> int:
        """ 検索該当レース数を取得する

        Returns:
            int: 検索該当レース数
        """
        return len(self.__race_table)

    def scrape_race_date(self, index: int) -> date:
        """ レース開催日をスクレイピングする

        Returns:
            date: レース開催日
        """
        td_list: list[Tag] = self.__race_table[index].find_all('td')
        date_str: str = td_list[0].a.contents[0]
        return datetime.strptime(date_str, '%Y/%m/%d').date()

    def scrape_race_name(self, index: int) -> str:
        """ レース名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: レース名
        """
        td_list: list[Tag] = self.__race_table[index].find_all('td')
        race_name: str = str(td_list[4].a.contents[0])
        return self.__helper.arrange_string(race_name)

    def scrape_race_id(self, index: int) -> int:
        """ レースIDをスクレイピングする.

        Args:
            index (int): 表インデックス

        Returns:
            int: netkeiba レースID
        """
        td_list: list[Tag] = self.__race_table[index].find_all('td')
        url: str = str(td_list[4].a.attrs['href'])
        return self.__helper.get_id_from_url(url)

    def scrape_num_race_horse(self, index: int) -> int:
        """ レース出走頭数をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: レース出走頭数
        """
        td_list: list[Tag] = self.__race_table[index].find_all('td')
        return int(td_list[7].contents[0])

    # Private Functions for Scrape Race Table ------------------------------
    def __scrape_race_table(self) -> list[Tag]:
        """ レース表をスクレイピングする
        """
        table: Tag = self.__soup.find('table', class_='race_table_01')
        # 検索該当レースがない場合
        if table is None:
            self.__logger.error(SearchedRaceAPI.__ERR_MESSAGE_0502)
            sys.exit()
        table_row_list: list[Tag] = table.findAll('tr')
        return table_row_list[1:]
