# -*- coding: utf-8 -*-

from nkscraper import ShutubaTableAPI

race_id = 202206050811  # 2022年有馬記念
api = ShutubaTableAPI.create(race_id)

num_horse = api.get_num_horse()
for index in range(num_horse):
    print(api.scrape_horse_name(index))
