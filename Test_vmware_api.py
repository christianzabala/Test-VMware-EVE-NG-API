#!/usr/bin/env python3.8

import requests
import re
import subprocess
from re import search, IGNORECASE


class vmware_api:
    def __init__(self):
        self.vm_path = "C:\\Program Files (x86)\\VMware\\VMware Player\\vmrest.exe"
        self.vmrest = None  # for VMware API subprocess
        self.api_url = ""  # "http://127.0.0.1:8697/api/vms"
        self.user_pass = None  # Username: Password
        self.headers = {
            "Accept": "application/vnd.vmware.vmw.rest-v1+json",
            "Content-Type": "application/vnd.vmware.vmw.rest-v1+json",
        }
        self.vm_list = list()  # ['EVE-COMM-VM.vmx', 'PNET_2.0.3.vmx']
        self.id_vm = {}  # {'SF4992599URC1Q2BIQEBMST35RR9LFVN': 'EVE-COMM-VM.vmx'}
        self.vm_power = {}  # {'EVE-COMM-VM.vmx': {'power_state': 'poweredOn'}}

    def get(self, url):
        """
        A function for GET requests
        """
        response = requests.get(url=url, headers=self.headers, auth=self.user_pass)
        data = self.check_status_code(response)
        return data

    def put(self, url, payload):
        """
        A function for GET requests
        """
        response = requests.put(
            url=url, headers=self.headers, auth=self.user_pass, data=payload
        )
        data = self.check_status_code(response)
        return data

    def check_status_code(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code != 200:
            print(response.status_code)
            print(response.text)
            exit()

        else:
            print(response)
            exit()

    def run_vmrest(self):
        """
        A function to open VMware Workstation Player API
        """
        print(
            f"Opening VMware Workstation Player API on the app default location({self.vm_path})"
        )
        self.vmrest = subprocess.Popen(
            [self.vm_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        count = 0
        while True:
            line = self.vmrest.stdout.readline()
            if line.strip() == "":
                continue
            count += 1
            if count == 8:
                self.get_ip_port(line)
                break

        self.login_vmrest()

    def get_ip_port(self, line):
        """
        A function to get the IP address and port of the VMware Workstation API
        """
        ip_port = re.findall(r"[0-9]+(?:\.[0-9]+){3}:[0-9]+", line)
        self.api_url = f"http://{ip_port[0]}/api/vms"

    def login_vmrest(self):
        """
        A function to get the VMware API credentials, and test it if it is correct
        """
        y_n = input("\nLogin to VMware Workstation API as default(y/n): ")
        while True:
            if y_n.lower() == "y":
                self.user_pass = ("xtian", "VMware@123")
                break
            elif y_n.lower() == "n":
                username = input("Username: ")
                password = input("Password: ")
                self.user_pass = (f"{username}", f"{password}")
                break
            else:
                print("Invalid input, Try Again!")

        print("Logging in on VMware Workstation API..")
        data = requests.get(url=self.api_url, headers=self.headers, auth=self.user_pass)
        if data.status_code == 200:
            print("Login Successfull")
            print("\nChecking available VMs..")
            self.list_vms()
        elif data.status_code != 200:
            while True:
                choice = input(
                    'Invalid credentials, Input "yes" to try again, "no" to shutdown the API: '
                )
                if choice.lower() == "yes":
                    self.login_vmrest()
                elif choice.lower() == "no":
                    self.vmrest.kill()
                else:
                    print("Invalid input, Try again!")
        else:
            print(data)

    def list_vms(self):
        """
        A function to get the VM's available on the VMware Workstation
        """
        list_1 = list()  # list of items after using split from the value of path
        self.vm_list.clear()
        self.id_vm.clear()

        data = self.get(self.api_url)

        vm_path = [i["path"] for i in data if "path" in i]
        for item in vm_path:
            list_1.append(item.split("\\"))

        id_list = [i["id"] for i in data if "id" in i]

        for item in list_1:
            r = re.compile(".*.vmx$")
            for vm in filter(r.match, item):
                self.vm_list.append(vm)

        self.id_vm.update(zip(id_list, self.vm_list))

        for key, value in self.id_vm.items():
            self.vm_power.update({value: self.get(f"{self.api_url}/{key}/power")})

        print("\n" + "=" * 50)
        print("\nVMware Workstation has the following VMs:")
        for vm, power in self.vm_power.items():
            print(f'{vm.split(".vmx")[0]} - {power["power_state"]}')

        self.vm_menu()

    def get_vm_id(self, vm_name):
        vm_id = [k for k, v in self.id_vm.items() if v == vm_name]
        return vm_id[0]

    def vm_menu(self):
        """
        A function that serves as a menu to give options available
        """
        choice = input(
            "\n"
            + "=" * 50
            + """\n Select an option how to proceed:
            1 = Power on a VM
            2 = Power off a VM
            3 = show the IP address of a VM
            4 = log-in on a VM (Work in Progress)
            Q = Quit and Turn off VMware workstation API

            Please enter your choice: """
        )
        if choice == "1":
            print("\n" + "=" * 50)
            self.vm_power_on()
        elif choice == "2":
            print("\n" + "=" * 50)
            self.vm_power_off()
        elif choice == "3":
            print("\n" + "=" * 50)
            self.vm_ip()
        elif choice == "4":
            print("\n" + "=" * 50)
            self.vm_power_off()
        elif choice.upper() == "Q":
            print("\n" + "=" * 50)
            print("Session Terminated")
            self.vmrest.kill()
            exit()
        else:
            print("Invalid input, Try again!")
            self.vm_menu()

    def vm_power_on(self):

        while True:
            vm_name = (
                input("\nEnter the VM name(without .vmx) you want to power on: ")
                + ".vmx"
            )

            for vm in self.vm_list:
                if search(vm_name, vm, IGNORECASE) is not None:
                    power_url = f"{self.api_url}/{self.get_vm_id(vm_name)}/power"
                    data = self.get(power_url)

                    if data["power_state"] == "poweredOff":
                        print(f"Powering On {vm_name}:")
                        data1 = self.put(power_url, "on")

                        print(f'{vm_name} is now {data1["power_state"]}')
                        self.list_vms()

                    elif data["power_state"] == "poweredOn":
                        print(f"{vm_name} is already powered on, returning on the menu")
                        self.list_vms()

                    else:
                        print(data1)

                else:
                    print("VM name not found, Try again!")

    def vm_power_off(self):

        while True:
            vm_name = (
                input("\nEnter the VM name(without .vmx) you want to power off: ")
                + ".vmx"
            )
            for vm in self.vm_list:
                if search(vm_name, vm, IGNORECASE) is not None:
                    power_url = f"{self.api_url}/{self.get_vm_id(vm_name)}/power"
                    data = self.get(power_url)

                    if data["power_state"] == "poweredOn":
                        print(f"Powering Off {vm_name}:")
                        data1 = self.put(power_url, "off")
                        print(f'{vm_name} is now {data1["power_state"]}')
                        self.list_vms()

                    elif data["power_state"] == "poweredOn":
                        print(
                            f"{vm_name} is already powered off, returning on the menu"
                        )
                        self.list_vms()
                else:
                    print("VM name not found, Try again!")

    def vm_ip(self):
        for vm, power in self.vm_power.items():
            if power["power_state"] == "poweredOn":
                ip = self.get(f"{self.api_url}/{self.get_vm_id(vm)}/ip")
                print(f'{vm} IP address: {ip["ip"]}')

            elif power["power_state"] == "poweredOff":
                print(f"{vm} is currently powered off or still booting up")

        self.vm_menu()


vmware_api().run_vmrest()
