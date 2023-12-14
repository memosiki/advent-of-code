import enum
import logging
import sys
from copy import deepcopy
from queue import Queue

from sortedcontainers import SortedSet

logging.basicConfig(level=logging.INFO)
logger = logging.Logger(__file__)


class Battle:
    ATTACK_DMG = 3
    STARTING_HP = 200

    battlefield: list[list[str]]
    N: int  # battlefield height
    M: int  # battlefield width

    units = SortedSet()  # set of all units in battle : (x, y)
    hit_points = {}  # hit_points of units in battle : (x, y) -> health

    # battleground tiles
    class Tile(enum.Enum):
        elf = "E"
        goblin = "G"
        free = "."
        wall = "#"

    # enemies for any unit
    enemy_map = {
        Tile.elf.value: Tile.goblin.value,
        Tile.goblin.value: Tile.elf.value,
    }

    # helper template for BFS, no nodes visited
    visited_clean_template: list[list[bool]]

    def __init__(self, descr=sys.stdin):
        self.battlefield = [list(line.rstrip()) for line in descr]

        # x is primary, order is defined by (x, y)
        # -------> y
        # |
        # |
        # v x
        # since the map is walled off never do any boundary check

        self.N = len(self.battlefield)
        self.M = len(self.battlefield[0])
        self.visited_clean_template = [[False] * self.M for i in range(self.N)]

        # Gathering all units
        for x in range(self.N):
            for y in range(self.M):
                if self.battlefield[x][y] in self.enemy_map:
                    self.units.add((x, y))
                    self.hit_points[(x, y)] = Battle.STARTING_HP

    def opponents(self, x, y, type=None):
        type = type or self.battlefield[x][y]
        """Returns coord generator of enemies unit is able to fight"""
        # order (x, y)
        enemy = self.enemy_map[type]
        return (
            (a, b)
            for a, b in ((x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y))
            if self.battlefield[a][b] == enemy
        )

    def can_fight(self, x, y) -> bool:
        """Is there opponents to fight"""
        return any(self.opponents(x, y))

    def can_stand(self, x, y) -> bool:
        return self.battlefield[x][y] == Battle.Tile.free.value

    def should_move_to(self, x, y, type) -> bool:
        """Is there standable ground and opponents to fight"""
        return any(self.opponents(x, y, type)) and self.can_stand(x, y)

    def attack(self, x, y) -> bool:
        # Fight the lowest hp enemy, True if it dies
        opponent = min(
            self.opponents(x, y), key=lambda opponent: self.hit_points[opponent]
        )
        self.hit_points[opponent] -= Battle.ATTACK_DMG
        if self.hit_points[opponent] <= 0:
            logger.info("%s perished", (x, y))
            del self.hit_points[opponent]
            self.units.remove(opponent)
            (x, y) = opponent
            self.battlefield[x][y] = Battle.Tile.free.value
            return True
        return False

    def find_move(self, x, y) -> tuple | None:
        """
        BFS search of orderly lowest and nearest attack position -- order is (x,y).
        Move along found path for one step.
        """
        visited = deepcopy(self.visited_clean_template)
        path = {}  # path taken (x_next, y_next) -> (x_prev, y_prev)
        queue = Queue()
        x_start, y_start = x, y
        type = self.battlefield[x][y]
        queue.put((x_start, y_start))
        visited[x_start][y_start] = True
        while not queue.empty():
            x, y = queue.get()
            if self.should_move_to(x, y, type):
                # unwind path
                while path[x, y] != (x_start, y_start):
                    x, y = path[x, y]
                return x, y

            # traversal order (x, y)
            if not visited[x - 1][y] and self.can_stand(x - 1, y):
                visited[x - 1][y] = True
                path[(x - 1, y)] = (x, y)
                queue.put((x - 1, y))
            if not visited[x][y - 1] and self.can_stand(x, y - 1):
                visited[x][y - 1] = True
                path[(x, y - 1)] = (x, y)
                queue.put((x, y - 1))
            if not visited[x][y + 1] and self.can_stand(x, y + 1):
                visited[x][y + 1] = True
                path[(x, y + 1)] = (x, y)
                queue.put((x, y + 1))
            if not visited[x + 1][y] and self.can_stand(x + 1, y):
                visited[x + 1][y] = True
                path[(x + 1, y)] = (x, y)
                queue.put((x + 1, y))
        # no path found
        logger.info("%s is stuck. Skipping turn", (x, y))
        return None

    def move(self, old, new):
        self.hit_points[new] = self.hit_points[old]
        del self.hit_points[old]
        self.units.add(new)
        self.units.remove(old)
        x, y = old
        x1, y1 = new
        self.battlefield[x1][y1] = self.battlefield[x][y]
        self.battlefield[x][y] = Battle.Tile.free.value

    def pprint(self):
        """Debug print"""
        print("Units", len(self.hit_points), "Hp", self.hit_points)
        for x in range(self.N):
            print("".join(self.battlefield[x][y] for y in range(self.M)))

    def one_sided(self):
        # no enemies remain
        return len(set(self.battlefield[x][y] for (x, y) in self.units)) == 1

    def commence(self):
        round = 0
        while True:
            round += 1
            for unit in self.units.copy():
                if unit not in self.units:
                    # already dead (T _T')
                    continue
                (x, y) = unit

                if not self.can_fight(x, y):
                    if coords := self.find_move(x, y):
                        self.move((x, y), coords)
                        x, y = coords
                if self.can_fight(x, y):
                    self.attack(x, y)

            if self.one_sided():
                break
        self.pprint()
        print("Full rounds", round - 1)
        print("Hit points", sum(self.hit_points.values()))
        print("Outcome", (round - 1) * sum(self.hit_points.values()))


if __name__ == "__main__":
    Battle().commence()
