import json

def read_state_file(json_file,dict_key):
    with open (json_file, "r") as states:
        states_dict = json.load(states)

    if dict_key in states_dict:
        return states_dict[dict_key]

    else:
        return "New Item"

def write_state_file(json_file,dict_key,value):
    with open (json_file, "r") as states:
        states_dict = json.load(states)

    states_dict[dict_key] = value

    with open (json_file, "w") as states:
        json.dump(states_dict, states)

def find_item_state(item,stock_state):
    item_list_combined = "".join(item)

    read_stock = read_state_file("stock_state.json",item_list_combined)

    if stock_state == read_stock:
        return False
    elif read_stock == "New Item":
        write_state_file("stock_state.json",item_list_combined,stock_state)
        return None
    else:
        write_state_file("stock_state.json",item_list_combined,stock_state)
        return True
