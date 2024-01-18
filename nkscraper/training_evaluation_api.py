# -*- coding: utf-8 -*-
""" 調教評価スクレイピングAPIモジュール
"""

from __future__ import annotations

# nkscraper
from nkscraper.utils import NKScraperException, NKScraperLogger, NKScraperHelper
from nkscraper.common import NetkeibaCategory, NetkeibaContents, NetkeibaRequests
from nkscraper.url import TrainingEvaluationURL

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


class TrainingEvaluationAPI():
    """ 調教評価スクレイピングAPIクラス
    """

    __ERR_MESSAGE_0401: str = 'NetkeibaContentsが調教評価ではありません.'
    __ERR_MESSAGE_0402: str = '調教評価表を取得できませんでした.'
    __WARN_MESSAGE_0401: str = '枠番を取得できませんでした. 出馬表が確定していない可能性があります.'
    __WARN_MESSAGE_0402: str = '馬番を取得できませんでした. 出馬表が確定していない可能性があります.'
    __WARN_MESSAGE_0403: str = '調教評価を取得できませんでした. 調教評価に記載がない可能性があります.'

    def __init__(self, contents: NetkeibaContents) -> None:
        """ コンストラクタ

        Args:
            contents (NetkeibaContents): netkeiba Webページコンテンツ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__helper: NKScraperHelper = NKScraperHelper()

        if contents.category != NetkeibaCategory.TRAINING_EVALUATION:
            self.__logger.error(TrainingEvaluationAPI.__ERR_MESSAGE_0401)
            sys.exit()

        self.__soup: BeautifulSoup = contents.soup
        self.__race_id: int = self.__helper.get_id_from_url(contents.url)
        self.__table: list[Tag] = self.__scrape_training_evaluation_table()
        self.__num_horse: int = len(self.__table)

    @staticmethod
    def create(race_id: int) -> TrainingEvaluationAPI:
        """ 調教評価スクレイピングAPIを作成する

        Args:
            race_id (int): netkeiba レースID

        Returns:
            TrainingEvaluationAPI: 調教評価スクレイピングAPI
        """
        return TrainingEvaluationAPI.create_by_list([race_id])[0]

    @staticmethod
    def create_by_list(race_id_list: list[int]) -> list[TrainingEvaluationAPI]:
        """ 調教評価スクレイピングAPIを作成する

        Args:
            race_id_list (list[int]): netkeiba レースID配列

        Returns:
            list[TrainingEvaluationAPI]: 調教評価スクレイピングAPI配列
        """
        # TrainingEvaluationURLの作成
        url_list: list[NetkeibaURL] = [
            TrainingEvaluationURL(race_id) for race_id in race_id_list]
        # 出馬表 NetkeibaContents の作成
        reqests: NetkeibaRequests = NetkeibaRequests()
        contents_list: list[NetkeibaContents] = reqests.get_by_list(url_list)
        # 調教評価スクレイピングAPIを作成して返却
        return [TrainingEvaluationAPI(contents) for contents in contents_list]

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

    def scrape_race_distance(self) -> int:
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
        """ レース開催競馬場名をスクレイピングする

        Returns:
            str: レース開催競馬場名
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

    def scrape_wakuban(self, index: int) -> int | None:
        """ 枠番をスクレイピングする

        Args:
            index (int): 表インデックス (0 <= table_index < レース出走頭数)

        Returns:
            int | None: 枠番 (枠番が確定していない場合はNoneを返す)
        """
        td_waku: Tag = self.__table[index].find(
            'td', class_=re.compile('Waku'))
        span_waku: Tag = td_waku.contents[0]
        try:
            return int(span_waku.contents[0])

        # 枠番が確定されていない場合
        except IndexError:
            self.__logger.warning(TrainingEvaluationAPI.__WARN_MESSAGE_0401)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_umaban(self, index: int) -> int | None:
        """ 馬番をスクレイピングする

        Args:
            index (int): 表インデックス (0 <= table_index < レース出走頭数)

        Returns:
            int | None: 馬番 (馬番が確定していない場合はNoneを返す)
        """
        td_umaban: Tag = self.__table[index].find(
            'td', class_='Umaban')
        try:
            return int(td_umaban.contents[0])

        # 馬番が確定されていない場合
        except IndexError:
            self.__logger.warning(TrainingEvaluationAPI.__WARN_MESSAGE_0402)
            return None
        except Exception as e:
            raise NKScraperException(e)

    def scrape_horse_name(self, index: int) -> str:
        """ 馬名をスクレイピングする

        Args:
            index (int): 表インデックス (0 <= table_index < レース出走頭数)

        Returns:
            str: 馬名
        """
        div_horse_name: Tag = self.__table[index].find(
            'div', class_='Horse_Name')
        horse_name: str = div_horse_name.a.contents[0]
        return self.__helper.arrange_string(horse_name)

    def scrape_horse_id(self, index: int) -> int:
        """ 馬IDをスクレイピングする

        Args:
            index (int): 表インデックス (0 <= table_index < レース出走頭数)

        Returns:
            int: netkeiba 馬ID
        """
        div_horse_name: Tag = self.__table[index].find(
            'div', class_='Horse_Name')
        horse_url: str = div_horse_name.a.attrs['href']
        return self.__helper.get_id_from_url(horse_url)

    def scrape_training_evaluation(self, index: int) -> str | None:
        """ 調教評価をスクレイピングする

        Args:
            index (int): 表インデックス (0 <= table_index < レース出走頭数)

        Returns:
            str | None: 調教評価 (記載がない場合はNoneを返す)
        """
        td_training_evaluation: Tag = self.__table[index].findAll('td')[5]
        try:
            training_evaluation: str = td_training_evaluation.contents[0]
            return self.__helper.arrange_string(training_evaluation)

        except IndexError:
            self.__logger.warning(TrainingEvaluationAPI.__WARN_MESSAGE_0403)
            return None
        except Exception as e:
            raise NKScraperException(e)

    # Private Functions for Scrape Training Evaluation Table -----------------
    def __scrape_training_evaluation_table(self) -> list[Tag]:
        """ 調教評価表をスクレイピングする
        """
        try:
            table: Tag = self.__soup.find('table', class_='OikiriTable')
            return table.findAll('tr', class_='HorseList')

        except AttributeError:
            self.__logger.error(TrainingEvaluationAPI.__ERR_MESSAGE_0402)
            sys.exit()
        except Exception as e:
            raise NKScraperException(e)
