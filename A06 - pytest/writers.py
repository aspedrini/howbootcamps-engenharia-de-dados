import datetime
import json
import os
from typing import List


class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter:

    def __init__(self, coin: str, api:str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now().strftime('/%Y/%m/%d')}.json" 

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok= True)
        with open(self.filename, 'a') as f:
            f.write(row)
        
    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + '\n')
        elif isinstance(data,List):
            for i in data:
                self.write(i)
        else:
            # a exceção nao existe, foi necessário criar uma classe para ela
            raise DataTypeNotSupportedForIngestionException(data) 