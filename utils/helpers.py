import re
import os
import csv
from database import database


def format_number(phone):
    test = re.match("(?:2519)+\d{8}$", phone)
    return phone if test == None else f"+{phone}"


def mongo_export_to_file(collection: str):
    # make an API call to the MongoDB server
    mongo_docs = database.db[collection].find()
    print(mongo_docs)
    if database.db[collection].count_documents({}) == 0:
        return
    fieldnames = list(mongo_docs[0].keys())
    fieldnames.remove('_id')
    # compute the output file directory and name
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'report')
    print(output_dir)
    output_file = os.path.join(
        output_dir, 'report.csv')
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(mongo_docs)
    return output_file
