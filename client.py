"""
the script fetches all the tasks as well as uploads all the tasks for GCI
"""
import os
import json
import csv
import requests
import click
import logging

class GCIClient:

    def __init__(self, debug=False):
        """
        initialises the GCIClient class and sets basic information to
        be used with all other methods
        """

        if debug:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger('requests.packages.urllib3')
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

        self.auth_token = os.environ["GCI_API_TOKEN"]
        self.url = "https://codein.withgoogle.com/api/program/current/"
        self.headers = {
            'Authorization': 'Bearer {token}'.format(
                token=self.auth_token
            ),
            'Content-Type': 'application/json'
        }
    
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

        with open("tasks.csv", "w+", newline="\n") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "name",
                "description",
                "status",
                "max_instances",
                "mentors",
                "is_beginner",
                "tags",
                "categories",
                "time_to_complete_in_days",
                "private_metadata",
                "external_url"
            ])
            for task in tasks:
                csv_writer.writerow([
                    task["name"],
                    task["description"],
                    task["status"],
                    task["max_instances"],
                    task["mentors"],
                    str(task["is_beginner"]).lower(),
                    task["tags"],
                    ",".join(str(x) for x in task["categories"]),
                    task["time_to_complete_in_days"],
                    task["private_metadata"],
                    task["external_url"]
                ])
        
        print("all tasks saved to tasks.csv!")


@click.command()
@click.option("--verbose/--no-verbose", default=False, help="show debug information")
@click.option('--save-as', required=True, type=click.Choice(['json', 'csv']), help="format to save the tasks in")
def main(verbose, save_as):
    try:
        client = GCIClient(debug=verbose)
        
        if save_as == "json":
            client.tasks_to_json()
        elif save_as == "csv":
            client.tasks_to_csv()
    except KeyError as err:
        logging.debug(err)
        logging.error("Please set GCI_API_TOKEN environment variable first!")

if __name__ == "__main__":
    main()