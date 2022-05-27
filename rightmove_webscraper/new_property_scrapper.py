import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from rightmove_webscraper import RightmoveData
import pandas as pd
#from pushbullet import Pushbullet
import win32com.client as win32
import pywintypes
import logging
import time
import random
import json

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib


API_KEY = "o.yzXvMKJUUgExumrvZ1wkMMt7xrIjJTC5"
logging.basicConfig(filename='logger.log', level=logging.DEBUG, format='%(asctime)s- %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

def check_new_property(rmd, mails):
    query_result_path = pathlib.Path('rightmove_results.json')
    if not query_result_path.exists():

        urls = rmd.get_results.drop_duplicates(subset='url')
        with open(query_result_path, 'w+', encoding='utf-8') as file:
            urls.to_json(file, orient='records', force_ascii=False)
        urls = urls['url'].values
    else:
        urls = pd.read_json(query_result_path)
        urls = urls['url'].values

    rmd.refresh_data()
    results = rmd.get_results
    results = results.drop_duplicates(subset='url')

    for link in results['url'].values:
        if link not in urls:
            #results[results['url']== url]

            print('Saving new results to rightmove_results.json')
            with open(query_result_path, 'w+', encoding='utf-8') as file:
                results.to_json(file, orient='records', force_ascii=False)

            print(f'New property found: {link}')
            logging.info(f'New property found: {link}')
            price = results[results['url'] == link]['price'].values[0]

            address = results[results['url'] == link]['address'].values[0]
            postcode = results[results['url'] == link]['postcode'].values[0]

            # ## send push
            # pb = Pushbullet(API_KEY)
            # push = pb.push_note(address, f'price: {price} \npostcode: {postcode}\nlink: {link}')

            ## send email
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            try:
                if type(mails)== list:
                    mail.To = "; ".join([email for email in mails])
                    mail.Subject = address
                    mail.Body = f'price: {price} \npostcode: {postcode}\nlink: {link}'
                    # mail.HTMLBody =
                    mail.Send()
                else:
                    mail.To = mails
                    mail.Subject = address
                    mail.Body = f'price: {price} \npostcode: {postcode}\nlink: {link}'
                    # mail.HTMLBody =
                    mail.Send()
            except pywintypes.com_error:
                raise Exception('Email not specified in config.json')

    return rmd

import datetime

def format_time(elapsed):
    '''
    Takes a time in seconds and returns a string hh:mm:ss
    '''
    # Round to the nearest second.
    elapsed_rounded = int(round((elapsed)))

    # Format as hh:mm:ss
    return str(datetime.timedelta(seconds=elapsed_rounded))



if __name__ == "__main__":

    ## time limits
    ts_last_req = time.time()-300
    min_req_interval = 300

    PREFIX = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E61466&"

    with open("config.json", "r") as f:
        doc = json.load(f)
        url = doc["params"]
        email = doc["misc"]["mails"]

    # url


    url = PREFIX + "&".join(["=".join([key, str(url[key])]) for key in url])
    rmd = RightmoveData(url)

    while True:


        # print(ts_last_req)
        interval = time.time() - ts_last_req
        if (interval < min_req_interval):
            sleep = (random.uniform(0.8, 1) * (min_req_interval - interval))
            logging.info('Sleeping for ' + str(sleep)+ 's')
            print('Sleeping for ' + str(sleep))
            time.sleep(sleep)
        logging.info('Checking new properties... ' )
        rmd = check_new_property(rmd, email)
        ts_last_req = time.time()
        #break