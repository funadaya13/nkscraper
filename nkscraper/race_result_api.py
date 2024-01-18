# -*- coding: utf-8 -*-
""" レース結果スクレイピングAPIモジュール
"""

from __future__ import annotations

# nkscraper
from nkscraper.utils import NKScraperException, NKScraperLogger, NKScraperHelper
from nkscraper.common import NetkeibaCategory, NetkeibaContents, NetkeibaRequests
from nkscraper.url import RaceResultURL

# build-in
from datetime import datetime
import re
import sys

# for type declaration only
from nkscraper.common import NetkeibaFieldID
from nkscraper.url import NetkeibaURL
from logging import Logger
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import date


class RaceResultAPI():
    """ レース結果スクレイピングAPIクラス
    """

    __ERR_MESSAGE_0101: str = 'NetkeibaContentsがレース結果ではありません.'
    __ERR_MESSAGE_0102: str = 'レース結果表が見つかりませんでした.'
    __WARN_MESSAGE_0101: str = '着順を取得できませんでした. 出走取消馬・または競走除外馬の可能性があります.'
    __WARN_MESSAGE_0102: str = 'タイムを取得できませんでした. 出走取消馬・競走除外馬の可能性があります.'
    __WARN_MESSAGE_0103: str = '単勝人気を取得できませんでした. 出走取消馬の可能性があります.'
    __WARN_MESSAGE_0104: str = '単勝オッズを取得できませんでした. 出走取消馬の可能性があります.'
    __WARN_MESSAGE_0105: str = '上がり3Fタイムを取得できませんでした. 出走取消馬・競走除外馬の可能性があります.'
    __WARN_MESSAGE_0106: str = 'コーナー通過順位を取得できませんでした. 出走取消馬・競走除外馬の可能性があります.'
    __WARN_MESSAGE_0107: str = '馬体重を取得できませんでした. 出走取消馬の可能性があります.'
    __WARN_MESSAGE_0108: str = '馬体重増減を取得できませんでした. 出走取消馬, または, 前回馬体重が計測不能だった可能性があります.'

    def __init__(self, contents: NetkeibaContents) -> None:
        """ コンストラクタ

        Args:
            contents (NetkeibaContents): netkeiba Webページコンテンツ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__helper: NKScraperHelper = NKScraperHelper()

        if contents.category != NetkeibaCategory.RACE_RESULT:
            self.__logger.error(RaceResultAPI.__ERR_MESSAGE_0101)
            sys.exit()

        self.__soup: BeautifulSoup = contents.soup
        self.__race_id: int = self.__helper.get_id_from_url(contents.url)
        self.__table: list[Tag] = self.__scrape_race_result_table()
        self.__num_horse: int = len(self.__table)

    @staticmethod
    def create(race_id: int) -> RaceResultAPI:
        """ レース結果スクレイピングAPIを作成する

        Args:
            race_id (int): netkeiba レースID

        Returns:
            RaceResultAPI: レース結果スクレイピングAPI
        """
        return RaceResultAPI.create_by_list([race_id])[0]

    @staticmethod
    def create_by_list(race_id_list: list[int]) -> list[RaceResultAPI]:
        """ レース結果スクレイピングAPIを作成する

        Args:
            race_id_list (list[int]): netkeiba レースID配列

        Returns:
            list[RaceResultAPI]: レース結果スクレイピングAPI配列
        """
        # RaceResultURLの作成
        url_list: list[NetkeibaURL] = [RaceResultURL(race_id) for race_id in race_id_list]
        # レース結果 NetkeibaContents の作成
        reqests: NetkeibaRequests = NetkeibaRequests()
        contents_list: list[NetkeibaContents] = reqests.get_by_list(url_list)
        # レース結果スクレイピングAPIを作成して返却
        return [RaceResultAPI(contents) for contents in contents_list]

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

        Returns:
            int: レース出走頭数
        """
        return self.__num_horse

    def scrape_rank(self, index: int) -> int | None:
        """ 着順をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 着順 (出走取消馬、競走除外の場合はNoneを返す)
        """
        div_rank: Tag = self.__table[index].find('div', class_='Rank')
        try:
            return int(div_rank.contents[0])

        # 出走取消馬・競走除外馬の場合
        except ValueError:
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0101)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_wakuban(self, index: int) -> int:
        """ 枠番をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: 枠番
        """
        td_waku: Tag = self.__table[index].find('td', class_=re.compile('Waku'))
        div_waku: Tag = td_waku.find('div')
        return int(div_waku.contents[0])

    def scrape_umaban(self, index: int) -> int:
        """ 馬番をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: 馬番
        """
        td_umaban: Tag = self.__table[index].findAll('td')[2]
        div_umaban: Tag = td_umaban.find('div')
        return int(div_umaban.contents[0])

    def scrape_horse_name(self, index: int) -> str:
        """ 馬名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 馬名
        """
        span_horse_name: Tag = self.__table[index].find('span', class_='Horse_Name')
        horse_name: str = span_horse_name.a.contents[0]
        return self.__helper.arrange_string(horse_name)

    def scrape_horse_id(self, index: int) -> int:
        """ 馬IDをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: netkeiba 馬ID
        """
        span_horse_name: Tag = self.__table[index].find('span', class_='Horse_Name')
        horse_url: str = span_horse_name.a.attrs['href']
        return self.__helper.get_id_from_url(horse_url)

    def scrape_sex_age(self, index: int) -> str:
        """ 馬性齢をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 馬性齢
        """
        div_horse_info_detail: Tag = self.__table[index].find(
            'div', class_='Horse_Info_Detail')
        span_sex_age: Tag = div_horse_info_detail.find('span')
        sex_age: str = str(span_sex_age.contents[0])
        return self.__helper.arrange_string(sex_age)

    def scrape_jockey_weight(self, index: int) -> float:
        """ 斤量をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            float: 斤量
        """
        span_jockey_weight: Tag = self.__table[index].find(
            'span', class_='JockeyWeight')
        return float(span_jockey_weight.contents[0])

    def scrape_jockey_name(self, index: int) -> str:
        """ 騎手名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 騎手名
        """
        td_jockey: Tag = self.__table[index].find('td', class_='Jockey')
        jockey_name: str = td_jockey.a.contents[0]
        return self.__helper.arrange_string(jockey_name)

    def scrape_jockey_id(self, index: int) -> int:
        """ 騎手IDをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: netkeiba 騎手ID
        """
        td_jockey: Tag = self.__table[index].find('td', class_='Jockey')
        jockey_url: str = td_jockey.a.attrs['href']
        return self.__helper.get_id_from_url(jockey_url)

    def scrape_time(self, index: int) -> str | None:
        """ タイムをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str | None: タイム ex: 3:00.0 (出走取消馬・競走除外馬の場合はNoneを返す)
        """
        span_race_time: Tag = self.__table[index].find(
            'span', class_='RaceTime')
        try:
            time: str = str(span_race_time.contents[0])
            return self.__helper.arrange_string(time)

        # 出走取消馬・競走除外馬の場合
        except IndexError:
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0102)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_tansho_rank(self, index: int) -> int | None:
        """ 単勝人気をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 単勝人気 (出走取消馬の場合はNoneを返す)
        """
        span_odds_people: Tag = self.__table[index].find(
            'span', class_='OddsPeople')
        try:
            return int(span_odds_people.contents[0])

        # 出走取消馬の場合
        except IndexError:
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0103)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_tansho_odds(self, index: int) -> float | None:
        """ 単勝オッズをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 単勝オッズ (出走取消馬の場合はNoneを返す)
        """
        td_tansho_odds: Tag = self.__table[index].findAll('td')[10]
        span_tansho_odds: Tag = td_tansho_odds.find('span')
        try:
            return float(span_tansho_odds.contents[0])

        # 出走取消馬の場合
        except IndexError:
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0104)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_last_3f_time(self, index: int) -> float | None:
        """ 上がり3Fタイムスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 上がり3Fタイム (出走取消馬・競走除外馬の場合はNoneを返す)
        """
        td_last_3f_time: Tag = self.__table[index].findAll('td')[11]
        last_3f_time: str = self.__helper.arrange_string(
            td_last_3f_time.contents[0])
        try:
            return float(last_3f_time)

        # 出走取消馬・競走除外馬の場合
        except ValueError:
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0105)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_corner_ranks(self, index: int) -> str | None:
        """ コーナー通過順位をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: コーナー通過順位 ex: 14-15-14-15 (出走取消馬・競走除外馬の場合はNoneを返す)
        """
        td_passage_rate: Tag = self.__table[index].find(
            'td', class_='PassageRate')
        corner_ranks: str = td_passage_rate.contents[0]
        arranged_corner_ranks: str = self.__helper.arrange_string(corner_ranks)
        if arranged_corner_ranks == '':
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0106)
            return None
        return arranged_corner_ranks

    def scrape_area(self, index: int) -> str:
        """ 所属をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 所属
        """
        td_trainer: Tag = self.__table[index].find('td', class_='Trainer')
        span_area: Tag = td_trainer.find('span')
        area: str = span_area.contents[0]
        return self.__helper.arrange_string(area)

    def scrape_horse_weight(self, index: int) -> int | None:
        """ 馬体重をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 馬体重 (出走取消馬の場合はNoneを返す)
        """
        td_weight: Tag = self.__table[index].find('td', class_='Weight')
        horse_weight: str = str(td_weight.contents[0])
        try:
            return int(self.__helper.arrange_string(horse_weight))

        # 出走取消馬の場合
        except ValueError:
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0107)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_horse_weight_fluctuation(self, index: int) -> int | None:
        """ 馬体重増減をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 馬体重増減 (出走取消馬、または、前回計測不能の場合はNoneを返す)
        """
        td_weight: Tag = self.__table[index].find('td', class_='Weight')
        small_weight_fluctuation: Tag = td_weight.find('small')
        try:
            weight_fluctuation: str = small_weight_fluctuation.contents[0]
            return int(weight_fluctuation[1:-1])

        # 出走取消馬、または、前回計測不能の場合
        except IndexError:
            self.__logger.warning(RaceResultAPI.__WARN_MESSAGE_0108)
            return None
        except Exception as e:
            raise NKScraperException(e)

    # Private Functions for Scrape Race Result Table -------------------------
    def __scrape_race_result_table(self) -> list[Tag]:
        """ レース結果表をスクレイピングする
        """
        table: Tag = self.__soup.find('table', id='All_Result_Table')
        # レース結果表がない場合
        if table is None:
            self.__logger.error(RaceResultAPI.__ERR_MESSAGE_0102)
            sys.exit()
        table_row_list: list[Tag] = table.findAll('tr', class_='HorseList')
        return table_row_list
