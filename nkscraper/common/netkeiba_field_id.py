# -*- coding: utf-8 -*-
""" netkeiba 競馬場IDモジュール
"""

# built-in
from enum import Enum


class NetkeibaFieldID(Enum):
    """ netkeiba 競馬場ID
    """
    SAPPORO: str = '01'
    HAKODATE: str = '02'
    FUKUSHIMA: str = '03'
    NIIGATA: str = '04'
    TOKYO: str = '05'
    NAKAYAMA: str = '06'
    CHUKYO: str = '07'
    KYOTO: str = '08'
    HANSHIN: str = '09'
    KOKURA: str = '10'
