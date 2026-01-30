import unittest
import os
import sys
import json
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock streamlit before imports
sys.modules['streamlit'] = MagicMock()

from CDRepository import CDRepository
from CD import CD

class TestCDRepository(unittest.TestCase):
    def setUp(self):
        self.repo = CDRepository()
        self.test_file = "test_library.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_and_get_all(self):
        cd = CD(1, "Test", 700, 52, 0, 1, "Data")
        self.repo.add(cd)
        all_cds = self.repo.getAll()
        self.assertEqual(len(all_cds), 1)
        self.assertEqual(all_cds[0].name, "Test")

    def test_delete(self):
        cd = CD(1, "Test", 700, 52, 0, 1, "Data")
        self.repo.add(cd)
        deleted = self.repo.delete(1)
        self.assertTrue(deleted)
        self.assertEqual(len(self.repo.getAll()), 0)

    def test_delete_not_found(self):
        result = self.repo.delete(999)
        self.assertFalse(result)

    def test_get_free_space(self):
        cd1 = CD(1, "Full", 700, 52, 700, 1, "Data") # 0 free
        cd2 = CD(2, "Empty", 700, 52, 0, 1, "Data")  # 700 free
        self.repo.add(cd1)
        self.repo.add(cd2)
        
        result = self.repo.getFreeSpace(500)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Empty")

    def test_get_open_sessions(self):
        cd1 = CD(1, "Open", 700, 52, 100, 1, "Data")
        cd2 = CD(2, "Closed", 700, 52, 100, 1, "Finalized")
        self.repo.add(cd1)
        self.repo.add(cd2)

        result = self.repo.getOpenSessions()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Open")

    def test_save_and_load(self):
        # Create some data
        cd = CD(1, "Saved CD", 700, 52, 123, 1, "Data")
        self.repo.add(cd)
        
        # Save
        save_result = self.repo.uploadData(self.test_file)
        self.assertTrue(save_result)
        self.assertTrue(os.path.exists(self.test_file))

        # Clear repo and load
        new_repo = CDRepository()
        load_result = new_repo.loadData(self.test_file)
        self.assertTrue(load_result)
        
        loaded_cds = new_repo.getAll()
        self.assertEqual(len(loaded_cds), 1)
        self.assertEqual(loaded_cds[0].name, "Saved CD")
        self.assertEqual(loaded_cds[0].occupied_space, 123)

if __name__ == '__main__':
    unittest.main()
