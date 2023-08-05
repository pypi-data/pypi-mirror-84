
from typing import List

from ...util.singleton import Singleton
from ...data.api.raw import RawDataApi


class Universe(metaclass=Singleton):
    def __init__(self, name: str):
        self._name = name
        self._stock_list: List[str] = None

    def get(self) -> List[str]:
        if self._stock_list is None:
            self._load_data()
        return self._stock_list

    def _load_data(self):
        df = RawDataApi().get_em_index_component(index_list=[self._name])
        stock_list = df.set_index('datetime').stock_list.sort_index().array[-1]
        self._stock_list = stock_list.split(',')


class HS300Universe(Universe):
    # 沪深300
    def __init__(self):
        super().__init__('hs300')


class CSI800Universe(Universe):
    # 中证800
    def __init__(self):
        super().__init__('csi800')
