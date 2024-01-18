# -*- coding: utf-8 -*-
""" netkeiba 調教評価URLモジュール
"""

# nkscraper
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL


class TrainingEvaluationURL(NetkeibaURL):
    """ netkeiba 調教評価URLクラス
    """

    URL: str = 'https://race.netkeiba.com/race/oikiri.html?race_id='

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
        return NetkeibaCategory.TRAINING_EVALUATION

    @property
    def url(self) -> str:
        """ netkeiba 調教評価URL

        Returns:
            str: netkeiba 調教評価URL
        """
        return f'{TrainingEvaluationURL.URL}{self.__race_id}'
