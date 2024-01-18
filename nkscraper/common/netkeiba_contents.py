# -*- coding: utf-8 -*-
""" netkeiba Webページコンテンツモジュール
"""

# for type declaration only
from nkscraper.common import NetkeibaCategory
from nkscraper.url import NetkeibaURL
from bs4 import BeautifulSoup


class NetkeibaContents():
    """ netkeiba Webページコンテンツクラス
    """

    def __init__(self, url: NetkeibaURL, soup: BeautifulSoup) -> None:
        """ コンストラクタ

        Args:
            url (NetkeibaURL): NetkeibaURL オブジェクト
            soup (BeautifulSoup): netkeiba Webページ BeautifulSoupオブジェクト
        """
        self.__url: str = url.url
        self.__category: NetkeibaCategory = url.category
        self.__soup: BeautifulSoup = soup

    @property
    def category(self) -> NetkeibaCategory:
        """ netkeiba Webページカテゴリー

        Returns:
            NetkeibaCategory: netkeiba Webページカテゴリー
        """
        return self.__category

    @property
    def soup(self) -> BeautifulSoup:
        """ BeautifulSoupオブジェクト

        Returns:
            BeautifulSoup: BeautifulSoupオブジェクト
        """
        return self.__soup

    @property
    def url(self) -> str:
        """ netkeiba WebページURL

        Returns:
            str: netkeiba WebページURL
        """
        return self.__url
