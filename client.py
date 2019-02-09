"""
the script fetches all the tasks as well as uploads all the tasks for GCI
"""
import os
import json
import requests
import logging

class GCIClient:

    def __init__(self, debug=False):
        """
        initialises the GCIClient class and sets basic information to
        be used with all other methods
        """

        self.auth_token = os.environ["GCI_API_TOKEN"]
        self.url = "https://codein.withgoogle.com/api/program/current/"
        self.headers = {
            'Authorization': 'Bearer {token}'.format(
                token=self.auth_token
            ),
            'Content-Type': 'application/json'
        }

        if debug:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger('requests.packages.urllib3')
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
    
    def list_tasks(self, tasks_url=None, page_size=100):
        """
        returns a dictionary of json encoded tasks in "results" key
        """
        if tasks_url is None:
            tasks_url = self.url + "tasks"
        resp = requests.get(
            tasks_url,
            headers=self.headers,
            params={
                'page_size': page_size,
            }
        )
        resp.raise_for_status()
        return resp.json()
    
    def list_all_tasks(self):
        """
        returns the combined JSON for all the tasks
        """
        tasks = []
        req_url = None
        while(True):
            req_resp = self.list_tasks(tasks_url=req_url)
            to_append = req_resp["results"]
            tasks.extend(to_append)
            req_url = req_resp["next"]
            if req_url is None:
                break
        return tasks
    
    def tasks_to_json(self):
        """
        saves all the tasks in json format
        """
        print("working...")
        tasks = self.list_all_tasks()
        with open("tasks.JSON", "w+") as j_file:
            json.dump(tasks, j_file)
        print("all tasks saved to tasks.JSON!")

    def tasks_to_csv(self):
        """
        saves all the tasks in csv format
        """
        print("working...")
        tasks = self.list_all_tasks()
        

        with open("tasks.csv", "w+") as csv_file:
            
        print("All tasks saved to tasks.JSON!")


if __name__ == "__main__":
    client = GCIClient()
    client.tasks_to_json()
