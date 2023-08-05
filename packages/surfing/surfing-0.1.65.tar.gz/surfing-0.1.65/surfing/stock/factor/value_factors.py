
import pandas as pd

from .factor_types import ValueFactor
from .basic_factors import MarketValueFactor, AdjNetAssetAvgFactor, NetProfitTTMFactor, TotalRevenueTTMFactor
from .basic_factors import EBITDATTMFactor, EntValueFactor, DividendYearlyFactor
from .utils import normalize


class NAToMVFactor(ValueFactor):
    # 净市率
    def __init__(self):
        super().__init__('na_mv')

    def calc(self):
        # 净资产 / 总市值，即市净率倒数
        self._factor = AdjNetAssetAvgFactor().get() / MarketValueFactor().get()


class NPToMVFactor(ValueFactor):
    # 盈利收益比
    def __init__(self):
        super().__init__('np_mv')

    def calc(self):
        # 净利润 / 总市值，即市盈率倒数
        self._factor = NetProfitTTMFactor().get() / MarketValueFactor().get()


class SPSToPFactor(ValueFactor):
    # 营收股价比
    def __init__(self):
        super().__init__('sps_p')

    def calc(self):
        # 每股销售额 / 股价，即市销率倒数
        self._factor = TotalRevenueTTMFactor().get() / MarketValueFactor().get()


class DividendYieldFactor(ValueFactor):
    # 股息率
    def __init__(self):
        super().__init__('dys')

    def calc(self):
        # 过去12个月总派息额 / 总市值
        self._factor = DividendYearlyFactor().get() / MarketValueFactor().get()


class EBITDAToMVFactor(ValueFactor):
    # EBITDA股价比
    def __init__(self):
        super().__init__('eb_mv')

    def calc(self):
        # EBITDA（税息折旧及摊销前利润） / 总市值
        self._factor = EBITDATTMFactor().get() / MarketValueFactor().get()


class EBITDAToEVFactor(ValueFactor):
    # EBITDA企业价值比
    def __init__(self):
        super().__init__('eb_ev')

    def calc(self):
        # EBITDA（税息折旧及摊销前利润） / 企业价值, 即企业倍数的倒数
        self._factor = EBITDATTMFactor().get() / EntValueFactor().get()


class MixValueFactor(ValueFactor):
    # 合成因子
    def __init__(self):
        super().__init__('mixv')

    def calc(self):
        index = NAToMVFactor().get().index
        columns = NAToMVFactor().get().columns
        self._factor = pd.DataFrame((normalize(NAToMVFactor().get().T) + normalize(NPToMVFactor().get().T) + normalize(SPSToPFactor().get().T) +
                                    normalize(DividendYieldFactor().get().T) + normalize(EBITDAToMVFactor().get().T) + normalize(EBITDAToEVFactor().get().T)).T, index=index, columns=columns)
