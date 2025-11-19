from CDRepository import CDRepository
from CDService import CDService
from CDController import CDController
from CDView import CDView
from IndexView import IndexView

class IndexController:
    def __init__(self):
        self._indexView = IndexView()
  
        self._repository = CDRepository()
        self._service = CDService(self._repository)
        self._cdView = CDView()
        self._cdController = CDController(self._service, self._cdView)

    def executeOption(self, option: int):
        passToCDController = 1
        handleReports = 2
        saveLoadData = 3
        if option == passToCDController:
            self._cdController.run() 
        elif option == handleReports:
            self.run_reports()
        elif option == saveLoadData:
            self.save_load_data() 
        elif option == 0:
            self._indexView.show("Exiting...")
        else:
            self._indexView.show("Invalid option.")

    def run_reports(self):
        while True:
            choice = self._indexView.showFilteringOptions()
            sortByName = 1
            sortBySize = 2
            sortBySpeed = 3
            filterByFreeSpace = 4
            getOpenSessions = 5
            exitOption = 0
            result_list = []
            if choice == sortByName:
                result_list = self._service.sortByName()
                self._cdView.showList(result_list)
            elif choice == sortBySize:
                result_list = self._service.sortBySize()
                self._cdView.showList(result_list)
            elif choice == sortBySpeed:
                result_list = self._service.sortBySpeed()
                self._cdView.showList(result_list)
            elif choice == filterByFreeSpace:
                try:
                    min_space = float(input("Enter minimum free space (MB): "))
                    result_list = self._service.filterByFreeSpace(min_space)
                    self._cdView.showList(result_list)
                except ValueError:
                    self._indexView.show("Invalid number.")
            elif choice == getOpenSessions:
                result_list = self._repository.getOpenSessions()
                self._cdView.showList(result_list)
            elif choice == exitOption:
                break
            else:
                self._indexView.show("Invalid choice.")


    def save_load_data(self):
        print("\n--- Save/Load ---")
        print("1. Save Data")
        print("2. Load Data")
        try:
            choice = int(input("Choice: "))
            filepath = "cd_library.dat" 
            if choice == 1:
                success = self._repository.uploadData(filepath)
                self._indexView.show("Data saved." if success else "Save failed.")
            elif choice == 2:
                success = self._repository.loadData(filepath)
                self._indexView.show("Data loaded." if success else "Load failed.")
        except ValueError:
            self._indexView.show("Invalid choice.")


    def run(self):  # Dummy data for testing
        self._repository.loadData("dummy.dat")
        self._service.add("Album 1", 700, 52, 250, 1, "music")
        self._service.add("Windows XP ISO", 700, 24, 680, 1, "finalized")
        self._service.add("My Backups", 800, 52, 150, 3, "data")
        
        while True:
            option = self._indexView.showMainMenu()
            self.executeOption(option)
            if option == 0:
                break
    
if __name__ == "__main__":
    app = IndexController()
    app.run()