import json
import math
import os
import traceback
from argparse import ArgumentParser

import mysql.connector
import numpy as np
import pandas as pd
import pygsheets
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()


config = {
    'host': os.environ['DB_HOST'],
    'port': int(os.environ['DB_PORT']),
    'database': os.environ['DB_DATABASE'],
    'user': os.environ['DB_USERNAME'],
    'password': os.environ['DB_PASSWORD']
}


def process_command():
    parser = ArgumentParser()
    parser.add_argument(
        "query_path", help="Path of query file, one query per file.")
    parser.add_argument(
        "gsheets_key", help="Key of the google sheet, find in the url path.")
    parser.add_argument(
        "--sheet-prefix", help="The prefix of each worksheet. Followed by auto increment number.", default="query")
    return parser.parse_args()


class SheetDestination:
    def __init__(self, key):
        self.key = key
        self.gs = pygsheets.authorize(
            service_account_file=".service_account.json")
        self.sh = self.gs.open_by_key(key)

    def create_worksheet(self, sheet_name, **kwarg):
        self.ws = self.sh.add_worksheet(sheet_name, **kwarg)

    def dump_to_sheet(self, df, CHUNKSIZE, **kwarg):
        COLUMNS = len(df.columns)
        GSHEET_BATCH = CHUNKSIZE // COLUMNS
        for k in range(COLUMNS):
            start = f'A{GSHEET_BATCH * k + 1}'
            print(start)
            d_temp = df.iloc[(GSHEET_BATCH * k):(GSHEET_BATCH * (k + 1) - 1)].copy()
            self.ws.set_dataframe(d_temp, start=start, **kwarg)


class MysqlSource:
    def __init__(self, query):
        self.query = query
        self.cnx = mysql.connector.connect(**config)

    def get_data_batch(self, CHUNKSIZE):
        return pd.read_sql(self.query, self.cnx, chunksize=CHUNKSIZE)


class BigQuerylSource:
    def __init__(self, query):
        self.query = query
        self.client = bigquery.Client()

    def get_data_batch(self, CHUNKSIZE):
        df = self.client.query(query).to_dataframe()
        count = len(df.index)
        section = math.ceil(count / CHUNKSIZE)
        for chunk in np.array_split(df, section):
            yield chunk


class SourceFactory():
    def create(self, source, query):
        if source == 'mysql':
            return MysqlSource(query)
        elif source == 'bigquery':
            return BigQuerylSource(query)
        else:
            raise('source is not correct')


if __name__ == "__main__":
    job_config = json.load(open('./config.json'))
    jobs = job_config['jobs']
    for job in jobs:
        try:
            SOURCE = job['source']
            query_path = job["query_path"]
            key = job["gsheets_key"]
            prefix = job["sheet_prefix"]

            # Google sheet has a grid limits.
            # Max rows: 25000, max columns: 2
            # one row is reserved for the field names
            CHUNKSIZE = 50000
            with open(query_path) as f:
                query = f.read()
            destination = SheetDestination(key)

            source = SourceFactory().create(SOURCE, query)
            for i, df in enumerate(source.get_data_batch(CHUNKSIZE)):
                sheet_name = f'{prefix}_{i}'
                destination.create_worksheet(sheet_name, cols=1)
                destination.dump_to_sheet(
                    df, CHUNKSIZE, copy_index=False, nan='', copy_head=False, extend=True)
        except Exception as e:
            print(traceback.format_exc())
