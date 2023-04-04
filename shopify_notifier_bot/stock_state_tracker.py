import json

def read_state_file(json_file,dict_key):
    with open (json_file, "r") as states:
        states_dict = json.load(states)

    if dict_key in states_dict:
        return states_dict[dict_key]

    else:
        states_dict[dict_key] = "False"
        
        with open (json_file, "w") as states:
            json.dump(states_dict, states)

        return "False"

def write_state_file(json_file,dict_key,value):
    with open (json_file, "r") as states:
        states_dict = json.load(states)

    states_dict[dict_key] = value

    with open (json_file, "w") as states:
        json.dump(states_dict, states)

def find_item_state(item,stock_state):
    item_list_combined = "".join(item)

    if stock_state == read_state_file("stock_state.json",item_list_combined):
        return False
    else:
        write_state_file("stock_state.json",item_list_combined,stock_state)
        return True
