import csv
from itertools import combinations

DATA_PATH = 'docs/bf-datas.csv'
CLIENT_WALLET = 500
MAX_ACTIONS = 10


def run():
    actions = read_csv(DATA_PATH)
    for action in actions:
        gain_compute(action)
    choice = bruteforce(actions, CLIENT_WALLET)
    print("Actions to buy : ")
    for action in choice["actions"]:
        print(f"{action['name']:>15}")
    print(f" Cost : {choice['price']}, Gain : {choice['gain']},"
          f" balance: {choice['gain']-choice['price']}")


def read_csv(file: str) -> list:
    """
    Read csv file
    :param file:  path to the file
    :return: list of object
    """
    with open(file, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        __data = []
        for row in reader:
            __data.append(row)

        return __data


def gain_compute(action: dict):
    action['gain'] = int(action['price']) * int(action['profit'])


def bruteforce(actions, wallet: int = CLIENT_WALLET):
    best_choice = {"actions": [], "price": 0, "gain": 0}
    for number_of_actions in range(0, MAX_ACTIONS):
        possibilities = combinations(actions, number_of_actions)
        for combination in possibilities:
            combination_price = 0
            for action in combination:
                combination_price += int(action["price"])
            if combination_price > wallet:
                continue
            else:
                combination_gain = 0
                for action in combination:
                    combination_gain += int(action["gain"])
                this_choice = {"actions": combination,
                               "price": combination_price,
                               "gain": combination_gain}
                if this_choice["gain"] > best_choice["gain"]:
                    best_choice = this_choice
    return best_choice


run()
