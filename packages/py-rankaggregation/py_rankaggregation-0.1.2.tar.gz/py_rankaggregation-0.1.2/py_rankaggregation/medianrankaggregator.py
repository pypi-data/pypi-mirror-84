# coding=utf-8
import logging

import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)

from py_rankaggregation.rankaggregator import RankAggregator

class MedianRankAggregator(RankAggregator):
    """Median rank aggregator.
    """
    def __init__(self):
        super().__init__()

    def aggregate(self, listoflists):
        super().aggregate(listoflists)
        if self._aggregated_list is not None:
            return self._aggregated_list
        
        for _item, _ranks in self._item_ranks.items():
            _padded_lst = _ranks + [self._max_list_len+1,] * (self._max_list_len-len(_ranks))
            self._item_ranks[_item] = np.nanmedian(_padded_lst)
        self._aggregated_list = sorted(list(self._item_ranks.items()), key=lambda x: x[1])
        return self._aggregated_list

