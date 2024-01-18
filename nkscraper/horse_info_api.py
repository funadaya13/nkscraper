# -*- coding: utf-8 -*-
""" 競走馬情報スクレイピングAPIモジュール
"""

from __future__ import annotations

# nkscraper
from nkscraper.utils import InvalidValueError, TableNotFoundError, TableIndexError, NKScraperLogger, NKScraperHelper
from nkscraper.common import NetkeibaCategory, NetkeibaContents, NetkeibaRequests
from nkscraper.url import HorseInfoURL

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


class HorseInfoAPI():
    """ 競走馬情報スクレイピングAPIクラス
    """

    __ERR_MESSAGE_01: str = 'NetkeibaContentsが競走馬情報ではありません. NetkeibaCategory: {}'
    __ERR_MESSAGE_02: str = '競走馬情報が見つかりませんでした. URL: {}'
    __ERR_MESSAGE_03: str = '過去のレース成績表で, 不適切な表インデックスが入力されました. index: {}, URL: {}'
    __WARN_MESSAGE_0201: str = '過去のレース成績が見つかりませんでした. 新馬の可能性があります.'
    __WARN_MESSAGE_0202: str = '枠番が取得できませんでした. 海外レースの可能性があります.'
    __WARN_MESSAGE_0203: str = '単勝オッズが取得できませんでした. 出走取消レースの場合があります.'
    __WARN_MESSAGE_0204: str = '単勝人気が取得できませんでした. 出走取消レースの場合があります.'
    __WARN_MESSAGE_0205: str = '着順が取得できませんでした. 出走取消レース・競走除外レースの可能性があります.'
    __WARN_MESSAGE_0206: str = 'タイムが取得できませんでした. 出走取消レース・競走除外レース・タイムが取得できない海外レースの可能性があります.'
    __WARN_MESSAGE_0207: str = '着差が取得できませんでした. 出走取消レース・競走除外レース・海外レースの可能性があります.'
    __WARN_MESSAGE_0208: str = 'コーナー通過順位が取得できませんでした. 出走取消レース・競走除外レース・海外レースの可能性があります.'
    __WARN_MESSAGE_0209: str = '上がり3Fタイムが取得できませんでした. 出走取消レース・競走除外レース・海外レースの可能性があります.'
    __WARN_MESSAGE_0210: str = '馬体重が取得できませんでした. 出走取消レース・海外レースの可能性があります.'
    __WARN_MESSAGE_0211: str = '馬体重増減が取得できませんでした. 出走取消レース・海外レースの可能性があります.'
    __WARN_MESSAGE_0212: str = '着順が取得できませんでした. レースが中止となった可能性があります.'

    def __init__(self, contents: NetkeibaContents) -> None:
        """ コンストラクタ

        Args:
            contents (NetkeibaContents): netkeiba Webページコンテンツ
        """
        self.__logger: Logger = NKScraperLogger.create(__name__)
        self.__helper: NKScraperHelper = NKScraperHelper()

        if contents.category != NetkeibaCategory.HORSE_INFO:
            message: str = HorseInfoAPI.__ERR_MESSAGE_01.format(contents.category.name)
            self.__logger.error(message)
            raise InvalidValueError(message)

        self.__url: str = contents.url
        self.__soup: BeautifulSoup = contents.soup
        self.__horse_id: int = self.__helper.get_id_from_url(contents.url)
        self.__profile_table: list[Tag] = self.__scrape_profile_table()
        self.__result_table: list[Tag] | None = self.__scrape_result_table()
        self.__num_race_result: int = 0 if self.__result_table is None else len(
            self.__result_table)

    @staticmethod
    def create(horse_id: int) -> HorseInfoAPI:
        """ 競走馬情報スクレイピングAPIを作成する

        Args:
            horse_id (int): netkeiba 競走馬ID

        Returns:
            HorseInfoAPI: 競走馬情報スクレイピングAPI
        """
        return HorseInfoAPI.create_by_list([horse_id])[0]

    @staticmethod
    def create_by_list(horse_id_list: list[int]) -> list[HorseInfoAPI]:
        """ 競走馬情報スクレイピングAPIを作成する

        Args:
            horse_id_list (list[int]): netkeiba 競走馬ID配列

        Returns:
            list[HorseInfoAPI]: 競走馬情報スクレイピングAPI配列
        """
        # HorseInfoURLの作成
        url_list: list[NetkeibaURL] = [HorseInfoURL(race_id) for race_id in horse_id_list]
        # 競走馬情報 NetkeibaContents の作成
        reqests: NetkeibaRequests = NetkeibaRequests()
        contents_list: list[NetkeibaContents] = reqests.get_by_list(url_list)
        # 競走馬情報スクレイピングAPIを作成して返却
        return [HorseInfoAPI(contents) for contents in contents_list]

    # Public API Functions ----------------------------------------------------
    def scrape_horse_name(self) -> str:
        """ 競走馬名をスクレイピングする

        Returns:
            str: 競走馬名
        """
        div_horse_title: Tag = self.__soup.find('div', class_='horse_title')
        h1_horse_name: Tag = div_horse_title.find('h1')
        horse_name: str = str(h1_horse_name.contents[-1])
        return self.__helper.arrange_string(horse_name)

    def scrape_horse_id(self) -> int:
        """ 競走馬IDをスクレイピングする.

        Returns:
            int: netkeiba 競走馬ID
        """
        return self.__horse_id

    def scrape_trainer_name(self) -> str:
        """ 調教師名をスクレイピングする

        Returns:
            str: 調教師名
        """
        trainer_name: str = str(self.__profile_table[1].a.contents[0])
        return self.__helper.arrange_string(trainer_name)

    def scrape_trainer_id(self) -> int:
        """ 調教師IDをスクレイピングする

        Returns:
            int: 調教師ID
        """
        trainer_url: str = str(self.__profile_table[1].a.attrs['href'])
        return self.__helper.get_id_from_url(trainer_url)

    def scrape_area(self) -> str:
        """ 所属をスクレイピングする

        Returns:
            str: 所属
        """
        td_area: Tag = self.__profile_table[1].find('td')
        area: str = str(td_area.contents[1])
        arranged_area: str = self.__helper.arrange_string(area)
        return arranged_area[1:-1]

    def scrape_father_name(self) -> str:
        """ 父馬名をスクレイピングする

        Returns:
            str: 父馬名
        """
        blood_table: Tag = self.__soup.find('table', class_='blood_table')
        tr_father: Tag = blood_table.find('tr')
        td_father: Tag = tr_father.find('td')
        father_name: str = str(td_father.a.contents[0])
        return self.__helper.arrange_string(father_name)

    def scrape_father_id(self) -> int:
        """ 父馬IDをスクレイピングする

        Returns:
            int: 父馬ID
        """
        blood_table: Tag = self.__soup.find('table', class_='blood_table')
        tr_father: Tag = blood_table.find('tr')
        td_father: Tag = tr_father.find('td')
        father_url: str = str(td_father.a.attrs['href'])
        return self.__helper.get_id_from_url(father_url)

    def exist_race_result(self) -> bool:
        """ 過去のレース成績が存在するか確認する

        Returns:
            bool: 過去のレース成績が存在すればTrue, しなければFalseを返す
        """
        return self.__result_table is not None

    def get_num_race_result(self) -> int:
        """ 過去出走のレース数をスクレイピングする

        Returns:
            int: 過去出走のレース数
        """
        return self.__num_race_result

    def scrape_race_date(self, index: int) -> date:
        """ レース開催日をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            date: レース開催日
        """
        self.__validate_table_index(index)
        td_data: Tag = self.__result_table[index].find_all('td')[0]
        date_str: str = str(td_data.a.contents[0])
        return datetime.strptime(date_str, '%Y/%m/%d').date()

    def scrape_field_name(self, index: int) -> str:
        """ 競馬場名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 競馬場名
        """
        self.__validate_table_index(index)
        td_field_name: Tag = self.__result_table[index].find_all('td')[1]
        field_name: str = str(td_field_name.a.contents[0])
        arranged_field_name: str = self.__helper.arrange_string(field_name)
        return re.sub(r'[0-9]+', '', arranged_field_name)

    def scrape_field_id(self, index: int) -> NetkeibaFieldID:
        """ NetkeibaFieldID をスクレイピングする.

        Args:
            index (int): 表インデックス

        Returns:
            NetkeibaFieldID: NetkeibaFieldID
        """
        self.__validate_table_index(index)
        field_name: str = self.scrape_field_name(index)
        return self.__helper.convert_field_name_to_id(field_name)

    def scrape_race_name(self, index: int) -> str:
        """ レース名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: レース名
        """
        self.__validate_table_index(index)
        td_race_name: Tag = self.__result_table[index].find_all('td')[4]
        race_name: str = str(td_race_name.a.contents[0])
        return self.__helper.arrange_string(race_name)

    def scrape_race_id(self, index: int) -> int:
        """ レースIDをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: netkeiba レースID
        """
        self.__validate_table_index(index)
        td_race_name: Tag = self.__result_table[index].find_all('td')[4]
        race_url: str = str(td_race_name.a.attrs['href'])
        return self.__helper.get_id_from_url(race_url)

    def scrape_wakuban(self, index: int) -> int | None:
        """ 枠番をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 枠番 (海外レースで枠番の記載がない場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_wakuban: Tag = self.__result_table[index].find_all('td')[7]
        try:
            return int(td_wakuban.contents[0])

        # 海外レースの場合
        except ValueError:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0202)
            return None
        except Exception as e:
            raise e

    def scrape_umaban(self, index: int) -> int:
        """ 馬番をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: 馬番
        """
        self.__validate_table_index(index)
        td_umaban: Tag = self.__result_table[index].find_all('td')[8]
        return int(td_umaban.contents[0])

    def scrape_tansho_odds(self, index: int) -> float | None:
        """ 単勝オッズをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 単勝オッズ (出走取消レースの場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_tansho_odds: Tag = self.__result_table[index].find_all('td')[9]
        try:
            # return float(td_tansho_odds.contents[0])
            raise Exception('TEST')

        # 出走取消レースの場合
        except ValueError:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0203)
            return None
        except Exception as e:
            raise e

    def scrape_tansho_rank(self, index: int) -> int | None:
        """ 単勝人気をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 単勝人気 (出走取消レースの場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_tansho_rank: Tag = self.__result_table[index].find_all('td')[10]
        try:
            return int(td_tansho_rank.contents[0])

        # 出走取消レースの場合
        except ValueError:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0204)
            return None
        except Exception as e:
            raise e

    def scrape_rank(self, index: int) -> int | None:
        """ 着順をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 着順 (出走取消レース・競走除外レースの場合はNoneを返す)
        """
        self.__validate_table_index(index)
        td_rank: Tag = self.__result_table[index].find_all('td')[11]
        try:
            return int(td_rank.contents[0])

        # 出走取消レース・競走除外レースの場合
        except ValueError:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0205)
            return None
        # 着順欄が空欄の場合
        except IndexError:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0212)
            return None
        except Exception as e:
            raise e

    def scrape_jockey_name(self, index: int) -> str:
        """ 騎手名をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: 騎手名
        """
        self.__validate_table_index(index)
        td_jockey_name: Tag = self.__result_table[index].find_all('td')[12]
        jockey_name: str = str(td_jockey_name.a.contents[0])
        return self.__helper.arrange_string(jockey_name)

    def scrape_jockey_id(self, index: int) -> int:
        """ 騎手IDをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: netkeiba 騎手ID
        """
        self.__validate_table_index(index)
        td_jockey_id: Tag = self.__result_table[index].find_all('td')[12]
        jockey_url: str = td_jockey_id.a.attrs['href']
        return self.__helper.get_id_from_url(jockey_url)

    def scrape_jockey_weight(self, index: int) -> float:
        """ 斤量をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: 騎手ID
        """
        self.__validate_table_index(index)
        td_jockey_weight: Tag = self.__result_table[index].find_all('td')[13]
        jockey_weight: str = td_jockey_weight.contents[0]
        arranged_jockey_weight: str = self.__helper.arrange_string(jockey_weight)
        return float(arranged_jockey_weight)

    def scrape_course_type(self, index: int) -> str:
        """ コース種別をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str: コース種別
        """
        self.__validate_table_index(index)
        td_course_type: Tag = self.__result_table[index].find_all('td')[14]
        course_type_distance: str = str(td_course_type.contents[0])
        arranged_course_type_distance: str = self.__helper.arrange_string(
            course_type_distance)
        return arranged_course_type_distance[0]

    def scrape_distance(self, index: int) -> int:
        """ レース距離をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int: レース距離
        """
        self.__validate_table_index(index)
        td_course_type: Tag = self.__result_table[index].find_all('td')[14]
        course_type_distance: str = str(td_course_type.contents[0])
        arranged_course_type_distance: str = self.__helper.arrange_string(
            course_type_distance)
        return int(arranged_course_type_distance[1:])

    def scrape_time(self, index: int) -> str | None:
        """ タイムをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str | None: タイム (出走取消レース・競走除外レース・タイムが取得できない海外レースの場合Noneを返す)
        """
        self.__validate_table_index(index)
        td_time: Tag = self.__result_table[index].find_all('td')[17]
        time: str = str(td_time.contents[0])
        arranged_time: str = self.__helper.arrange_string(time)
        # 出走取消レース・競走除外レース・タイムが取得できない海外レースの場合
        if len(arranged_time) == 1:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0206)
            return None
        return arranged_time

    def scrape_time_difference(self, index: int) -> str | None:
        """ 着差をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str | None: タイム (出走取消レース・競走除外レース・海外レースの場合Noneを返す)
        """
        self.__validate_table_index(index)
        td_time_difference: Tag = self.__result_table[index].find_all('td')[18]
        time_difference: str = str(td_time_difference.contents[0])
        arranged_time_difference: str = self.__helper.arrange_string(time_difference)
        # 出走取消レース・競走除外レース・海外レースの場合
        if len(arranged_time_difference) == 1:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0207)
            return None
        return time_difference

    def scrape_corner_ranks(self, index: int) -> str | None:
        """ コーナー通過順位をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str | None: コーナー通過順位 (出走取消レース・競走除外レース・海外レースの場合Noneを返す)
        """
        self.__validate_table_index(index)
        td_corner_ranks: Tag = self.__result_table[index].find_all('td')[20]
        corner_ranks: str = str(td_corner_ranks.contents[0])
        arranged_corner_ranks: str = self.__helper.arrange_string(corner_ranks)
        # 出走取消レース・競走除外レース・海外レースの場合
        # NOTE: 新潟1000mのような直線コースの際は、int変換でValueErrorが発生しないことを確認する
        if len(arranged_corner_ranks) == 1:
            try:
                int(arranged_corner_ranks)
            except ValueError:
                self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0208)
                return None
        return arranged_corner_ranks

    def scrape_last_3f_time(self, index: int) -> str | None:
        """ 上がり3Fタイムをスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            str | None: コーナー通過順位 (出走取消レース・競走除外レース・海外レースの場合Noneを返す)
        """
        self.__validate_table_index(index)
        td_last_3f_time: Tag = self.__result_table[index].find_all('td')[22]
        last_3f_time: str = str(td_last_3f_time.contents[0])
        arranged_last_3f_time: str = self.__helper.arrange_string(last_3f_time)
        # 出走取消レース・競走除外レース・海外レースの場合
        if len(arranged_last_3f_time) == 1:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0209)
            return None
        return arranged_last_3f_time

    def scrape_horse_weight(self, index: int) -> int | None:
        """ 馬体重をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 馬体重 (出走取消レース・海外レースの場合Noneを返す)
        """
        self.__validate_table_index(index)
        td_horse_weight: Tag = self.__result_table[index].find_all('td')[23]
        horse_weight: str = str(td_horse_weight.contents[0])
        arranged_horse_weight: str = self.__helper.arrange_string(horse_weight)
        # 出走取消レース・海外レースの場合
        if arranged_horse_weight == '計不':
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0210)
            return None
        return int(arranged_horse_weight[0:3])

    def scrape_horse_weight_fluctuation(self, index: int) -> int | None:
        """ 馬体重増減をスクレイピングする

        Args:
            index (int): 表インデックス

        Returns:
            int | None: 馬体重増減 (出走取消レース・海外レースの場合Noneを返す)
        """
        self.__validate_table_index(index)
        td_horse_weight_fluctuation: Tag = self.__result_table[index].find_all('td')[23]
        horse_weight_fluctuation: str = str(td_horse_weight_fluctuation.contents[0])
        arranged_horse_weight_fluctuation: str = self.__helper.arrange_string(
            horse_weight_fluctuation)
        # 出走取消レース・海外レースの場合
        if arranged_horse_weight_fluctuation == '計不':
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0211)
            return None
        return int(arranged_horse_weight_fluctuation[3:-1].replace('(', ''))

    # Private Functions for Scrape Table ----------------------------------
    def __scrape_profile_table(self) -> list[Tag]:
        """ 競走馬プロフィール表をスクレピングする
        """
        table_prof: Tag = self.__soup.find('table', class_='db_prof_table')
        if table_prof is None:
            message: str = HorseInfoAPI.__ERR_MESSAGE_02.format(self.__url)
            self.__logger.error(message)
            raise TableNotFoundError(message)

        return table_prof.find_all('tr')

    def __scrape_result_table(self) -> list[Tag] | None:
        """ 競走馬情報レース結果表をスクレイピングする
        """
        table_race_result: Tag = self.__soup.find('table', class_='db_h_race_results')
        if table_race_result is None:
            self.__logger.warning(HorseInfoAPI.__WARN_MESSAGE_0201)
            return None

        return table_race_result.find('tbody').findAll('tr')

    # Private Functions for Validate Table Index ----------------------------------
    def __validate_table_index(self, index: int) -> None:
        """ 表インデックスをチェックする
        """
        min_index: int = 0
        max_index: int = self.__num_race_result - 1
        message: str = HorseInfoAPI.__ERR_MESSAGE_03.format(index, self.__url)
        if index < min_index or index > max_index:
            self.__logger.error(message)
            raise TableIndexError(message)
