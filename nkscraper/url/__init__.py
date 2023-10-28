# -*- coding: utf-8 -*-
""" nkscraper URLパッケージ
"""

from .netkeiba_url import NetkeibaURL
from .horse_info_url import HorseInfoURL
from .race_result_url import RaceResultURL
from .shutuba_table_url import ShutubaTableURL
from .odds_url import OddsURL
from .training_evaluation_url import TrainingEvaluationURL


__all__ = [
    'NetkeibaURL',
    'HorseInfoURL',
    'ShutubaTableURL',
    'RaceResultURL',
    'OddsURL',
    'TrainingEvaluationURL',
]
