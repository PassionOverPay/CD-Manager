import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock streamlit before importing modules that rely on it
sys.modules['streamlit'] = MagicMock()

from CDService import CDService
from CD import CD

class TestCDService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = CDService(self.mock_repo)

    def test_add_cd(self):
        # Setup mock behavior
        self.mock_repo.get_next_id.return_value = 1
        self.mock_repo.add.return_value = True

        # Call the method
        result = self.service.add("New CD", 700.0, 48, 100.0, 1, "Data")

        # Verify interactions and result
        self.assertTrue(result)
        self.mock_repo.get_next_id.assert_called_once()
        self.mock_repo.add.assert_called_once()
        
        # Verify arguments passed to repo.add
        # We can't easily compare value of new_cd object because it's created inside the method
        # but we can check if it was called with a CD instance
        args, _ = self.mock_repo.add.call_args
        self.assertIsInstance(args[0], CD)
        self.assertEqual(args[0].name, "New CD")

    def test_update_status(self):
        # Mock finding a CD
        mock_cd = MagicMock()
        self.mock_repo.getAll.return_value = [mock_cd]
        mock_cd.id = 1
        
        # Call update_status
        result = self.service.update_status(1, True)

        # Verify
        self.assertTrue(result)
        mock_cd.set_finalized.assert_called_once_with(True)

    def test_update_status_not_found(self):
        self.mock_repo.getAll.return_value = []
        result = self.service.update_status(999, True)
        self.assertFalse(result)

    def test_sort_by_name(self):
        cd1 = CD(1, "B Album", 700, 52, 100, 1, "Data")
        cd2 = CD(2, "A Album", 700, 52, 100, 1, "Data")
        self.mock_repo.getAll.return_value = [cd1, cd2]

        result = self.service.sortByName()
        self.assertEqual(result, [cd2, cd1])

    def test_sort_by_size(self):
        cd1 = CD(1, "Small", 100, 52, 50, 1, "Data")
        cd2 = CD(2, "Big", 700, 52, 50, 1, "Data")
        self.mock_repo.getAll.return_value = [cd1, cd2]

        result = self.service.sortBySize()
        self.assertEqual(result, [cd2, cd1]) # Reverse order (descending)

    def test_filter_by_free_space(self):
        self.mock_repo.getFreeSpace.return_value = ["some_cd"]
        result = self.service.filterByFreeSpace(200.0)
        self.mock_repo.getFreeSpace.assert_called_with(200.0)
        self.assertEqual(result, ["some_cd"])

    def test_delete_cd(self):
        self.mock_repo.delete.return_value = True
        self.assertTrue(self.service.delete_cd(1))
        self.mock_repo.delete.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
