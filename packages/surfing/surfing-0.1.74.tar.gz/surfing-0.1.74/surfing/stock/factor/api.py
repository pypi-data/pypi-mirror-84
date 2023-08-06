
import datetime
from typing import Tuple, List, Optional

import pandas as pd
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset

from .derived_factors import DerivedFactor


class StockFactorApi:

    _DECOMP_RET_DATE_OFFSET = DateOffset(years=1)

    @staticmethod
    def get_stock_factor_ret(factor_names: Tuple[str], universe: str) -> Optional[pd.DataFrame]:
        rets: List[pd.Series] = []
        for one in factor_names:
            try:
                factor = DerivedFactor._registry[one]
            except KeyError as e:
                print(f'[stock_factor_api] invalid stock factor name {one} (err_msg){e} (universe){universe}')
                continue
            f_ret = factor.get_ret(universe=universe)
            if f_ret is not None:
                rets.append(f_ret)
            else:
                print(f'[stock_factor_api] retrieve return of {one} failed (universe){universe}')
        if rets:
            return pd.concat(rets, axis=1)

    @staticmethod
    def decomp_ret(fund_ret: pd.Series, factor_names: Tuple[str], universe: str) -> Optional[pd.Series]:
        ret_rg = StockFactorApi.get_stock_factor_ret(factor_names, universe)
        if ret_rg is None:
            print(f'[stock_factor_api] retrieve return of {factor_names} failed')
            return
        try:
            fund_ret = fund_ret.dropna()
            cal_start_date = (fund_ret.index.array[-1] - StockFactorApi._DECOMP_RET_DATE_OFFSET).date()
            if fund_ret.index.array[0] > cal_start_date:
                print(f'[stock_factor_api] not enough data of fund {fund_ret.name} (start_date){fund_ret.index.array[0]}')
                return
            filtered_fund_ret = fund_ret[fund_ret.index >= cal_start_date]
            if filtered_fund_ret.empty:
                print(f'[stock_factor_api] no data of fund {fund_ret.name} to decomp (start_date){fund_ret.index.array[0]} (end_date){fund_ret.index.array[-1]}')
                return
            rg = filtered_fund_ret.to_frame().join(ret_rg).ffill().dropna()
            Y = rg.iloc[:, 0]
            X = sm.add_constant(rg.iloc[:, 1:])
            model1 = sm.OLS(Y, X)
            resu1 = model1.fit()
            return pd.Series(resu1.params, index=['const']+ret_rg.columns.to_list(), name=fund_ret.name)
        except Exception as e:
            print(f'[stock_factor_api] abnormal error when decomp return (err_msg){e}')
            return
