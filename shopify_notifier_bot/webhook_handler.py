import re
import requests
import config_handler

def fix_nonetypes(json_item):
    try:
        return str(json_item)
    except TypeError:
        return ""

def webhook_sender(item,stock_state,stock_info,link,url):
    if stock_state == False:
        return

    stock_change = ""
    if stock_state == None:
        stock_change += "New item "
    if stock_info == "True":
        stock_change += "in stock!"
    elif stock_info == "False":
        stock_change != "out of stock!"
    stock_change = stock_change.capitalize()

    variable_dict = {
        "{Stock Change}" : stock_change,
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
