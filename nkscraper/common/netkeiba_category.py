# -*- coding: utf-8 -*-
""" netkeiba Webページカテゴリーモジュール
"""

# built-in
from enum import Enum


class NetkeibaCategory(Enum):
    """ netkeiba Webページカテゴリー
    """
    SHUTUBA_TABLE = 0  # 出馬表
    RACE_RESULT = 10  # レース結果
    ODDS = 20  # オッズ
    TRAINING_EVALUATION = 30  # 調教評価
    HORSE_INFO = 40  # 馬情報
    SEARCHED_RACE = 50  # レース検索結果
