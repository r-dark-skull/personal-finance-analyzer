#! /usr/local/bin/python3

import time
import requests
from datetime import date, timedelta


if __name__ == "__main__":
    print(f"Executing Task for : {(date.today() - timedelta(days=1)).strftime("%Y-%m-%d")}")
    requests.get(f"http://localhost:5000/analysis/save_emails_for/{(date.today() - timedelta(days=1)).strftime("%Y-%m-%d")}")
    
    time.sleep(90)

    requests.get(f"http://localhost:5000/analysis/analyze_emails")
    print("Execution Complete")
