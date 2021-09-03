import csv
import time
from pprint import pprint

DATA_PATH = 'docs/dataset2_Python+P7.csv'
CLIENT_WALLET = 500


def run():
    start_time = time.time()
    actions = read_csv(DATA_PATH)
    actions = clean_dataset(actions)
    for action in actions:
        gain_compute(action)
    choice = optimized(CLIENT_WALLET, actions)
    total_time = time.time() - start_time
    print("Actions to buy : ")
    tot_cost = 0
    tot_balance = 0
    tot_gain = 0

    pprint(choice)
    for action in choice:
        print(f"{action['name']:>15} {action['gain']:>20}")
        tot_cost += int(float(action["price"]))
        tot_balance += int(float(action['balance']))
        tot_gain += int(float(action["gain"]))
    print(f" Cost : {tot_cost}, Gain : {tot_gain},"
          f" balance: {tot_balance}")
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


def clean_dataset(actions: list):
    for action in actions:
        if float(action["price"]) <= 0:
            actions.remove(action)
        if float(action["profit"]) <= 0:
            actions.remove(action)
    return actions


def gain_compute(action: dict):
    action['gain'] = int(float(action['price']) * float(action['profit']) / 100 + float(action['price']))
    action['balance'] = int(float(action['gain']) - float(action['price']))


def optimized(wallet, actions):
    matrice = [[0 for x in range(wallet + 1)] for x in range(len(actions) + 1)]

    for i in range(1, len(actions)+1):
        for w in range(1, wallet+1):
            if int(float(actions[i-1]['price']))*100 <= w:
                matrice[i][w] = \
                    max(int(float(actions[i-1]["balance"])) + matrice[i-1][w - int(float(actions[i-1]["price"]))],
                        matrice[i-1][w])
            else:
                matrice[i][w] = matrice[i-1][w]

    w = wallet
    n = len(actions)
    actions_selection = []

    while w >= 0 and n >= 0:
        a = actions[n-1]
        if matrice[n][w] == matrice[n - 1][w - int(float(a["price"]))] + int(float(a["balance"])):
            actions_selection.append(a)
            w -= int(float(a["price"]))
        n -= 1

    return actions_selection


run()
