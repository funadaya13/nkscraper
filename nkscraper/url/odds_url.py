# -*- coding: utf-8 -*-
""" netkeiba オッズURLモジュール
"""

# nkscraper
from nkscraper.utils import NKScraperLogger, InvalidValueError
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL

# built-in
from logging import Logger


class OddsURL(NetkeibaURL):
    """ netkeiba オッズURLクラス
    """

    URL: str = 'https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&action=init&race_id='
    __ERR_MESSAGE_01: str = 'レースIDは12桁の正の整数を入力してください. race_id: {}'

    def __init__(self, race_id: int) -> None:
        """ コンストラクタ

        Args:
            race_id (int): netkeiba レースID
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__validate_race_id(race_id)
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

    def __validate_race_id(self, race_id: int) -> None:
        """ レースIDバリデーション
        """

        def raise_err():
            message: str = OddsURL.__ERR_MESSAGE_01.format(race_id)
            self.__logger.error(message)
            raise InvalidValueError(message)

        if not isinstance(race_id, int):
            raise_err()
        if race_id < 0:
            raise_err()
        if len(str(race_id)) != 12:
            raise_err()
