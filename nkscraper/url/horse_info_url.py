# -*- coding: utf-8 -*-
""" netkeiba 競走馬情報URLモジュール
"""

# nkscraper
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL


class HorseInfoURL(NetkeibaURL):
    """ netkeiba 競走馬情報URLクラス
    """

    URL: str = 'https://db.netkeiba.com/horse/'

    def __init__(self, horse_id: int) -> None:
        """ コンストラクタ

        Args:
            horse_id (int): netkeiba 競走馬ID
        """
        self.__horse_id: int = horse_id

    @property
    def category(self) -> NetkeibaCategory:
        """ netkeiba Webページカテゴリー

        Returns:
            NetkeibaCategory: netkeiba Webページカテゴリー
        """
        return NetkeibaCategory.HORSE_INFO

    @property
    def url(self) -> str:
        """ netkeiba 競走馬情報URL

        Returns:
            str: netkeiba 競走馬情報URL
        """
        return f'{HorseInfoURL.URL}{self.__horse_id}'
