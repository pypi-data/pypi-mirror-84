import logging

import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


class RankAggregator(object):
    """Rank aggregator base class.
    """
    def __init__(self):
        super().__init__()
        self._listoflists = []
        self._aggregated_list = None

    def aggregate(self, listoflists):
        if listoflists is None:
            raise TypeError("No input provided.")
        if len(listoflists) == 0:
            raise ValueError("Empty list.")
        self._listoflists = listoflists
        
        if len(self._listoflists) == 1:
            self._aggregated_list = self._listoflists[0]

        self._item_ranks = {}
        self._max_list_len = np.max([len(clst) for clst in self._listoflists])
        for clst in self._listoflists:
            if not isinstance(clst[0], tuple) and not isinstance(clst[0], list):
                clst = [(_item, _rank+1) for _rank, _item in enumerate(clst)]
            for _item, _rank in clst:
                if _item not in self._item_ranks:
                    self._item_ranks[_item] = []
                self._item_ranks[_item].append(_rank)

