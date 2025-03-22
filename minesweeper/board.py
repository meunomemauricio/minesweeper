import itertools
import random
import time

from minesweeper.cells import Cell, CellMatrix


class GameOverError(Exception):
    """Tried to execute an action after the game is over."""


class Board:
    # Maximum allowed mines as a fraction of the total # of cells
    MAX_MINES = 0.5

    def __init__(self, rows: int, cols: int, mines: int) -> None:
        max_mines = int((rows * cols) * self.MAX_MINES)
        if mines > max_mines:
            raise ValueError(f"Too many mines (max. {max_mines})")

        self.rows = rows
        self.cols = cols
        self.mines = mines

        self._cells = CellMatrix(rows=rows, cols=cols)

        self.initialized = False
        self.game_over = False

        self.start_time: float | None = None
        self.stop_time: float | None = None

    def __getitem__(self, coords: tuple[int, int]) -> Cell:
        """Access the rows of pieces

        This allows for readonly access to the cells using the format

            board[r][c]
        """
        return self._cells[*coords]

    @property
    def elapsed(self) -> float:
        """Elapsed time since game started until game over."""
        if not self.start_time:
            return 0.0

        stop_time = self.stop_time if self.stop_time else time.time()
        return stop_time - self.start_time

    @property
    def mines_left(self) -> float:
        """Score based on the elapsed time."""
        return self.mines - self._cells.flag_count

    @property
    def has_won(self) -> bool:
        """Whether the board reached a winning state."""
        return self._cells.correct_count == self.mines

    def _initialize(self, row: int, col: int) -> None:
        """Generate a new valid game board.

        `row` and `col` are the coordinates of the first step.
        """
        # Generate possible mine coordinates, making sure the first step is
        # removed.
        population = list(itertools.product(range(self.rows), range(self.cols)))
        population.remove((row, col))

        # Assign mines at random
        mine_coords = random.sample(population=population, k=self.mines)
        for r_m, c_m in mine_coords:
            self._cells[r_m, c_m].is_mine = True

            # Increment adjacent regular cells
            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                try:
                    cell = self._cells[r_m + i, c_m + j]
                except IndexError:
                    pass
                else:
                    if cell.count < Cell.MAX_COUNT:
                        self._cells[r_m + i, c_m + j].count += 1

        self.initialized = True
        self.start_time = time.time()

    def _reveal_adjacent(self, cell: Cell) -> None:
        """Recursively reveal adjacent empty cells."""
        stack: list[Cell] = [cell]
        revealed: set[Cell] = set()

        while stack:
            cell = stack.pop()
            if cell in revealed:
                continue

            cell.is_hidden = False
            revealed.add(cell)

            if not cell.is_empty:
                continue

            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                r_adj, c_adj = cell.row + i, cell.col + j
                try:
                    adj = self._cells[r_adj, c_adj]
                except IndexError:
                    continue
                else:
                    stack.append(adj)

    def reset(self) -> None:
        """Reset the Board."""
        self.start_time = None
        self.stop_time = None
        self.initialized = False
        self.game_over = False
        self._cells = CellMatrix(rows=self.rows, cols=self.cols)

    def step(self, row: int, col: int) -> None:
        """Step into one of the cells.

        The board is initialized on the first step as a way to ensure it's not
        on a mine straight away.
        """
        if not (self.initialized):
            self._initialize(row=row, col=col)

        if self.game_over:
            raise GameOverError("Can't step after game over.")

        cell = self._cells[row, col]
        if cell.is_flag:
            return

        cell.is_hidden = False

        if cell.is_empty:
            self._reveal_adjacent(cell=cell)

        if cell.is_mine:
            self.stop_time = time.time()
            self.game_over = True

    def flag(self, row: int, col: int) -> None:
        """Mark a cell as a flag or undo it."""
        if not (self.initialized):
            self._initialize(row=row, col=col)

        if self.game_over:
            raise GameOverError("Can't toggle flags after game over.")

        cell = self._cells[row, col]
        cell.is_flag = not cell.is_flag
        cell.is_hidden = not cell.is_hidden

        if self.has_won:
            self.stop_time = time.time()
            self.game_over = True
