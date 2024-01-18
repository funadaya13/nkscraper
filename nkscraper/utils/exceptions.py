# -*- coding: utf-8 -*-
""" nkscraper 例外モジュール
"""


class NKScraperException(Exception):
    """ nkscraper 例外基底クラス
    """
    pass

class InvalidValueError(NKScraperException):
    """ 不適切な値が入力された際に投げるエラー
    """
    pass

class NetkeibaRequestsError(NKScraperException):
    """ netkeiba Webページの取得に失敗した際に投げるエラー
    """
    pass

class TableNotFoundError(NKScraperException):
    """ 対象のテーブルが見つからなかった際に投げるエラー
    """
    pass

class TableIndexError(NKScraperException):
    """ 不適切な表インデックスが入力された際に投げるエラー
    """
    pass
