class IndexView:
    def __init__(self):
        pass

    def showMainMenu(self) -> int:
        print("\n=== Personal CD Library ===\n")
        print("1. Manage CDs")
        print("2. Show Reports (Sorting/Filtering)")
        print("3. Save/Load Data")
        print("0. Exit")
        try:
            choice = int(input("Enter your choice: "))
            return choice
        except ValueError:
            print("Invalid input.")
            return -1

    def showFilteringOptions(self) -> int:
        print("\n--- Reports Menu ---")
        print("1. Sort by Name")
        print("2. Sort by Size")
        print("3. Sort by Speed")
        print("4. Filter by Free Space > (you will be prompted)")
        print("5. Show CDs with Open Sessions")
        print("0. Back")
        try:
            choice = int(input("Enter choice: "))
            return choice
        except ValueError:
            return -1

    def show(self, item: str):
        print(item)