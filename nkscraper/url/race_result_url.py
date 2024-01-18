# -*- coding: utf-8 -*-
""" netkeiba レース結果URLモジュール
"""

# nkscraper
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL


class RaceResultURL(NetkeibaURL):
    """ netkeiba レース結果URLクラス
    """

    URL: str = 'https://race.netkeiba.com/race/result.html?race_id='

    def __init__(self, race_id: int) -> None:
        """ コンストラクタ

        Args:
            race_id (int): レースID
        """
        self.__race_id: int = race_id

    @property
    def category(self) -> NetkeibaCategory:
        """ netkeiba Webページカテゴリー

        Returns:
            NetkeibaCategory: netkeiba Webページカテゴリー
        """
        return NetkeibaCategory.RACE_RESULT

    @property
    def url(self) -> str:
        """ netkeiba レース結果URL

        Returns:
            str: netkeiba レース結果URL
        """
        return f'{RaceResultURL.URL}{self.__race_id}'
