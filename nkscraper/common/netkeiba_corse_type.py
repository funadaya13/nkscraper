# -*- coding: utf-8 -*-
""" netkeiba コース種別モジュール
"""

# built-in
from enum import Enum


class NetkeibaCorseType(Enum):
    """ netkeiba コース種別
    """
    SHIBA: dict = 1
    DIRT: dict = 2
    JUMP: dict = 3

    @property
    def name(self) -> str:
        """
        """
        if self == NetkeibaCorseType.SHIBA:
            return '芝'
        elif self == NetkeibaCorseType.DIRT:
            return 'ダ'
        elif self == NetkeibaCorseType.JUMP:
            return '障' 
