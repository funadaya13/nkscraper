# -*- coding: utf-8 -*-
""" netkeiba オッズURLモジュール
"""

# nkscraper
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL


class OddsURL(NetkeibaURL):
    """ netkeiba オッズURLクラス
    """

    URL: str = 'https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&action=init&race_id='

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
        return NetkeibaCategory.ODDS

    @property
    def url(self) -> str:
        """ netkeiba オッズURL

        Returns:
            str: netkeiba オッズURL
        """
        return f'{OddsURL.URL}{self.__race_id}'
