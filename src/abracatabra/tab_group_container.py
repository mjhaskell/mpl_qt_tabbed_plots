from typing import Sequence
from itertools import chain

from .tabbed_figure_widget import TabbedFigureWidget


class TabGroupContainer:
    def __init__(self, group_list: list[list[TabbedFigureWidget]],
                 row_major: bool):
        """
        A container for a list of tab groups.

        Args:
            group_list (list[list[TabbedFigureWidget]]): A list of lists, where
                each inner list contains TabbedFigureWidget objects representing
                a group of tabs.
            row_major (bool): If True, the first index is the row index and the
                second index is the column index. If False, the order is reversed.
        """
        self._tab_groups: list[list[TabbedFigureWidget]] = group_list
        self._row_major = row_major

    def __getitem__(self, index: tuple[int,int]) -> TabbedFigureWidget:
        """
        Returns the tab group at the given index.

        Args:
            index (tuple[int, int]): A tuple containing two integers, where the
                first integer is the row index and the second integer is the
                column index.
        """
        if not isinstance(index, Sequence) or len(index) != 2:
            raise ValueError(f'Index must contain two integers, got {index}')
        row, col = index
        if not self._row_major:
            col, row = index
        return self._tab_groups[row][col]

    def __iter__(self):
        return chain.from_iterable(self._tab_groups)
