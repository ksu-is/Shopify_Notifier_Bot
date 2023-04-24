import re
import requests
import config_handler

def fix_nonetypes(json_item):
    try:
        return str(json_item)
    except TypeError:
        return ""

def webhook_sender(item,stock_state,stock_info,link,url):
    if stock_state == True and stock_info == "True":
        content = config_handler.read("config.cfg","webhook","in_stock_message")
    elif stock_state == True and stock_info == "False":
        content = config_handler.read("config.cfg","webhook","out_of_stock_message")
    elif stock_state == None and stock_info == "True":
        content = config_handler.read("config.cfg","webhook","new_item_in_stock_message")
    elif stock_state == None and stock_info == "False":
        content = config_handler.read("config.cfg","webhook","new_item_out_of_stock_message")
    else:
        return

    variable_dict = {
        "{Name}" : fix_nonetypes(item['name']),
        "{Title}" : fix_nonetypes(item['title']),
        "{SKU}" : fix_nonetypes(item['sku']),
        "{Public Title}" : fix_nonetypes(item['public_title']),
        "{Option1}" : fix_nonetypes(item['option1']),
        "{Option2}" : fix_nonetypes(item['option2']),
        "{Option3}" : fix_nonetypes(item['option3']),
        "{Link}" : link,
    }

    for key in variable_dict.keys():
        content = re.sub(key, variable_dict[key], content)

    content = content.replace(r'\n', '\n')

    data = {
        "content" : content
    }

    requests.post(url,json=data)
