# -*- coding: utf-8 -*-
""" netkeiba コース種別モジュール
"""

# built-in
from enum import Enum


class NetkeibaCorseType(Enum):
    """ netkeiba コース種別
    """
    SHIBA: int = 1
    DIRT: int = 2
    JUMP: int = 3

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
