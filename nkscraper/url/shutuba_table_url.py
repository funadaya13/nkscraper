# -*- coding: utf-8 -*-
""" netkeiba 出馬表URLモジュール
"""

# nkscraper
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL


class ShutubaTableURL(NetkeibaURL):
    """ netkeiba 出馬表URLクラス
    """

    URL: str = 'https://race.netkeiba.com/race/shutuba.html?race_id='

    def __init__(self, race_id: int) -> None:
        """ コンストラクタ

        Args:
            race_id (int): netkeiba レースID
        """
        self.__race_id: int = race_id

    @property
    def category(self) -> NetkeibaCategory:
        """ netkeiba Webページカテゴリー

        Returns:
            NetkeibaCategory: netkeiba Webページカテゴリー
        """
        return NetkeibaCategory.SHUTUBA_TABLE

    @property
    def url(self) -> str:
        """ netkeiba 出馬表URL

        Returns:
            str: netkeiba 出馬表URL
        """
        return f'{ShutubaTableURL.URL}{self.__race_id}'
