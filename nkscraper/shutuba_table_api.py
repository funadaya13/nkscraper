# -*- coding: utf-8 -*-
""" 出馬表スクレイピングAPIモジュール
"""

from __future__ import annotations

# nkscraper
from nkscraper.utils import InvalidValueError, TableNotFoundError, TableIndexError, NKScraperLogger, NKScraperHelper
from nkscraper.common import NetkeibaCategory, NetkeibaContents, NetkeibaRequests
from nkscraper.url import ShutubaTableURL

# build-in
from datetime import datetime
import re

# for type declaration only
from nkscraper.common import NetkeibaFieldID
from nkscraper.url import NetkeibaURL
from logging import Logger
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import date


class ShutubaTableAPI():
    """ 出馬表スクレイピングAPIクラス
    """

    __ERR_MESSAGE_01: str = 'NetkeibaContentsが出馬表ではありません. category: {}'
    __ERR_MESSAGE_02: str = '出馬表を取得できませんでした. URL: {}'
    __ERR_MESSAGE_03: str = '出馬表で, 不適切な表インデックスが入力されました. index: {}, URL: {}'
    __WARN_MESSAGE_01: str = '枠番を取得できませんでした. 出馬表が確定していない可能性があります. index: {}, URL: {}'
    __WARN_MESSAGE_02: str = '馬番を取得できませんでした. 出馬表が確定していない可能性があります. index: {}, URL: {}'
    __WARN_MESSAGE_03: str = '騎手を取得できませんでした. 出馬表が確定していない可能性があります. index: {}, URL: {}'
    __WARN_MESSAGE_04: str = '騎手IDを取得できませんでした. 出馬表が確定していない可能性があります. index: {}, URL: {}'
    __WARN_MESSAGE_05: str = '馬体重を取得できませんでした. 馬体重が確定していない可能性があります. index: {}, URL: {}'
    __WARN_MESSAGE_06: str = '馬体重を取得できませんでした. 出走取消馬の可能性があります. index: {}, URL: {}'
    __WARN_MESSAGE_07: str = '馬体重増減を取得できませんでした. 馬体重が確定していない, または, 出走取消馬の可能性があります. index: {}, URL: {}'

    def __init__(self, contents: NetkeibaContents) -> None:
        """ コンストラクタ

        Args:
            contents (NetkeibaContents): netkeiba Webページコンテンツ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__helper: NKScraperHelper = NKScraperHelper()

        if contents.category != NetkeibaCategory.SHUTUBA_TABLE:
            message: str = ShutubaTableAPI.__ERR_MESSAGE_01.format(contents.category)
            self.__logger.error(message)
            raise InvalidValueError(message)

        self.__url: str = contents.url
        self.__soup: BeautifulSoup = contents.soup
        self.__race_id: int = self.__helper.get_id_from_url(contents.url)
        self.__table: list[Tag] = self.__scrape_shutuba_table()
        self.__num_horse: int = len(self.__table)

    @staticmethod
    def create(race_id: int) -> ShutubaTableAPI:
        """ 出馬表スクレイピングAPIを作成する

        Args:
            race_id (int): netkeiba レースID

        Returns:
            ShutubaTableAPI: 出馬表スクレイピングAPI
        """
        return ShutubaTableAPI.create_by_list([race_id])[0]

    @staticmethod
    def create_by_list(race_id_list: list[int]) -> list[ShutubaTableAPI]:
        """ 出馬表スクレイピングAPIを作成する

        Args:
            race_id_list (list[int]): netkeiba レースID配列

        Returns:
            list[ShutubaTableAPI]: 出馬表スクレイピングAPI配列
        """
        # ShutubaTableURLの作成
        url_list: list[NetkeibaURL] = [
            ShutubaTableURL(race_id) for race_id in race_id_list]
        # 出馬表 NetkeibaContents の作成
        reqests: NetkeibaRequests = NetkeibaRequests()
        contents_list: list[NetkeibaContents] = reqests.get_by_list(url_list)
        # 出馬表スクレイピングAPIを作成して返却
        return [ShutubaTableAPI(contents) for contents in contents_list]

    # Public API Functions ----------------------------------------------------
    def scrape_race_name(self) -> str:
        """ レース名をスクレイピングする

        Returns:
            str: レース名
        """
        div_race_name: Tag = self.__soup.find('div', class_='RaceName')
        race_name: str = str(div_race_name.contents[0])
        return self.__helper.arrange_string(race_name)

    def scrape_race_id(self) -> int:
        """ レースIDをスクレイピングする.

        Returns:
            int: netkeiba レースID
        """
        return self.__race_id

    def scrape_race_date(self) -> date:
        """ レース開催日をスクレイピングする

        Returns:
            date: レース開催日
        """
        title: str = str(self.__soup.find('title').contents[0])
        date_str: str = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', title)[0]
        return datetime.strptime(date_str, '%Y年%m月%d日').date()

    def scrape_course_type(self) -> str:
        """ コース種別をスクレイピングする

        Returns:
            str: コース種別 (芝 or ダ)
        """
        div_race_data01: Tag = self.__soup.find('div', class_='RaceData01')
        course_type_distance_span: Tag = div_race_data01.find('span')
        course_type_distance: str = self.__helper.arrange_string(
            str(course_type_distance_span.contents[0]))
        return course_type_distance[0]

    def scrape_distance(self) -> int:
        """ レース距離をスクレイピングする

        Returns:
            int: レース距離
        """
        div_race_data01: Tag = self.__soup.find('div', class_='RaceData01')
        course_type_distance_span: Tag = div_race_data01.find('span')
        course_type_distance: str = self.__helper.arrange_string(
            str(course_type_distance_span.contents[0]))
        return int(course_type_distance[1:-1])

    def scrape_field_name(self) -> str:
        """ 競馬場名をスクレイピングする

        Returns:
            str: 競馬場名
        """
        div_race_data02: Tag = self.__soup.find('div', class_='RaceData02')
        field_name_span: Tag = div_race_data02.findAll('span')[1]
        field_name: str = field_name_span.contents[0]
        return self.__helper.arrange_string(field_name)

    def scrape_field_id(self) -> NetkeibaFieldID:
        """ NetkeibaFieldID をスクレイピングする.

        Returns:
            NetkeibaFieldID: NetkeibaFieldID
        """
        field_name: str = self.scrape_field_name()
        return self.__helper.convert_field_name_to_id(field_name)

    def get_num_horse(self) -> int:
        """ レース出走頭数を取得する
        """
        return self.__num_horse

    def scrape_wakuban(self, index: int) -> int | None:
        """ 枠番をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 枠番 (枠番が確定していない場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_waku: Tag = self.__table[index].find(
            'td', class_=re.compile('Waku'))
        span_waku: Tag = td_waku.contents[0]
        try:
            return int(span_waku.contents[0])

        # 枠番が確定されていない場合
        except IndexError:
            self.__logger.warning(ShutubaTableAPI.__WARN_MESSAGE_01.format(index, self.__url))
            return None

    def scrape_umaban(self, index: int) -> int | None:
        """ 馬番をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 馬番 (馬番が確定していない場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_umaban: Tag = self.__table[index].find(
            'td', class_=re.compile('Umaban'))
        try:
            return int(td_umaban.contents[0])

        # 馬番が確定されていない場合
        except IndexError:
            self.__logger.warning(ShutubaTableAPI.__WARN_MESSAGE_02.format(index, self.__url))
            return None

    def scrape_horse_name(self, index: int) -> str:
        """ 馬名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 馬名
        """
        self.__validate_table_index(index)
        span_horse_name: Tag = self.__table[index].find(
            'span', class_='HorseName')
        horse_name: str = span_horse_name.a.contents[0]
        return self.__helper.arrange_string(horse_name)

    def scrape_horse_id(self, index: int) -> int:
        """ 馬IDをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: netkeiba 馬ID
        """
        self.__validate_table_index(index)
        span_horse_name: Tag = self.__table[index].find(
            'span', class_='HorseName')
        horse_url: str = span_horse_name.a.attrs['href']
        return self.__helper.get_id_from_url(horse_url)

    def scrape_sex_age(self, index: int) -> str:
        """ 馬性齢をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 馬性齢
        """
        self.__validate_table_index(index)
        try:
            td_barei: Tag = self.__table[index].find('td', class_='Barei')
            sex_age: str = str(td_barei.contents[0])

        # 出走取り消し馬の場合
        except AttributeError:
            span_age: Tag = self.__table[index].find('span', class_='Age')
            sex_age = str(span_age.contents[0])

        return self.__helper.arrange_string(sex_age)

    def scrape_jockey_weight(self, index: int) -> float:
        """ 斤量をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            float: 斤量
        """
        self.__validate_table_index(index)
        td_jockey_weight: Tag = self.__table[index].findAll('td')[5]
        return float(td_jockey_weight.contents[0])

    def scrape_jockey_name(self, index: int) -> str | None:
        """ 騎手名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str | None: 騎手名 (騎手が確定していない場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_jockey: Tag = self.__table[index].find('td', class_='Jockey')
        try:
            jockey_name: str = td_jockey.a.contents[0]
            return self.__helper.arrange_string(jockey_name)

        # 騎手が確定していない場合
        except AttributeError:
            self.__logger.warning(ShutubaTableAPI.__WARN_MESSAGE_03.format(index, self.__url))
            return None

    def scrape_jockey_id(self, index: int) -> int | None:
        """ 騎手IDをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: netkeiba 騎手ID (騎手が確定していない場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_jockey: Tag = self.__table[index].find('td', class_='Jockey')
        try:
            jockey_url: str = td_jockey.a.attrs['href']
            return self.__helper.get_id_from_url(jockey_url)

        # 騎手が確定していない場合
        except AttributeError:
            self.__logger.warning(ShutubaTableAPI.__WARN_MESSAGE_04.format(index, self.__url))
            return None

    def scrape_area(self, index: int) -> str:
        """ 所属をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 所属 (栗東・美浦など)
        """
        self.__validate_table_index(index)
        td_trainer: Tag = self.__table[index].find('td', class_='Trainer')
        span_area: Tag = td_trainer.find('span')
        area: str = span_area.contents[0]
        return self.__helper.arrange_string(area)

    def scrape_trainer_name(self, index: int) -> str:
        """ 調教師名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 調教師名
        """
        self.__validate_table_index(index)
        td_trainer: Tag = self.__table[index].find('td', class_='Trainer')
        trainer_name: str = str(td_trainer.a.contents[0])
        return self.__helper.arrange_string(trainer_name)

    def scrape_trainer_id(self, index: int) -> int:
        """ 調教師IDをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: netkeiba 調教師ID
        """
        self.__validate_table_index(index)
        td_trainer: Tag = self.__table[index].find('td', class_='Trainer')
        trainer_url: str = str(td_trainer.a.attrs['href'])
        return self.__helper.get_id_from_url(trainer_url)

    def scrape_horse_weight(self, index: int) -> int | None:
        """ 馬体重をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 馬体重 (馬体重が確定していない場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_weight: Tag = self.__table[index].find('td', class_='Weight')
        try:
            horse_weight: str = str(td_weight.contents[0])
            return int(self.__helper.arrange_string(horse_weight))

        # 馬体重が確定していない場合
        except ValueError:
            self.__logger.warning(ShutubaTableAPI.__WARN_MESSAGE_05.format(index, self.__url))
            return None
        # 出走取消馬の場合
        except AttributeError:
            self.__logger.warning(ShutubaTableAPI.__WARN_MESSAGE_06.format(index, self.__url))
            return None

    def scrape_horse_weight_fluctuation(self, index: int) -> int | None:
        """ 馬体重増減をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 馬体重増減 (馬体重が確定していない場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_weight: Tag = self.__table[index].find('td', class_='Weight')
        try:
            horse_weight_fluctuation: str = str(td_weight.small.contents[0])
            return int(horse_weight_fluctuation[1:-1])

        # 馬体重が未確定・出走取消馬の場合
        except AttributeError:
            self.__logger.warning(ShutubaTableAPI.__WARN_MESSAGE_07.format(index, self.__url))
            return None

    # Private Functions for Scrape ShutubaTable ------------------------------
    def __scrape_shutuba_table(self) -> list[Tag]:
        """ 出馬表をスクレイピングする
        """
        table: Tag = self.__soup.find('table', class_='Shutuba_Table')
        table_row_list: list[Tag] = table.findAll('tr', class_='HorseList')
        # 出馬表がない場合
        if len(table_row_list) == 0:
            message: str = ShutubaTableAPI.__ERR_MESSAGE_02.format(self.__url)
            self.__logger.error(message)
            raise TableNotFoundError(message)
        return table_row_list

    # Private Functions for Validate Table Index ----------------------------------
    def __validate_table_index(self, index: int) -> None:
        """ 表インデックスをチェックする
        """
        min_index: int = 0
        max_index: int = self.__num_horse - 1
        if index < min_index or index > max_index:
            message: str = ShutubaTableAPI.__ERR_MESSAGE_03.format(index, self.__url)
            self.__logger.error(message)
            raise TableIndexError(message)
