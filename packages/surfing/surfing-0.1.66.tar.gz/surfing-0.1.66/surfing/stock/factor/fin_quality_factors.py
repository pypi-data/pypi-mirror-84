
import pandas as pd

from .factor_types import FinQualityFactor
from .basic_factors import GrossProfitFactor, IncomeTTMFactor, NetProfitTTMFactor, AdjNetAssetAvgFactor, TotalAssetAvgFactor, FixAssetAvgFactor
from .utils import normalize


class GrossMarginFactor(FinQualityFactor):
    # 毛利率
    def __init__(self):
        super().__init__('gr_mar')

    def calc(self):
        # 过去四个季度的毛利润除以营业收入
        self._factor = GrossProfitFactor().get() / IncomeTTMFactor().get()


class ReturnOnAssetsFactor(FinQualityFactor):
    # 资产回报率
    def __init__(self):
        super().__init__('roa')

    def calc(self):
        # 过去四个季度的净利润除以总资产
        self._factor = NetProfitTTMFactor().get() / TotalAssetAvgFactor().get()


class ReturnOnEquityFactor(FinQualityFactor):
    # 股本回报率
    def __init__(self):
        super().__init__('roe')

    def calc(self):
        # 过去四个季度的净利润除以调整净资产
        self._factor = NetProfitTTMFactor().get() / AdjNetAssetAvgFactor().get()


class TurnoverRateOfFAFactor(FinQualityFactor):
    # 固定资产周转率
    def __init__(self):
        super().__init__('tr_fa')

    def calc(self):
        # 过去四个季度的营业收入除以固定资产
        self._factor = IncomeTTMFactor().get() / FixAssetAvgFactor().get()


class MixFinQualityFactor(FinQualityFactor):
    # 合成因子
    def __init__(self):
        super().__init__('mixf')

    def calc(self):
        index = GrossMarginFactor().get().index
        columns = GrossMarginFactor().get().columns
        self._factor = pd.DataFrame((normalize(GrossMarginFactor().get().T) + normalize(ReturnOnAssetsFactor().get().T) +
                                    normalize(ReturnOnEquityFactor().get().T) + normalize(TurnoverRateOfFAFactor().get().T)).T, index=index, columns=columns)
