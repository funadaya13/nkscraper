# -*- coding: utf-8 -*-
""" オッズスクレイピングAPIモジュール
"""

from __future__ import annotations

# nkscraper
from nkscraper.utils import NKScraperLogger, InvalidValueError, TableNotFoundError, TableIndexError, NKScraperHelper
from nkscraper.common import NetkeibaCategory, NetkeibaContents, NetkeibaRequests
from nkscraper.url import OddsURL

# build-in
import json

# for type declaration only
from nkscraper.url import NetkeibaURL
from logging import Logger
from bs4 import BeautifulSoup


class OddsAPI():
    """ オッズスクレイピングAPIクラス
    """

    __ERR_MESSAGE_01: str = 'NetkeibaContentsがオッズではありません. category: {}'
    __ERR_MESSAGE_02: str = 'オッズを取得できませんでした. 馬券の販売が開始されていない可能性があります. URL: {}'
    __ERR_MESSAGE_03: str = '不適切な馬番が入力されました. umaban: {}, URL: {}'
    __WARN_MESSAGE_0301: str = 'オッズを取得できませんでした. 出走取消馬の可能性があります.'
    __WARN_MESSAGE_0302: str = '単勝人気を取得できませんでした. 出走取消馬の可能性があります.'

    def __init__(self, contents: NetkeibaContents) -> None:
        """ コンストラクタ

        Args:
            contents (NetkeibaContents): netkeiba Webページコンテンツ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__helper: NKScraperHelper = NKScraperHelper()

        if contents.category != NetkeibaCategory.ODDS:
            message: str = OddsAPI.__ERR_MESSAGE_01.format(contents.category)
            self.__logger.error(message)
            raise InvalidValueError(message)

        self.__url: str = contents.url
        self.__soup: BeautifulSoup = contents.soup
        self.__race_id: int = self.__helper.get_id_from_url(contents.url)
        self.__odds_json: dict = self.__scrape_odds_json()
        self.__tansho_odds_json: dict = self.__odds_json['1']
        self.__num_horse: int = len(self.__tansho_odds_json)

    @staticmethod
    def create(race_id: int) -> OddsAPI:
        """ オッズスクレイピングAPIを作成する

        Args:
            race_id (int): netkeiba レースID

        Returns:
            OddsAPI: オッズスクレイピングAPI
        """
        return OddsAPI.create_by_list([race_id])[0]

    @staticmethod
    def create_by_list(race_id_list: list[int]) -> list[OddsAPI]:
        """ オッズスクレイピングAPIを作成する

        Args:
            race_id_list (list[int]): netkeiba レースID配列

        Returns:
            list[OddsAPI]: オッズスクレイピングAPI配列
        """
        # OddsURLの作成
        url_list: list[NetkeibaURL] = [OddsURL(race_id) for race_id in race_id_list]
        # 出馬表 NetkeibaContents の作成
        reqests: NetkeibaRequests = NetkeibaRequests()
        contents_list: list[NetkeibaContents] = reqests.get_by_list(url_list)
        # オッズスクレイピングAPIを作成して返却
        return [OddsAPI(contents) for contents in contents_list]

    def scrape_race_id(self) -> int:
        """ レースIDをスクレイピングする.

        Returns:
            int: netkeiba レースID
        """
        return self.__race_id

    def get_num_horse(self) -> int:
        """ レース出走頭数を取得する

        Returns:
            int: レース出走頭数
        """
        return self.__num_horse

    def scrape_tansho_odds(self, umaban: int) -> float | None:
        """ 単勝オッズをスクレイピングする

        Args:
            umaban (int): 馬番

        Returns:
            float | None: 単勝オッズ (出走取消馬の場合はNoneを返す)
        """
        self.__validate_umaban(umaban)
        key: str = str(umaban).zfill(2)
        data: list = self.__tansho_odds_json[key]
        tansho_odds: float = float(data[0])
        # 出走取消馬の場合
        if tansho_odds < 0:
            self.__logger.warning(self.__WARN_MESSAGE_0301)
            return None
        return tansho_odds

    def scrape_tansho_rank(self, umaban: int) -> int | None:
        """ 単勝人気をスクレイピングする

        Args:
            umaban (int): 馬番

        Returns:
            int | None: 単勝人気 (出走取消馬の場合はNoneを返す)
        """
        self.__validate_umaban(umaban)
        key: str = str(umaban).zfill(2)
        data: list = self.__tansho_odds_json[key]
        tansho_rank: int = int(data[2])
        # 出走取消馬の場合
        if tansho_rank == 9999:
            self.__logger.warning(self.__WARN_MESSAGE_0302)
            return None
        return tansho_rank


    # Private Functions for Scrape Odds JSON
    def __scrape_odds_json(self) -> dict:
        """ オッズ情報を保持するJSONオブジェクトをスクレイピングする
        """
        odds_string: str = str(self.__soup.find('p').contents[0])
        odds_json: dict = json.loads(odds_string)
        if odds_json['status'] == 'NG' or odds_json['status'] == 'yoso':
            message: str = OddsAPI.__ERR_MESSAGE_02.format(self.__url)
            self.__logger.error(message)
            raise TableNotFoundError(message)
        return odds_json['data']['odds']

    # Private Functions for Validate umaban ----------------------------------
    def __validate_umaban(self, umaban: int) -> None:
        """ 馬番をチェックする
        """
        min_umaban: int = 1
        max_umaban: int = self.__num_horse
        if umaban < min_umaban or umaban > max_umaban:
            message: str = OddsAPI.__ERR_MESSAGE_03.format(umaban, self.__url)
            self.__logger.error(message)
            raise TableIndexError(message)
