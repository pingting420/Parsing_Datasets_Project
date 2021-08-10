
import pandas as pd
import numpy as np
import json


class CompetitorAnalyst:

    def __init__(self, result_path, review_path):
        self.result_base = pd.read_csv(result_path)
        self.review_base = pd.read_csv(review_path)
        return

    def analyse_competitor(self, val, kind='business'):
        if val in self.result_base['software.name'].values.tolist():
            category = self.result_base[self.result_base['software.name'] == val]['Sub.cat1'].values[0]
            return self._analyse_cat(category, kind)
        elif val in self.result_base['Sub.cat1'].values.tolist():
            return self._analyse_cat(val, kind)
        else:
            return BaseException('wrong input')

    def _analyse_cat(self, category, kind='business'):
        cat_competitions = {}
        competitors = self.result_base.loc[self.result_base['Sub.cat1'] == category]['software.name'].unique()
        for software in competitors:
            cat_competitions[software] = self._analyse_software_in_review(software, kind)
        return json.dumps(cat_competitions, indent=4, separators=(',', ': '))

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
        return pd.Series(np.around(np.true_divide(np.multiply(array_kind_of_software, 100), counters), 4),
                         index=kind_of_software_review.index).apply(
            lambda xx: "%.2f%%" % xx).to_dict()


def main():
    com = CompetitorAnalyst('./result_base.csv', './review_base.csv')
    print(com.analyse_competitor('FigPii', 'job_title'))


if __name__ == '__main__':
    main()
