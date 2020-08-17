#!/usr/bin/env python3.8

import json
import requests
import argparse
from pprint import pprint
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class EVE_API:
    def __init__(self, ip):
        self.ip = ip
        self.userpass = None
        self.html5 = -1  # To log in as native console and to see IP/Port of nodes
        self.cookies = None
        self.api_url = ""  # http://{ip}/api
        self.current_lab = ""  # http://{ip}/api/labs/{key}//{name}/nodes
        self.current_lab_name = ""
        self.session = {}
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.name_id = {}  # {"vIOS1": 1, "vIOS2": 2}

    def persist_session(self):
        """
        A function to used the data on the login function to login on EVE-NG & store the date of the session
        """
        ip = self.ip
        self.api_url = f"http://{ip}/api"
        self.session = requests.Session()
        login_url = self.api_url + "/auth/login"

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        try:
            r = self.session.post(login_url, data=json.dumps(self.userpass))
            r_content = r.json()

            if r_content.get("code") == 200:
                print(r_content.get("message"))
                self.list_folders()

            elif r_content.get("code") != 200:
                print(r_content.get("message"))
                self.session = {}

        except Exception as e:
            print(str(e))
            self.session = {}
            return

    def login(self, username, password):
        """
        A function to store the credentials needed to login on EVE-NG
        """
        self.userpass = {
            "username": username,
            "password": password,
            "html5": self.html5,
        }

        self.persist_session()

    def logout(self):
        """
        A function to logout on EVE-NG( WORK IN PROGRESS)
        """
        logout_url = "/auth/logout"
        if self.session:
            self.get(logout_url)
            self.session = {}

    def get(self, url):
        """
        A function for GET requests
        """
        response = requests.get(
            url=url, headers=self.headers, cookies=self.session.cookies
        )
        data = response.json()
        return data

    def list_folders(self):
        """
        A function to get all the names of the folders that a user have
        """
        url_folders = f"{self.api_url}/folders/"
        data = self.get(url_folders)

        folders_in_root = list()
        for folders in data["data"]["folders"]:
            folders_in_root.append(folders["name"])

        self.open_folders(folders_in_root)

    def open_folders(self, folders):
        """
        A function to get the labs path on all folders of the user
        """
        lab_paths = list()  # from path = [/Labfolder//myLab.unl]

        for folder in folders:
            url_labs = f"{self.api_url}/folders/{folder}/"
            data = self.get(url_labs)

            for labs in data["data"]["labs"]:
                lab_paths.append(labs["path"])

        print("\nHere are your folders and labs:")
        self.convert_to_dict(lab_paths)

    def convert_to_dict(self, labPath_list):
        """
        A function that convert the paths(/Labfolder//myLab.unl) of the lab to a dictionary. EX:
        {'MyLabs': ['test_lab.unl'], 'TestLab': ['MPLS.unl', 'OSPF LAB.unl']}
        """
        c = list()  # [('folder1', 'lab1.unl'), ('folder2', 'lab_1.unl')]

        for a in labPath_list:
            x = re.split("/([^/]+)/([^/]*)/", a)
            without_empty_strings = [string for string in x if string != ""]
            c.append(tuple(without_empty_strings))

        key_value = dict()
        for folder, lab in c:
            key_value.setdefault(folder, []).append(lab)

        for key, value in key_value.items():
            remove_unl = [n.split(".unl")[0] for n in value]
            print(f'The folder "{key}" has the ff labs:', remove_unl)

        self.list_nodes(key_value)

    def list_nodes(self, kv):
        """
        A function to list the nodes(Name - Image - ID) on the lab chosen by the user
        and to create a dictiory(name_id) for the node names and ID on the lab
        """
        self.name_id.clear()  # To clear the empty the dict if a user changed folder/lab

        while True:
            name = input("\nEnter the lab name, you want to work on: ") + ".unl"
            if any(name in values for values in kv.values()):
                for key in kv.keys():
                    if name in kv[key]:
                        self.current_lab = f"{self.api_url}/labs/{key}//{name}/nodes"
                        self.current_lab_name = f"{name}"
                        data = self.get(self.current_lab)
                        # pprint(data)
                        for ele in data.values():
                            if isinstance(ele, dict):
                                print(
                                    "\nHere are the nodes on the lab: (Name - Image - ID)"
                                )
                                for k, v in ele.items():
                                    devices = (
                                        f'  {v["name"]} - {v["image"]} - {v["id"]}'
                                    )
                                    print(devices)
                                    self.name_id.update({v["name"]: str(v["id"])})
                        # print(self.name_id)
                        self.menu()

            else:
                print("Incorrect lab name, Try again!")
                self.list_folders()

    def menu(self):
        """
        A function that serves as a menu to give options available
        """
        choice = input(
            "\n"
            + "=" * 50
            + """\n Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: """
        )
        if choice == "1":
            print("\n" + "=" * 50)
            self.all_nodes()
        elif choice == "2":
            print("\n" + "=" * 50)
            self.half_nodes_1()
        elif choice == "3":
            print("\n" + "=" * 50)
            self.start_node_name()
        elif choice == "4":
            print("\n" + "=" * 50)
            self.number_nodes()
        elif choice == "5":
            print("\n" + "=" * 50)
            self.list_active_node()
        elif choice == "6":
            print("\n" + "=" * 50)
            self.stop_node_name()
        elif choice == "7":
            print("\n" + "=" * 50)
            self.stop_all_nodes()
        elif choice == "8":
            print("\n" + "=" * 50)
            self.list_folders()
        elif choice.upper() == "Q":
            print("\n" + "=" * 50)
            print("Session Terminated")
            exit()
        else:
            print("Invalid input, Try again!")
            self.menu()

    def all_nodes(self):
        """
        A function that start all nodes on the chosen lab
        """

        print(f"\nStarting all nodes:")
        url_start = f"{self.current_lab}/start"
        data = self.get(url_start)
        if data["status"] == "success":
            print(f"\nAll nodes{list(self.name_id.keys())} has been started!")

        self.menu()

    def half_nodes_1(self):
        """
        A function that start half of the nodes on the chosen lab
        """
        d1 = dict(list(self.name_id.items())[len(self.name_id) // 2 :])
        d2 = dict(list(self.name_id.items())[: len(self.name_id) // 2])
        for k, v in d2.items():
            print(f"\nStarting {k} with node id of {v}:")
            url_start = f"{self.current_lab}/{v}/start"
            data = self.get(url_start)
            if data["status"] == "success":
                print(f"\n{k} had started")

            else:
                print(data["status"])
                break
        while True:
            start_back = input("\nDo you want to start the remaining nodes? (y/n): ")
            if start_back.lower() == "n":
                self.menu()
            elif start_back.lower() == "y":
                self.half_nodes_2(d1)
            else:
                print("Incorrect Input, Try again!")

    def half_nodes_2(self, d1):
        """
        A function that start the remaining nodes
        """
        for k, v in d1.items():
            print(f"\nStarting {k} with node id of {v}:")
            url_start = f"{self.current_lab}/{v}/start"
            data = self.get(url_start)
            if data["status"] == "success":
                print(f"\n{k} had started")

            else:
                print(data["status"])
                break

        self.menu()

    def start_node_name(self):
        """
        A function that start the nodes inputted by the user
        """
        while True:
            node_name = input(
                "\nEnter the node names separated by space or comma. input 'back' to go back on the menu: "
            )
            n_name = node_name.replace(",", " ")
            l_node = n_name.split()
            l_node = list(dict.fromkeys(l_node))  # remove duplicate input

            for nodes in l_node:
                if nodes.lower() == "back":
                    self.menu()
                elif any(nodes in key for key in self.name_id.items()):
                    print(f"\nStarting node {nodes}:")
                    url_start = f"{self.current_lab}/{self.name_id[f'{nodes}']}/start"
                    data = self.get(url_start)
                    if data["status"] == "success":
                        print(f"\n{nodes} had started")

                else:
                    print(
                        f"\nThe node name: ({nodes}) is not part of the lab or incorrect"
                    )
            self.start_node_name()

    def number_nodes(self):
        """
        A function that start a number of nodes inputted by the user
        """
        num_list = list(self.name_id.values())

        print(f"The lab ({self.current_lab_name}) has {len(num_list)} nodes")
        while True:
            node_number = input(
                "\nEnter the number of nodes you want to start, or type (back) to return on the menu: "
            )
            if node_number.lower() == "back":
                self.menu()

            elif not node_number.isdigit():
                print("Input is not a number, try again!")
                self.number_nodes()

            else:
                id_num = list()
                num_node = int(node_number)
                if num_node > len(num_list):
                    print(
                        "Entered number of nodes is more than the lab has, Try again!"
                    )

                elif num_node <= len(num_list):
                    print(f"\nStarting {num_list} nodes:")
                    for n in range(1, num_node + 1):
                        id_num.append(num_list[n - 1])

                    for nodes in id_num:
                        if any(nodes in v for v in self.name_id.values()):
                            url_start = f"{self.current_lab}/{nodes}/start"
                            data = self.get(url_start)
                            if data["status"] == "success":
                                print(
                                    f"{list(self.name_id.keys())[list(self.name_id.values()).index(nodes)]} had started"
                                )

                    self.number_nodes()

    def list_active_node(self):
        """
        A function that list all the active nodes and telnet IP/Port
        """

        for k, v in self.name_id.items():
            url_nodes = f"{self.current_lab}/{v}"
            data = self.get(url_nodes)
            telnet_ip = data["data"]["url"]
            ip = telnet_ip.split("telnet://")[1]

            if data["data"]["status"] == 2:
                print(f"Node {k} is currently Active with telnet IP/Port: {ip}")

            elif data["data"]["status"] == 0:
                print(f"Node {k} is Not Active")

            else:
                pprint(data)

        self.menu()

    def stop_node_name(self):
        """
        A function that stops all the nodes inputted by the user
        """
        while True:
            node_name = input(
                "\nEnter the node names separated by space or comma. input 'back' to go back on the menu: "
            )
            n_name = node_name.replace(",", " ")
            l_node = n_name.split()
            l_node = list(dict.fromkeys(l_node))  # remove duplicate input

            for nodes in l_node:
                if nodes.lower() == "back":
                    self.menu()
                elif any(nodes in key for key in self.name_id.items()):
                    print(f"\nStopping node {nodes}:")
                    url_start = f"{self.current_lab}/{self.name_id[f'{nodes}']}/stop"
                    data = self.get(url_start)
                    # pprint(data)
                    if data["status"] == "success":
                        print(f"\n{nodes} has been stopped")

                else:
                    print(
                        f"\nThe node name: ({nodes}) is not part of the lab or incorrect"
                    )
            self.stop_node_name()

    def stop_all_nodes(self):
        """
        A function that stops all the nodes inputted by the user
        """
        print(f"\nStopping all nodes:")
        url_stop = f"{self.current_lab}/stop"
        data = self.get(url_stop)
        if data["status"] == "success":
            print(f"\nAll nodes {list(self.name_id.keys())} has been stopped!")
            self.menu()
        else:
            print(data.get("message"))


# Things to do:
# Integrate open vmx
# integrate open securecrt
# add an argument on argparse for known folder, labs, nodes to start or just up to list all nodes on a lab


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--default",
        action="store_true",
        dest="default",
        help="Use default Username, Password and IP.",
    )
    parser.add_argument(
        "-ip", "--ip_address", type=str, dest="ip", help="Eve-NG Sever IP Address."
    )
    parser.add_argument(
        "-user", "--username", type=str, dest="username", help="Eve-NG GUI Username."
    )
    parser.add_argument(
        "-pass", "--password", type=str, dest="password", help="Eve-NG GUI Password.",
    )

    args = parser.parse_args()

    # Could not differentiate mutually inclusive and exclusive on argparse methods so I created the ff instead:
    dict_args = vars(args)
    list_values = list(dict_args.values())

    if list_values.count(None) == 3 and list_values.count(True) == 1:
        print("Using default IP and Credentials")
        ca = EVE_API("192.168.85.128").login("admin", "eve")

    elif list_values.count(None) == 0 and list_values.count(False) == 1:
        print("Using given IP, Username, and Password")
        EVE_API(args.ip).login(args.username, args.password)

    elif list_values.count(None) > 0 < 3 and list_values.count(False) == 1:
        print("One or more of the ff:(IP, Username, and Password) is needed.")

    elif list_values.count(None) >= 0 and list_values.count(True) == 1:
        print(
            "(-d)default credentials will not work if there is a given IP, Username, Password"
        )

    elif list_values.count(None) >= 1 and list_values.count(False) == 1:
        print(
            "One of the following: (IP, Username, and Password) are not set, add -d to use default EVE-NG GUI IP & Credentials is not set"
        )


if __name__ == "__main__":
    main()

