import math


class Grid(object):
    def __init__(self, starting_grid):
        self.grid = starting_grid
        self.updated = False

    def __getitem__(self, key):
        return self.grid[key]

    def __str__(self):
        grid = ''
        for row_num, _ in enumerate(self.grid):
            row = self.get_row(row_num)
            grid += "{} {} {} | {} {} {} | {} {} {} \n".format(*row)
        return grid

    def __eq__(self, other):
        return self.grid == other.grid

    def set_cell(self, row, col, value):
        self.grid[row][col] = value
        self.updated = True

    def get_row(self, row):
        return self.grid[row]

    def get_col(self, col):
        column_data = []
        for row in self.grid:
            column_data.append(row[col])

        return column_data

    def get_row(self, row):
        return self.grid[row]

    def get_section(self, row, col):
        section_size = self.section_size()
        row_start = row // section_size * section_size
        row_end = row_start + section_size
        col_start = col // section_size * section_size
        col_end = col_start + section_size

        return [[self.grid[x][y] for y in range(col_start, col_end)] for x in range(row_start, row_end)]

    def section_size(self):
        return int(math.sqrt(self.grid_size()))

    def grid_size(self):
        return len(self.grid)
