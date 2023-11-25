import logging
import os
import requests # The library we use to send requests to the API

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

##################################################
################ MongoDB Functions ############### 
##################################################


def get_brevets():
    """
    Obtains the newest document in the collection in brevet_database.
    Returns the total brevet distance, the date_time for the start of the race, and a dictionary of 
    brevet control data including the control distance, open time, and close time.
    """
    # Get documents in brevets_database from the API
    brevet_collection = requests.get(f"{API_URL}brevets").json()

    # We really only want the last part
    brevet = brevet_collection[-1]

    # Return the needed information
    return brevet["total_distance"], brevet["date_time"], brevet["control_data"]

def insert_brevets(total_distance, date_time, control_data):
    """
    Inserts a new brevet list of dictionaries into the database "brevets", under the collection "brevets".
    
    Inputs a list of dictionaries 

    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    # Send a post request to the API
    _id = requests.post(f"{API_URL}brevets", json={"total_distance": total_distance, "date_time": date_time, "control_data": control_data}).json()
    
    # Format the id into a string and send back
    return str(_id)




