# -*- coding: utf-8 -*-
""" netkeiba レース検索結果URLモジュール
"""

# nkscraper
from nkscraper.utils import NKScraperLogger
from nkscraper.common import NetkeibaCategory, NetkeibaFieldID, NetkeibaCorseType
from nkscraper.url import NetkeibaURL

# built-in
import urllib

# for type declaration only
from logging import Logger


class SearchedRaceURL(NetkeibaURL):
    """ netkeiba レース検索結果URLクラス
    """

    URL: str = 'https://db.netkeiba.com/?pid=race_list&sort=date&list=100'

    def __init__(self, race_name: str, field_id: NetkeibaFieldID, 
                 distance: int, corse_type: NetkeibaCorseType, start_year: int,
                 start_month: int, end_year: int, end_month: int) -> None:
        """ コンストラクタ

        Args:
            race_name (str): レース名
            field_id (NetkeibaFieldID): netkeiba 競馬場ID
            distance (int): 距離
            corse_type (NetkeibaCorseType): netkeiba コース種別
            start_year (int): 検索開始年
            start_month (int): 検索開始月
            end_year (int): 検索終了年
            end_month (int): 検索終了月
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)

        self.__race_name: str = urllib.parse.quote(race_name, encoding='euc-jp')
        self.__field_id: str = field_id.value
        self.__distance: int = distance
        self.__corse_type: int = corse_type.name
        self.__start_year: int = start_year
        self.__start_mon: int = start_month
        self.__end_year: int = end_year
        self.__end_mon: int = end_month

    @property
    def category(self) -> NetkeibaCategory:
        """ netkeiba Webページカテゴリー

        Returns:
            NetkeibaCategory: netkeiba Webページカテゴリー
        """
        return NetkeibaCategory.SEARCHED_RACE

    @property
    def url(self) -> str:
        """ netkeiba レース検索結果URL

        Returns:
            str: netkeiba レース検索結果URL
        """
        return f'{SearchedRaceURL.URL}' + \
               f'&word={self.__race_name}' + \
               f'&track%5B%5D={self.__corse_type}' + \
               f'&start_year={self.__start_year}' + \
               f'&start_mon={self.__start_mon}' + \
               f'&end_year={self.__end_year}' + \
               f'&end_mon={self.__end_mon}' + \
               f'&jyo%5B%5D={self.__field_id}' + \
               f'&kyori%5B%5D={self.__distance}'
