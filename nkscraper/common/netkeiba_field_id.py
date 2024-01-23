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
    OBIHIRO: str = '65'
    MONBETSU: str = '30'
    MORIOKA: str = '35'
    MIZUSAWA: str = '36'
    URAWA: str = '42'
    FUNABASHI: str = '43'
    OI: str = '44'
    KAWASAKI: str = '45'
    KANAZAWA: str = '46'
    KASAMATSU: str = '47'
    NAGOYA: str = '48'
    SONODA: str = '50'
    HIMEJI: str = '51'
    KOCHI: str = '54'
    SAGA: str = '55'
