# -*- coding: utf-8 -*-
""" netkeiba URLモジュール
"""

# built-in
from abc import ABC, abstractmethod

# for type declaration only
from nkscraper.common import NetkeibaCategory


class NetkeibaURL(ABC):
    """ netkeiba URLインターフェース
    """

    @property
    @abstractmethod
    def category(self) -> NetkeibaCategory:
        """ netkeiba Webページカテゴリー

        Returns:
            NetkeibaCategory: netkeiba Webページカテゴリー
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def url(self) -> str:
        """ netkeiba URL

        Returns:
            str: netkeiba URL
        """
        raise NotImplementedError()
