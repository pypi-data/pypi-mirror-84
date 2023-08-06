
from typing import Optional, Dict

import numpy as np
import pandas as pd

from ...constant import StockFactorType
from .base import Factor
from .basic_factors import StockPostPriceFactor
from .utils import get_quarterly_tradingday_list


class DerivedFactor(Factor):

    _registry = {}

    def __init__(self, name, f_type: StockFactorType):
        super().__init__(name, f_type)
        # 这里我们将每一个universe下的因子值都存下来
        self._factor_ret: Dict[str, pd.DataFrame] = {}

    def get_ret(self, universe='default') -> Optional[pd.DataFrame]:
        try:
            return self._factor_ret[universe]
        except KeyError:
            return self._load_ret(universe)

    def save(self, universe='default') -> bool:
        try:
            self._factor_ret[universe].to_parquet(self._get_s3_factor_ret_uri(universe), compression='gzip')
            # return super().save()
            return True
        except KeyError:
            return False

    def register(self):
        DerivedFactor._registry[self.name] = self

    def calc_ret(self, universe='default', n=5) -> pd.DataFrame:
        '''
        Name: cal_ret
        Input: A DataFrame of factor; number of groups.
        Output: The factor return series of F1-Fn portfolio.
        '''
        ret_list = []
        dt_list = []
        isNaN = True
        factor = self.get(universe=universe)
        # 计算收益
        spp_factor = StockPostPriceFactor().get()
        ret = spp_factor.apply(np.log).diff()
        tradingday_list = get_quarterly_tradingday_list()
        for i in range(0, len(factor)):
            dt_list.append(factor.index[i])
            if len(factor.iloc[i].dropna()) == 0:
                ret_list.append(np.nan)
            elif isNaN:
                F1_bound = factor.iloc[i].dropna().quantile(1-1/n)
                Fn_bound = factor.iloc[i].dropna().quantile(1/n)
                F1_set = factor.iloc[i][factor.iloc[i] > F1_bound].index
                Fn_set = factor.iloc[i][factor.iloc[i] < Fn_bound].index
                ret_list.append(np.nan)
                isNaN = False
            elif factor.index[i] in tradingday_list:
                F1_ret = ret.iloc[i][F1_set].mean()
                Fn_ret = ret.iloc[i][Fn_set].mean()
                ret_list.append(F1_ret - Fn_ret)

                F1_bound = factor.iloc[i].dropna().quantile(1-1/n)
                Fn_bound = factor.iloc[i].dropna().quantile(1/n)
                F1_set = factor.iloc[i][factor.iloc[i] > F1_bound].index
                Fn_set = factor.iloc[i][factor.iloc[i] < Fn_bound].index
            else:
                F1_ret = ret.iloc[i][F1_set].mean()
                Fn_ret = ret.iloc[i][Fn_set].mean()
                ret_list.append(F1_ret - Fn_ret)

        self._factor_ret[universe] = pd.DataFrame(ret_list, index=dt_list)
        self._factor_ret[universe].columns = [self.name]

    def _load_ret(self, universe) -> Optional[pd.DataFrame]:
        try:
            self._factor_ret[universe]: pd.DataFrame = pd.read_parquet(self._get_s3_factor_ret_uri(universe))
        except Exception as e:
            print(f'retrieve ret from s3 failed, (err_msg){e}; try to re-calc')
            self.calc_ret(universe)
        return self._factor_ret[universe]
