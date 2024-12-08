from collections import defaultdict, namedtuple

from tqdm import tqdm

Resources = namedtuple("Resources", "geode obsidian clay ore", defaults=[0, 0, 0, 0])


class ResourcesMixin:
    def immediate_mul(self: Resources, rhs) -> Resources:
        return Resources(*(elema * rhs for elema in self))

    def add(self, rhs: Resources) -> Resources:
        return Resources(*(elema + elemb for elema, elemb in zip(self, rhs)))

    def substract(self, rhs: Resources) -> Resources:
        return Resources(*(elema - elemb for elema, elemb in zip(self, rhs)))


Resources.__matmul__ = ResourcesMixin.immediate_mul
Resources.__add__ = ResourcesMixin.add
Resources.__sub__ = ResourcesMixin.substract
Resources.invalid = lambda self: any((elem < 0 for elem in self))
Robots = Resources

costs = [
    Resources(ore=2, obsidian=7),
    Resources(ore=3, clay=14),
    Resources(ore=2),
    Resources(ore=4),
]


def affordable_count(resources: Resources) -> Robots:
    return Robots(
        *(
            min(
                res // cost if cost > 0 else float("inf")
                for cost, res in zip(robot_cost, resources)
            )
            for robot_cost in costs
        )
    )


def cost(robots: Robots) -> Resources:
    res = Resources()
    for cost, robot_count in zip(costs, robots):
        res = res + cost @ robot_count
    return res


def pay_cost(order: Robots, resources: Resources) -> Resources:
    return resources - cost(order)


max_time = 14 + 1
dp: list[dict[Robots, Resources]] = [
    defaultdict(Resources) for _ in range(max_time + 1)
]
dp[0][Robots(ore=1)] = Resources()


def pprint(t):
    for robots, res in dp[t].items():
        print(*robots, "-->", *res)


for time in tqdm(range(max_time), ascii=True):
    orders: dict[Robots, Robots] = defaultdict(list)
    for state, res in dp[time].items():
        geo, obs, cla, ore = affordable_count(res)
        # poor mans permutation
        for geo_robots in range(geo + 1):
            for obs_robots in range(obs + 1):
                for cla_robots in range(cla + 1):
                    for ore_robots in range(ore + 1):
                        order = Robots(geo_robots, obs_robots, cla_robots, ore_robots)
                        if not pay_cost(order, res).invalid():
                            orders[state].append(order)

    # print("Time", time, "prep phase")
    # pprint(time)
    for state, res in dp[time].items():
        dp[time][state] = state + res
    for state, state_orders in orders.items():
        for order in state_orders:
            new_res = pay_cost(order, dp[time][state])
            state = state + order
            # todo: check if the greedy choice is correct here
            dp[time + 1][state] = max(new_res, dp[time + 1][state])
    # print("Time", time, "end phase")
    # pprint(time)
    # print()

answer = max(dp[-1].values(), key=lambda x: x.geode)
print("Max geodes", answer)
