from typing import List

from CD import CD

class CDView:
    def __init__(self):
        pass

    def showMainMenu(self) -> int:
        print("\n--- CD Menu ---")
        print("1. Show all CDs")
        print("2. Add new CD")
        print("3. Find CD by ID")
        print("4. Back to main menu")
        try:
            choice = int(input("Enter choice: "))
            return choice
        except ValueError:
            return 0

    def showList(self, cd_list: List[CD]):
        if not cd_list:
            print("--- No CDs to display ---")
            return
        print("--- Displaying CDs ---")
        for cd in cd_list:
            print(cd) # Uses the __str__ method

    def showAdd(self) -> dict:
        print("--- Add New CD ---")
        try:
            data = {
                "name": input("Name: "),
                "size": float(input("Total Size (MB): ")),
                "encryption_speed": int(input("Encryption Speed: ")),
                "occupied_space": float(input("Occupied Space (MB): ")),
                "session_count": int(input("Session Count: ")),
                "session_type": input("Session Type: ")
            }
            return data
        except ValueError:
            print("Error: Invalid input. Please enter numbers for size, speed, etc.")
            return None

    def readId(self) -> int:
        try:
            cd_id = int(input("Enter CD ID: "))
            return cd_id
        except ValueError:
            print("Error: Invalid ID.")
            return -1

    def show(self, item: str):
        print(item)