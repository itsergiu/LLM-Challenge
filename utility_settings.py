# utility_settings
import pandas as pd
import json
import time


class SaveResultsCsvJson:
    def __init__(self, df):
        self.text_file = None
        self.text = None
        self.json = None
        self.json_file = None
        self.df = df

    def generate_json_text_files(self):
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')

        # self.json = self.df.to_json('data.json', orient='records')
        self.json = self.df.to_json(orient='records')
        self.json_file = f'sap_blog_stat_{timestamp}.json'

        self.text_file = f'sap_blog_stat_{timestamp}.csv'
        # self.text = self.df.to_csv('data.csv', index=False)
        self.text = self.df.to_csv(index=False)

