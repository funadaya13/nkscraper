# -*- coding: utf-8 -*-
""" netkeiba 競走馬情報URLモジュール
"""

# nkscraper
from nkscraper.utils import InvalidValueError, NKScraperLogger
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL

# built-in
from logging import Logger


class HorseInfoURL(NetkeibaURL):
    """ netkeiba 競走馬情報URLクラス
    """

    URL: str = 'https://db.netkeiba.com/horse/'
    __ERR_MESSAGE_01: str = '競走馬IDは10桁の正の整数を入力してください. horse_id: {}'

    def __init__(self, horse_id: int) -> None:
        """ コンストラクタ

        Args:
            horse_id (int): netkeiba 競走馬ID
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__validate_horse_id(horse_id)
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

    def __validate_horse_id(self, horse_id: int) -> None:
        """ 競走馬IDバリデーション
        """

        def raise_err():
            message: str = HorseInfoURL.__ERR_MESSAGE_01.format(horse_id)
            self.__logger.error(message)
            raise InvalidValueError(message)

        if not isinstance(horse_id, int):
            raise_err()
        if horse_id < 0:
            raise_err()
        if len(str(horse_id)) != 10:
            raise_err()
