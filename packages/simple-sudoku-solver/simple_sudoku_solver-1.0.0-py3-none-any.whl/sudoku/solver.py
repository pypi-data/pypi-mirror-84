from sudoku.strategies import RowStrategy, ColumnStrategy, SectionStrategy
from sudoku.sudoku import Grid


class Solver(object):
    def __init__(self, grid: Grid):
        self.grid = grid

    def solve(self):
        while True:
            self.grid.updated = False
            self.solve_grid()

            if not self.grid.updated:
                break

    def solve_grid(self):
        for col_index, col in enumerate(self.grid):
            for row_index, _ in enumerate(col):
                self.solve_cell(row_index, col_index)

    def solve_cell(self, row, col):
        if isinstance(self.grid[row][col], int):
            return

        if self.grid[row][col] is None:
            initial_values = range(1, 10)
        else:
            initial_values = self.grid[row][col]

        section_strategy = SectionStrategy(self.grid, col=col, row=row)
        col_strategy = ColumnStrategy(self.grid, col=col, next_strategy=section_strategy)
        row_strategy = RowStrategy(self.grid, row=row, next_strategy=col_strategy)

        cell_values = row_strategy.solve(initial_values)

        if initial_values == cell_values:
            return

        if len(cell_values) == 1:
            self.grid.set_cell(row, col, cell_values[0])
        else:
            self.grid.set_cell(row, col, cell_values)
