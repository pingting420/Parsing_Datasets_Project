
import pandas as pd
import numpy as np
import json
import sys


class CompetitorAnalyst:

    def __init__(self, result_path, review_path):
        self.result_base = pd.read_csv(result_path, low_memory=False)
        self.review_base = pd.read_csv(review_path, low_memory=False)
        return

    def analyse_competitor(self, val, kind='business'):
        if kind not in ['business', 'job_title']:
            raise ValueError('unsupported:' + kind)
        if val in self.result_base['software.name'].values.tolist():
            category = self.result_base[self.result_base['software.name'] == val]['Sub.cat1'].values[0]
            self._analyse_cat(category, kind)
            return
        elif val in self.result_base['Sub.cat1'].values.tolist():
            self._analyse_cat(val, kind)
            return
        else:
            raise ValueError('wrong input:' + val)

    def _analyse_cat(self, category, kind='business'):
        cat_competitions = {}
        competitors = self.result_base.loc[self.result_base['Sub.cat1'] == category]['software.name'].unique()
        for software in competitors:
            cat_competitions[software] = self._analyse_software_in_review(software, kind)
        with open(analyse_result_path, 'w') as f:
            json.dump(cat_competitions, f, indent=4, separators=(',', ': '))
        return

    def _analyse_software_in_review(self, software, kind='business'):
        software_review = self.review_base.loc[self.review_base['software.name'] == software].copy()

        if kind == 'business':
            y = []
            for x in software_review['business']:
                if x.find(',') != -1:
                    y.append(x.split(',')[0])
                else:
                    y.append('NaN')
            software_review['business'] = y

        kind_of_software_review = software_review[['software.name', kind]].fillna('NaN').groupby(kind).count()
        counters = kind_of_software_review['software.name'].sum()
        array_kind_of_software = np.array(kind_of_software_review['software.name'])
        a = pd.Series(np.around(np.true_divide(array_kind_of_software, counters), 2),
                         index=kind_of_software_review.index).to_dict()
        raw_total_review = self.result_base[self.result_base['software.name']==software]['total.reviews'].values[0]
        total_review = int(raw_total_review) if pd.notna(raw_total_review) else raw_total_review
        a['total.reviews'] = total_review
        return a

result_base_path = r'/usr/datasets/merging_datasets/data/base_data/result_base.csv'
review_base_path = r'/usr/datasets/merging_datasets/data/base_data/review_base.csv'
analyse_cat = 'job_title'
analyse_result_path = r'/usr/datasets/merging_datasets/data/base_data/job_title.txt'


def main():
    analyst_ins = CompetitorAnalyst(result_base_path, review_base_path)

    analyst_target = sys.argv[1]
    try:
        analyst_ins.analyse_competitor(analyst_target, analyse_cat)
    except ValueError as e:
        print(e)
    else:
        print("complete")


if __name__ == '__main__':
    main()
