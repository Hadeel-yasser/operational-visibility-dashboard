import requests
import sys
from datetime import datetime, timedelta
import pandas as pd
import random



#sys.stdout.reconfigure(encoding='utf-8') #for printing non-english character in the terminal when needed

ACTIVE_DAYS = [random.randint(0, 15) for i in range(6)]
def dummy_data_generator(page=1):
    names = ["Mike Johnson", "Sarah Ali", "Lily Chen", "John Smith", "Laila Khan"]
    leave_types = ["vacation", "sick", "emergency", "special_request", "resign","excuse"]
    statuses = ["accepted", "rejected"]
    
    mock_items = []
    for i in range(20):
        
        random_days =  random.randint(0, 120) #random.choice(ACTIVE_DAYS)
        start_date = (datetime.now() - timedelta(days=random_days)).date().isoformat()
        
        mock_items.append({
            "requester": {"name": random.choice(names), "t_id": random.randint(1000, 12000)},
            "status": random.choice(statuses),
            "start_date": start_date,
            "leave_rule": {"rule_type": random.choice(leave_types)},
            "request_message": "Demo data for portfolio purposes."
        })
    
    return {
        "data": mock_items,
        "pagination": {"next": page + 1 if page < 3 else None}
    }

def get_request(use_dummy=True):
    headers = {}
    params = {"page":1}
    url = ''
    cutoff = datetime(2026, 1, 1)
    if use_dummy:
        data = dummy_data_generator(params["page"])
    else:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
    result = []
    while True:
        for item in data["data"]:
            item_date = datetime.fromisoformat(item["start_date"])
            if item_date < cutoff:
                return result
            if item["status"] == "accepted" or item["status"] == "rejected":
                tutor_req_dict = {
                "tutor_name": item["requester"]["name"],
                "tutor_id": item["requester"]["t_id"],
                "status": item["status"],
                "request_date": item["start_date"],
                "request_type": item["leave_rule"]["rule_type"],
                "reason": item["request_message"]
                }
                result.append(tutor_req_dict)
        next_page = data["pagination"].get("next")
        if not next_page:
            break  
        params["page"]=next_page #add the new parameter for the page number
        if use_dummy:
            data = dummy_data_generator(params["page"])
        else:
            response = requests.get(url, params=params, headers=headers)
            data = response.json() # update data for the next page

    return result

def save_to_csv(request_list):
    df = pd.DataFrame(request_list)
    df.to_csv("Leave_Requests.csv",index=False)


