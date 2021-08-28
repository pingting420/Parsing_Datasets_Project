import pandas as pd
import json
import sys


class ResultBaser:

    def __init__(self, result_path):
        self.result_base = pd.read_csv(result_path, low_memory=False)
        return

    def analyse(self, val):
        sheet = self.result_base
        if val in sheet['software.name'].values.tolist():
            category = sheet[sheet['software.name'] == val]['Sub.cat1'].values[0]
            self._analyse_cat(category)
            return
        if val in sheet['Sub.cat1'].values.tolist():
            self._analyse_cat(val)
            return
        else:
            raise ValueError('wrong input')

    def _analyse_cat(self, cat):
        cat_competitions = {}
        competitors = self.result_base.loc[self.result_base['Sub.cat1'] == cat]['software.name'].unique()
        for software in competitors:
            cat_competitions[software] = self._analyse_software(software)
        with open(analyse_result_path, 'w') as f:
            json.dump(cat_competitions, f, indent=4, separators=(',', ': '))
        return

    def _analyse_software(self, software):
        sheet = self.result_base
        raw_total_review = sheet[sheet['software.name'] == software]['total.reviews'].values[0]
        total_review = int(raw_total_review) if pd.notna(raw_total_review) else raw_total_review
        res = {'overall.rating': sheet[sheet['software.name'] == software]['overall.rating'].values[0],
               'recomm.rating': sheet[sheet['software.name'] == software]['recomm.rating'].values[0],
               'easeofuse.rating': sheet[sheet['software.name'] == software]['easeofuse.rating'].values[0],
               'cust.serv.rating': sheet[sheet['software.name'] == software]['cust.serv.rating'].values[0],
               'feature.rating': sheet[sheet['software.name'] == software]['feature.rating'].values[0],
               'x2.rating': sheet[sheet['software.name'] == software]['x2.rating'].values[0],
               'total.reviews': total_review}
        return res



result_base_path = r'/usr/datasets/merging_datasets/data/base_data/result_base.csv'
analyse_result_path = r'/usr/datasets/merging_datasets/data/base_data/competitor_table.txt'


def main():
    sieve = ResultBaser(result_base_path)
    analyst_target = sys.argv[1]
    try:
        sieve.analyse(analyst_target)
    except ValueError as e:
        print(e)
    else:
        print("complete")


if __name__ == '__main__':
    main()
