"""
Core module for minesweeper game.
"""
import itertools
import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Self, TypeAlias


class CellType(IntEnum):
    EMPTY = 0
    MINE = 1


class CellStatus(IntEnum):
    CLOSED = 0
    OPENED = 1
    MARKED_MINE = 2
    MARKED_UNKNOWN = 3


NeighbourMines: TypeAlias = int
Cell: TypeAlias = tuple[CellType, CellStatus, NeighbourMines]
Cells: TypeAlias = list[list[Cell]]
Difficult: TypeAlias = tuple[int, int, int]


@dataclass
class World:
    map_size: tuple[int, int]
    cells: list[list[Cell]]

    @classmethod
    def from_(cls, difficult: Difficult) -> Self:
        row, column, mines = difficult
        cells = create_cells(row, column, mines)
        return cls((row, column), cells)

    def open(self, row: int, column: int) -> None:
        if self.cells[row][column][1] == CellStatus.CLOSED:
            self.cells[row][column] = (
                self.cells[row][column][0],
                CellStatus.OPENED,
                self.cells[row][column][2],
            )
            if self.cells[row][column][2] == 0:
                for i, j in itertools.product(
                    range(row - 1, row + 2), range(column - 1, column + 2)
                ):
                    if i == row and j == column:
                        continue
                    if i < 0 or j < 0:
                        continue
                    if i >= len(self.cells) or j >= len(self.cells[0]):
                        continue
                    self.open(i, j)

    def mark_mine(self, row: int, column: int) -> None:
        match self.cells[row][column]:
            case (_type, CellStatus.CLOSED, mines):
                self.cells[row][column] = (
                    _type,
                    CellStatus.MARKED_MINE,
                    mines,
                )
            case (_type, CellStatus.MARKED_MINE, mines):
                self.cells[row][column] = (
                    _type,
                    CellStatus.CLOSED,
                    mines,
                )
            case _:
                pass

    def mark_unknown(self, row: int, column: int) -> None:
        match self.cells[row][column]:
            case (_type, CellStatus.CLOSED, mines):
                self.cells[row][column] = (
                    _type,
                    CellStatus.MARKED_UNKNOWN,
                    mines,
                )
            case (_type, CellStatus.MARKED_UNKNOWN, mines):
                self.cells[row][column] = (
                    _type,
                    CellStatus.CLOSED,
                    mines,
                )
            case _:
                pass

    def get_neighbour_cells(self, row: int, column: int) -> tuple[Cell]:
        cells: tuple[Cell] = tuple()
        for i, j in itertools.product(
            range(row - 1, row + 2), range(column - 1, column + 2)
        ):
            if i == row and j == column:
                continue
            if i < 0 or j < 0:
                continue
            if i >= len(self.cells) or j >= len(self.cells[0]):
                continue
            cells += (self.cells[i][j],)
        return cells

    @property
    def game_over(self) -> bool:
        return any(
            cell[0] == CellType.MINE and cell[1] == CellStatus.OPENED
            for row in self.cells
            for cell in row
        )

    @property
    def win(self) -> bool:
        return all(
            (cell[0] == CellType.EMPTY and cell[1] == CellStatus.OPENED)
            or (cell[0] == CellType.MINE and cell[1] == CellStatus.MARKED_MINE)
            for row in self.cells
            for cell in row
        )


def create_cells(row: int, column: int, mines: int) -> Cells:
    cells: Cells = [
        [(CellType.EMPTY, CellStatus.CLOSED, 0) for _ in range(column)]
        for __ in range(row)
    ]
    indexes = list(itertools.product(range(row), range(column)))
    for i, j in random.sample(indexes, mines):
        cells[i][j] = (CellType.MINE, CellStatus.CLOSED, 0)
    for i, j in indexes:
        cells[i][j] = (
            cells[i][j][0],
            cells[i][j][1],
            calc_neighbour_mines(cells, i, j),
        )
    return cells


def calc_neighbour_mines(cells: Cells, row: int, column: int) -> NeighbourMines:
    mines = 0
    for i, j in itertools.product(
        range(row - 1, row + 2), range(column - 1, column + 2)
    ):
        if i == row and j == column:
            continue
        if i < 0 or j < 0:
            continue
        if i >= len(cells) or j >= len(cells[0]):
            continue
        if cells[i][j][0] == CellType.MINE:
            mines += 1
    return mines
