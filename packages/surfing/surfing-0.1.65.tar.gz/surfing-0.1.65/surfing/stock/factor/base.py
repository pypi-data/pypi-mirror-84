
from typing import Optional
# from functools import lru_cache
import pandas as pd

from ...util.singleton import Singleton
from ...constant import StockFactorType
from .universe import Universe

_BUCKET_NAME = 'tl-factors'


class Factor(metaclass=Singleton):

    def __init__(self, f_name: str, f_type: StockFactorType):
        self._f_name: str = f_name
        self._f_type: StockFactorType = f_type
        self._s3_uri: str = f's3://{_BUCKET_NAME}/factor/{f_name}.parquet'
        self._s3_uri_factor_ret: str = f's3://{_BUCKET_NAME}/factor_ret/{f_name}.parquet'
        self._factor: Optional[pd.DataFrame] = None

    # @lru_cache
    def get(self, universe=None) -> Optional[pd.DataFrame]:
        if self._factor is None:
            self._load_data()
        if universe is not None:
            if not isinstance(universe, Universe):
                assert False, f'universe should be an instance of Universe, not {type(universe)}'
            stock_list = universe.get()
            return self._factor.loc[:, stock_list]
        return self._factor

    def get_normalized(self, universe=None):
        data = self.get()
        if universe is not None:
            if not isinstance(universe, Universe):
                assert False, f'universe should be an instance of Universe, not {type(universe)}'
            stock_list = universe.get()
            data = data.loc[:, stock_list]
        return ((data.T - data.mean(axis=1))/data.std(axis=1)).T

    @property
    def name(self):
        return self._f_name

    @property
    def f_type(self):
        return self._f_type

    def save(self) -> bool:
        if self._factor is None:
            return False
        self._factor.to_parquet(self._s3_uri, compression='gzip')
        # TODO: 存储factor_return
        return True

    def calc(self):
        assert False, f'should impl specialized calc algo for the {self._f_name} factor'

    def _load_data(self) -> Optional[pd.DataFrame]:
        try:
            self._factor: pd.DataFrame = pd.read_parquet(self._s3_uri)
        except Exception as e:
            print(f'retrieve data from s3 failed, (err_msg){e}; try to re-calc')
            self.calc()
        return self._factor
