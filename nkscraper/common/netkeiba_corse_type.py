# -*- coding: utf-8 -*-
""" netkeiba コース種別モジュール
"""

from __future__ import annotations

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

    @staticmethod
    def from_course_type(course_type: str) -> NetkeibaCorseType:
        """ コース種別から netkeiba コース種別を作成する.
        """
        if course_type == '芝':
            return NetkeibaCorseType.SHIBA
        elif course_type == 'ダ':
            return NetkeibaCorseType.DIRT
        elif course_type == '障':
            return NetkeibaCorseType.JUMP
