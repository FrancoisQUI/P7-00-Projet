import csv
from itertools import combinations
import time

DATA_PATH = 'docs/dataset1_Python+P7.csv'
CLIENT_WALLET = 500


def run():
    start_time = time.time()
    actions = read_csv(DATA_PATH)
    for action in actions:
        gain_compute(action)
    choice = bruteforce(actions, CLIENT_WALLET)
    total_time = time.time() - start_time
    print("Actions to buy : ")
    for action in choice["actions"]:
        print(f"{action['name']:>15}")
    print(f" Cost : {choice['price']}, Gain : {choice['gain']},"
          f" balance: {choice['balance']}")
    print(f"Execution time : {total_time} sc")


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
    action['gain'] = float(action['price']) * float(action['profit'])
    action['balance'] = float(action['gain']) - float(action['price'])


def bruteforce(actions, wallet: int = CLIENT_WALLET):
    best_choice = {"actions": [], "price": 0, "gain": 0, "balance": 0}
    for number_of_actions in range(0, len(actions)):
        possibilities = combinations(actions, number_of_actions)
        for combination in possibilities:
            combination_price = 0
            for action in combination:
                combination_price += float(action["price"])
            if combination_price > wallet:
                continue
            else:
                combination_gain = 0
                combination_balance = 0
                for action in combination:
                    combination_gain += float(action["gain"])
                    combination_balance += float(action["balance"])
                this_choice = {"actions": combination,
                               "price": combination_price,
                               "gain": combination_gain,
                               "balance": combination_balance}
                if this_choice["balance"] > best_choice["balance"]:
                    best_choice = this_choice
    return best_choice


run()
