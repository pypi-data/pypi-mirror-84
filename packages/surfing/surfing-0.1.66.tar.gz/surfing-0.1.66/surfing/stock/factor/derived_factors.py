
from typing import Optional

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
        self._factor_ret: Optional[pd.DataFrame] = None

    def get_ret(self) -> Optional[pd.DataFrame]:
        if self._factor_ret is None:
            self._load_ret()
        return self._factor_ret

    def save(self) -> bool:
        if self._factor_ret is not None:
            self._factor_ret.to_parquet(self._s3_uri_factor_ret, compression='gzip')
        return True
        # return super().save()

    def register(self):
        DerivedFactor._registry[self.name] = self

    def calc_ret(self, n=5) -> pd.DataFrame:
        '''
        Name: cal_ret
        Input: A DataFrame of factor; number of groups.
        Output: The factor return series of F1-Fn portfolio.
        '''
        ret_list = []
        dt_list = []
        isNaN = True
        factor = self.get()
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

        self._factor_ret = pd.DataFrame(ret_list, index=dt_list)
        self._factor_ret.columns = [self.name]

    def _load_ret(self) -> Optional[pd.DataFrame]:
        try:
            self._factor_ret: pd.DataFrame = pd.read_parquet(self._s3_uri_factor_ret)
        except Exception as e:
            print(f'retrieve ret from s3 failed, (err_msg){e}; try to re-calc')
            self.calc_ret()
        return self._factor_ret
