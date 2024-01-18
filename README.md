# nkscraper

A Python Package for Scraping Netkeiba.


## 使い方

```python
from nkscraper import ShutubaTableAPI

race_id = 202206050811  # 2022年有馬記念
api = ShutubaTableAPI.create(race_id)

num_horse = api.get_num_horse()
for index in range(num_horse):
    print(api.scrape_horse_name(index))

# 結果
アカイイト
イズジョーノキセキ
ボルドグフーシュ
アリストテレス
ジェラルディーナ
ヴェラアズール
エフフォーリア
ウインマイティー
イクイノックス
ジャスティンパレス
ラストドラフト
ポタジェ
タイトルホルダー
ボッケリーニ
ブレークアップ
ディープボンド
```

## API

スクレイピングできる項目については、APIドキュメントを参照.
| # | API | 内容 | ドキュメント |
| --- | --- | --- | --- |
| 1 | ShutubaTableAPI | 出馬表 | [ShutubaTableAPI Documentation](https://funadaya13.github.io/nkscraper/nkscraper.shutuba_table_api.html) |
| 2 | RaceResultAPI | レース結果 | [RaceResultAPI Documentation](https://funadaya13.github.io/nkscraper/nkscraper.race_result_api.html) |
| 3 | HorseInfoAPI | 競走馬情報, 過去成績 | [HorseInfoAPI Documentation](https://funadaya13.github.io/nkscraper/nkscraper.horse_info_api.html) |
| 4 | OddsAPI | オッズ | [OddsAPI Documentation](https://funadaya13.github.io/nkscraper/nkscraper.odds_api.html) |
| 5 | TrainingEvaluationAPI | 調教評価 | [TrainingEvaluationAPI Documentation](https://funadaya13.github.io/nkscraper/nkscraper.training_evaluation_api.html) |
| 6 | SearchedRaceAPI | レース検索結果 | [SearchedRaceAPI Documentation](https://funadaya13.github.io/nkscraper/nkscraper.searched_race_api.html) |

## インストール

<pre>
pip install git+https://github.com/funadaya13/nkscraper.git
</pre>

## 環境

| # | 言語・パッケージ | バージョン |
| --- | --- | --- |
| 1 | Python | 3.9 |
| 2 | bs4 | ^0.0.1 |
| 3 | aiohttp | ^3.8.6 |
| 4 | lxml | ^4.9.3 |


## 環境構築

前提: poetry, pyenvのインストール

<pre>
git clone https://github.com/funadaya13/nkscraper.git
cd nkscraper
pyenv install 3.9.16
pyenv local 3.9.16
poetry config virtualenvs.in-project true
poetry install
</pre>
