from CDService import CDService
from CDView import CDView

class CDController:   
    def __init__(self, cd_service: CDService, cd_view: CDView):
        self._service = cd_service
        self._view = cd_view

    def searchCD(self, cd_id: int):
        print(f"\n--- Searching for ID {cd_id} ---")
        cd = self._service.find_by_id(cd_id)
        if cd:
            self._view.show(str(cd))
        else:
            self._view.show(f"Error: CD with ID {cd_id} not found.")

    def run(self):
        while True:
            choice = self._view.showMainMenu()
            invalidCD = -1
            showAllCD = 1
            addCD = 2
            findByID = 3
            goBack = 4
            if choice == showAllCD: 
                cds = self._service.get_all_cds()
                self._view.showList(cds)
            elif choice == addCD: 
                data = self._view.showAdd()
                if data:
                    success = self._service.add(**data) 
                    if success:
                        self._view.show("CD added successfully.")
                    else:
                        self._view.show("Error: Could not add CD.")
            elif choice == findByID:
                cd_id = self._view.readId()
                if cd_id != invalidCD:
                    self.searchCD(cd_id)
            elif choice == goBack:
                break
            else:
                self._view.show("Invalid choice, please try again.")