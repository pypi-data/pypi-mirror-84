import itertools
from abc import ABCMeta, abstractmethod
from sudoku.sudoku import Grid


class AbstractStrategy(object):
    def __init__(self, grid, next_strategy=None, row=None, col=None):
        self.grid = grid
        self.row = row
        self.col = col
        self.next_strategy = next_strategy

    def next(self, possible_values):
        if self.next_strategy:
            return self.next_strategy.solve(possible_values)

        return possible_values

    def solve(self, possible_values):
        possible_values = self.execute(possible_values)
        return self.next(possible_values)

    def execute(self, possible_values):
        pass


class RowStrategy(AbstractStrategy):
    def execute(self, possible_values):
        row_values = self.grid.get_row(self.row)
        row_values = [c for c in row_values if isinstance(c, int)]
        return list(set(possible_values) - set(row_values))


class ColumnStrategy(AbstractStrategy):
    def execute(self, possible_values):
        col_values = self.grid.get_col(self.col)
        col_values = [c for c in col_values if isinstance(c, int)]
        return list(set(possible_values) - set(col_values))


class SectionStrategy(AbstractStrategy):
    def execute(self, possible_values):
        section_values = self.grid.get_section(self.row, self.col)
        section_values = itertools.chain(*section_values)
        section_values = [c for c in section_values if isinstance(c, int)]
        return list(set(possible_values) - set(section_values))
