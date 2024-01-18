# -*- coding: utf-8 -*-
""" netkeiba コース種別モジュール
"""

# built-in
from enum import Enum


class NetkeibaCorseType(Enum):
    """ netkeiba コース種別
    """
    SHIBA: dict = {'id': 1, 'display': '芝'}
    DIRT: dict = {'id': 2, 'display': 'ダ'}
    JUMP: dict = {'id': 3, 'display': '障'}
