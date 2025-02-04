import sys
import requests
import re
import time
import json
import webhook_handler
import config_handler
import stock_state_tracker
from datetime import datetime,timezone

stock_delay = config_handler.read("config.cfg","stock","stock_delay")

url = config_handler.read("config.cfg","webhook","url")

def find_variants(url):
    convert_url = re.sub("(?<!\.js)$",".js",re.sub("\?.*",".js",url))
    find_variant = re.search("(?<=\?variant\=)\d+",url)
    stock_json = json.loads(requests.get(convert_url).text)

    if find_variant != None:
        return [find_variant.group(0), stock_json]

    else:
        return ["", stock_json]

def stock_info_handling(stock_info,stock_state_id,item_info,link):
    if stock_info == "True":
        stock_state = stock_state_tracker.find_item_state(stock_state_id,"True")
        webhook_handler.webhook_sender(item_info,stock_state,stock_info,link,url)

    elif stock_info == "False":
        stock_state = stock_state_tracker.find_item_state(stock_state_id,"False")
        webhook_handler.webhook_sender(item_info,stock_state,stock_info,link,url)
        
def stock_check_runner(request_data):
    variant_check = find_variants(request_data)

    stock_json = variant_check[1]
    find_variant = variant_check[0]

    for item in stock_json['variants']:
        if find_variant == "" or find_variant == str(item['id']):
            stock_info_handling(str(item['available']),request_data + "_" + str(item['id']),item,request_data)

    time.sleep(float(stock_delay))

if re.search("^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:/?|[/?]\S+)$", url, flags=re.IGNORECASE) == None:
    print("Webhook url not detected, exiting.")
    time.sleep(10)
    sys.exit()

with open("list.txt", "r") as urlListRaw:
    urlListLines = urlListRaw.readlines()
urlList = list(map(str.strip, urlListLines))

while True:
    try:
        for item in urlList:
            stock_check_runner(item)
    except Exception as e:
        utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        with open ("error_log.txt", "a") as log_file:
            log_file.write("\n")
            log_file.write(utc_time + ", ")
            log_file.write(str(e))