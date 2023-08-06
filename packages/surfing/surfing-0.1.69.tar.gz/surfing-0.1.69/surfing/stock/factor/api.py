
from typing import Tuple, List, Optional

import pandas as pd
import statsmodels.api as sm

from .derived_factors import DerivedFactor


class StockFactorApi:

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
            rg = pd.concat([fund_ret, ret_rg], axis=1, join='outer').ffill().dropna()
            Y = rg.iloc[1:, 0]
            X = rg.iloc[1:, 1:]
            model1 = sm.OLS(Y, X)
            resu1 = model1.fit()
            return pd.Series(resu1.params, index=ret_rg.columns, name=fund_ret.name)
        except Exception as e:
            print(f'[stock_factor_api] abnormal error when decomp return (err_msg){e}')
            return
