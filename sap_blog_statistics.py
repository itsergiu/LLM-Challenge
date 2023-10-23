# Blog:
# Online app:
# Statistics for https://blogs.sap.com/ | comments, likes and views
# Created by: Sergiu Iatco | October, 2023
# https://www.linkedin.com/in/sergiuiatco/


import requests
from bs4 import BeautifulSoup
import pandas as pd


class SapBlogStatistics:
    ZERO = '0'
    OK_SUCCESS = 'Y'
    OK_FAILURE = 'N'

    def __init__(self, file_name=None):
        self.file_name = file_name
        self.df_results = pd.DataFrame()
        self.df_file = pd.DataFrame()

        if file_name is not None:
            self.df_file = pd.read_csv(file_name)

    def mt_iter_file(self):
        if not self.df_file.empty:
            for _, row in self.df_file.iterrows():
                url = row['url']
                soup, ok = self.mt_requests_get(url)
                result_dict = self.mt_span_elements(url, soup, ok)
                self.mt_append_results(result_dict)

    def mt_requests_get(self, url):
        soup, ok = None, self.OK_FAILURE
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                ok = self.OK_SUCCESS
        except requests.RequestException:
            ok = self.OK_FAILURE
        return soup, ok

    @staticmethod
    def mt_span_elements(url, soup, ok):
        result_dict = {'url': [url], 'OK': [ok]}

        if soup is not None:
            span_elements = soup.find_all('span', class_='ds-social-stats__stat')
            for span_element in span_elements:
                i_element = span_element.find('i')
                i_class_name = i_element['class'][1]
                number_text = span_element.get_text(strip=True)
                result_dict[i_class_name] = [number_text]

        return result_dict

    def mt_append_results(self, result_dict):
        df_request = pd.DataFrame.from_dict(result_dict)
        self.df_results = pd.concat([self.df_results, df_request], axis=0).reset_index(drop=True)

    def mt_rename_cols(self, new_column_names):
        if not self.df_results.empty:
            column_mapping = {old_col: new_col for old_col, new_col in zip(self.df_results.columns, new_column_names)}
            self.df_results.rename(columns=column_mapping, inplace=True)

    def mt_convert_cols_to_int(self, column_names):
        if not self.df_results.empty:
            for cols in column_names:
                if self.df_results.dtypes[cols] == 'object':
                    self.df_results[cols] = pd.to_numeric(self.df_results[cols].str.replace(',', ''))
                    self.df_results[cols] = pd.to_numeric(self.df_results[cols], errors='coerce', downcast='integer')

    def mt_calculate_totals(self, cols_drop=None):
        if not self.df_results.empty:
            if cols_drop is None:
                cols_drop = ['url']
            df = self.df_results.copy()
            df.drop(cols_drop, axis=1, inplace=True)
            df_ok_sum = df.groupby(['OK']).sum()
            df_ok_count = df.groupby(['OK']).size().reset_index(name='Count')
        else:
            df_ok_sum = pd.DataFrame()
            df_ok_count = pd.DataFrame()
        return {'df_ok_sum': df_ok_sum, 'df_ok_count': df_ok_count}
