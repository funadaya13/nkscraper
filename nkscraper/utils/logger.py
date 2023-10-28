# -*- coding: utf-8 -*-
""" nkscraper ログモジュール
"""

# packages
from logging import getLogger, INFO, Formatter, StreamHandler, Logger
import sys


class NKScraperLogger():
    """ nkscraper ログクラス
    """

    @staticmethod
    def create(module_name: str) -> Logger:
        """ Logger 初期化関数

        Args:
            module_name (str): モジュール名

        Returns:
            Logger: 初期化したLoggerオブジェクト
        """
        # loggerを定義
        logger: Logger = getLogger(module_name)
        logger.setLevel(INFO)
        # ハンドラを定義
        # NOTE: 同一クラスからの Logger 再生成を防ぐ
        if not logger.hasHandlers():
            stream_handler = StreamHandler(sys.stdout)
            # 出力レベルを定義
            stream_handler.setLevel(INFO)
            # ハンドラの登録
            logger.addHandler(stream_handler)
            # loggerのフォーマットを定義
            formatter = Formatter(
                '%(asctime)s %(name)s [%(levelname)s]: %(message)s')
            # フォーマットを登録
            stream_handler.setFormatter(formatter)

        return logger
