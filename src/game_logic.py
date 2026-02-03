"""
Author: Joseph Ghviniashvili
Date: 1/14/2026

Backend of game.

 After each player click (attempt to place an obstacle), the frog computes the
shortest path to any edge cell (avoiding obstacles) and jumps one
cell along that path. If the frog reaches an edge, the player loses.
If there is no path to an edge, the player wins.

API (high level):
- `GameLogic(rows, cols)` - create a game instance
- `reset()` - reset the grid and respawn initial obstacles
- `add_obstacle(r, c)` - add an obstacle at (r,c) if possible
- `step_after_click(r, c)` - perform the click, compute path, make frog jump one cell
- `shortest_path_to_edge()` - returns list of (r,c) from frog to edge, or [] if none
- `get_state()` - returns dict with `rows`, `cols`, `frog`, `obstacles`, `status`
"""

import random
from collections import deque
from typing import List, Tuple, Set, Dict

Cell = Tuple[int, int]


class GameLogic:
    def __init__(self, rows: int = 11, cols: int = 11, min_obstacles: int = 10, max_obstacles: int = 15):
        self.rows = rows
        self.cols = cols
        self.min_obstacles = min_obstacles
        self.max_obstacles = max_obstacles
        self.frog: Cell = (rows // 2, cols // 2)
        self.obstacles: Set[Cell] = set()
        self.status: str = "in_progress"  # in_progress, win, lose
        self.spawn_initial_obstacles()

    def reset(self) -> None:
        """Reset the game to initial state and respawn obstacles."""
        self.frog = (self.rows // 2, self.cols // 2)
        self.obstacles.clear()
        self.status = "in_progress"
        self.spawn_initial_obstacles()

    def spawn_initial_obstacles(self) -> None:
        """Populate the grid with a random number (min..max) of obstacles,
        avoiding the frog's starting cell.
        """
        self.obstacles.clear()
        n = random.randint(self.min_obstacles, self.max_obstacles)
        attempts = 0
        while len(self.obstacles) < n and attempts < n * 10 + 100:
            r = random.randrange(self.rows)
            c = random.randrange(self.cols)
            if (r, c) == self.frog:
                attempts += 1
                continue
            self.obstacles.add((r, c))
            attempts += 1

    def in_bounds(self, cell: Cell) -> bool:
        r, c = cell
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, cell: Cell) -> List[Cell]:
        """Return the 6 neighboring cells for an even-row offset hex grid."""
        r, c = cell
        # Use even-row offset convention: even rows are shifted right
        if r % 2 == 0:
            # even row
            offsets = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        else:
            # odd row
            offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        res: List[Cell] = []
        for dr, dc in offsets:
            nb = (r + dr, c + dc)
            if self.in_bounds(nb):
                res.append(nb)
        return res

    def is_edge(self, cell: Cell) -> bool:
        r, c = cell
        return r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1

    def add_obstacle(self, r: int, c: int) -> bool:
        """Attempt to place an obstacle at (r,c).

        Returns True if an obstacle was placed, False otherwise (out of bounds,
        already an obstacle, or the frog's cell).
        """
        cell = (r, c)
        if not self.in_bounds(cell):
            return False
        if cell == self.frog:
            return False
        if cell in self.obstacles:
            return False
        self.obstacles.add(cell)
        return True

    def shortest_path_to_edge(self) -> List[Cell]:
        """Return the shortest path from the frog to any edge cell as a list
        of cells (including start and end). If no path exists, return [].
        Uses BFS for an unweighted grid.
        """
        start = self.frog
        if self.is_edge(start):
            return [start]

        q = deque([start])
        visited = {start}
        parent: Dict[Cell, Cell] = {}

        while q:
            cur = q.popleft()
            if self.is_edge(cur):
                # reconstruct path
                path = [cur]
                while path[-1] != start:
                    path.append(parent[path[-1]])
                path.reverse()
                return path

            for nb in self.neighbors(cur):
                if nb in visited:
                    continue
                if nb in self.obstacles:
                    continue
                visited.add(nb)
                parent[nb] = cur
                q.append(nb)

        return []

    def step_after_click(self, r: int, c: int) -> Dict:
        """Handle the player's click to place an obstacle at (r,c).

        After attempting to place the obstacle (ignored if invalid), the frog
        calculates the shortest path to any edge (avoiding obstacles). If no
        path exists => player wins. If a path exists, the frog moves one
        cell along that path. If after the move the frog is on an edge =>
        player loses.

        Returns a dict containing:
          - `added`: bool whether obstacle was added at (r,c)
          - `path`: list of cells for the full path (may be empty)
          - `moved_to`: new frog cell after the single jump
          - `status`: one of `in_progress`, `win`, `lose`
        """
        added = self.add_obstacle(r, c)

        if self.status != "in_progress":
            return {"added": added, "path": [], "moved_to": self.frog, "status": self.status}

        path = self.shortest_path_to_edge()
        if not path:
            self.status = "win"
            return {"added": added, "path": [], "moved_to": self.frog, "status": self.status}

        # path includes frog position at index 0; move one adjacent cell along that path
        if len(path) >= 2:
            start = self.frog
            # prefer the immediate next step if it's adjacent; otherwise pick the
            # first cell along the path that is adjacent to the start (defensive)
            next_cell = None
            neighbors = set(self.neighbors(start))
            if path[1] in neighbors:
                next_cell = path[1]
            else:
                for p in path[1:]:
                    if p in neighbors:
                        next_cell = p
                        break
            if next_cell is not None:
                self.frog = next_cell

        if self.is_edge(self.frog):
            self.status = "lose"

        return {"added": added, "path": path, "moved_to": self.frog, "status": self.status}

    def get_state(self) -> Dict:
        """Return a JSON-serializable snapshot of the current game state."""
        return {
            "rows": self.rows,
            "cols": self.cols,
            "frog": self.frog,
            "obstacles": list(self.obstacles),
            "status": self.status,
        }

