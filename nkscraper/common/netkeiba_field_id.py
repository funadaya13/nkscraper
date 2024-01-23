# -*- coding: utf-8 -*-
""" netkeiba 競馬場IDモジュール
"""

from __future__ import annotations

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

    @property
    def name(self) -> str:
        """ 競馬場名

        Returns:
            str: 競馬場名
        """
        if self == NetkeibaFieldID.SAPPORO:
            return '札幌'
        elif self == NetkeibaFieldID.HAKODATE:
            return '函館'
        elif self == NetkeibaFieldID.FUKUSHIMA:
            return '福島'
        elif self == NetkeibaFieldID.NIIGATA:
            return '新潟'
        elif self == NetkeibaFieldID.TOKYO:
            return '東京'
        elif self == NetkeibaFieldID.NAKAYAMA:
            return '中山'
        elif self == NetkeibaFieldID.CHUKYO:
            return '中京'
        elif self == NetkeibaFieldID.KYOTO:
            return '京都'
        elif self == NetkeibaFieldID.HANSHIN:
            return '阪神'
        elif self == NetkeibaFieldID.KOKURA:
            return '小倉'
        elif self == NetkeibaFieldID.OBIHIRO:
            return '帯広'
        elif self == NetkeibaFieldID.MONBETSU:
            return '門別'
        elif self == NetkeibaFieldID.MORIOKA:
            return '盛岡'
        elif self == NetkeibaFieldID.MIZUSAWA:
            return '水沢'
        elif self == NetkeibaFieldID.URAWA:
            return '浦和'
        elif self == NetkeibaFieldID.FUNABASHI:
            return '船橋'
        elif self == NetkeibaFieldID.OI:
            return '大井'
        elif self == NetkeibaFieldID.KAWASAKI:
            return '川崎'
        elif self == NetkeibaFieldID.KANAZAWA:
            return '金沢'
        elif self == NetkeibaFieldID.KASAMATSU:
            return '笠松'
        elif self == NetkeibaFieldID.NAGOYA:
            return '名古屋'
        elif self == NetkeibaFieldID.SONODA:
            return '園田'
        elif self == NetkeibaFieldID.HIMEJI:
            return '姫路'
        elif self == NetkeibaFieldID.KOCHI:
            return '高知'
        elif self == NetkeibaFieldID.SAGA:
            return '佐賀'

    @staticmethod
    def from_field_name(field_name: str) -> NetkeibaFieldID:
        """ 競馬場名から netkeiba 競馬場IDを作成する

        Args:
            field_name (str): 競馬場名

        Returns:
            NetkeibaFieldID: netkeiba 競馬場ID
        """
        if field_name == '札幌':
            return NetkeibaFieldID.SAPPORO
        elif field_name == '函館':
            return NetkeibaFieldID.HAKODATE
        elif field_name == '福島':
            return NetkeibaFieldID.FUKUSHIMA
        elif field_name == '新潟':
            return NetkeibaFieldID.NIIGATA
        elif field_name == '東京':
            return NetkeibaFieldID.TOKYO
        elif field_name == '中山':
            return NetkeibaFieldID.NAKAYAMA
        elif field_name == '中京':
            return NetkeibaFieldID.CHUKYO
        elif field_name == '京都':
            return NetkeibaFieldID.KYOTO
        elif field_name == '阪神':
            return NetkeibaFieldID.HANSHIN
        elif field_name == '小倉':
            return NetkeibaFieldID.KOKURA
        elif field_name == '帯広':
            return NetkeibaFieldID.OBIHIRO
        elif field_name == '門別':
            return NetkeibaFieldID.MONBETSU
        elif field_name == '盛岡':
            return NetkeibaFieldID.MORIOKA
        elif field_name == '水沢':
            return NetkeibaFieldID.MIZUSAWA
        elif field_name == '浦和':
            return NetkeibaFieldID.URAWA
        elif field_name == '船橋':
            return NetkeibaFieldID.FUNABASHI
        elif field_name == '大井':
            return NetkeibaFieldID.OI
        elif field_name == '川崎':
            return NetkeibaFieldID.KAWASAKI
        elif field_name == '金沢':
            return NetkeibaFieldID.KANAZAWA
        elif field_name == '笠松':
            return NetkeibaFieldID.KASAMATSU
        elif field_name == '名古屋':
            return NetkeibaFieldID.NAGOYA
        elif field_name == '園田':
            return NetkeibaFieldID.SONODA
        elif field_name == '姫路':
            return NetkeibaFieldID.HIMEJI
        elif field_name == '高知':
            return NetkeibaFieldID.KOCHI
        elif field_name == '佐賀':
            return NetkeibaFieldID.SAGA
