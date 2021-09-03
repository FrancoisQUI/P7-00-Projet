import csv
import time

DATA_PATH = 'docs/dataset2_Python+P7.csv'
CLIENT_WALLET = 500


def run():
    start_time = time.time()
    actions = read_csv(DATA_PATH)
    for action in actions:
        gain_compute(action)
    choice = optimized(actions, CLIENT_WALLET)
    total_time = time.time() - start_time
    print("Actions to buy : ")
    for action in choice["actions"]:
        print(f"{action['name']:>15} {action['gain']:>20}")
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
    action['gain'] = int(float(action['price']) * float(action['profit']) / 100 + float(action['price']))
    action['balance'] = int(float(action['gain']) - float(action['price']))


def optimized(actions, wallet: int = CLIENT_WALLET):
    best_choice = {"actions": [], "price": 0, "gain": 0, "balance": 0}
    sorted_action = sorted(actions, reverse=True, key=lambda action: action["balance"])
    client_wallet = wallet
    for action in sorted_action:
        if 0 < int(float(action["price"])) <= client_wallet and int(float(action["balance"]) > 0):
            best_choice["actions"].append(action)
            best_choice["price"] = best_choice["price"] + int(float(action["price"]))
            best_choice["gain"] = best_choice["gain"] + int(action["gain"])
            best_choice["balance"] = best_choice["balance"] + int(action["balance"])
            client_wallet = client_wallet - int(float(action["price"]))
        else:
            continue

    return best_choice


run()
