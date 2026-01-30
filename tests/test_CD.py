import unittest
import sys
import os

# Add parent directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CD import CD

class TestCD(unittest.TestCase):
    def setUp(self):
        self.cd = CD(
            id=1,
            name="Test CD",
            size=700.0,
            encryption_speed=52,
            occupied_space=200.0,
            session_count=2,
            session_type="Data"
        )

    def test_initialization(self):
        self.assertEqual(self.cd.id, 1)
        self.assertEqual(self.cd.name, "Test CD")
        self.assertEqual(self.cd.size, 700.0)
        self.assertEqual(self.cd.encryption_speed, 52)
        self.assertEqual(self.cd.occupied_space, 200.0)
        self.assertEqual(self.cd.session_count, 2)
        self.assertEqual(self.cd.session_type, "Data")
        self.assertTrue(self.cd.getOpenSession)  # Should be open since type is Data

    def test_get_free_space(self):
        self.assertEqual(self.cd.getFreeSpace, 500.0)

    def test_set_finalized(self):
        # Test finalizing
        self.cd.set_finalized(True)
        self.assertEqual(self.cd.session_type, "Finalized")
        self.assertFalse(self.cd.getOpenSession)

        # Test un-finalizing
        self.cd.set_finalized(False)
        self.assertEqual(self.cd.session_type, "Data")
        self.assertTrue(self.cd.getOpenSession)

    def test_to_dict(self):
        expected_dict = {
            "id": 1,
            "name": "Test CD",
            "size": 700.0,
            "encryption_speed": 52,
            "occupied_space": 200.0,
            "session_count": 2,
            "session_type": "Data",
            "free_space": 500.0,
            "is_open": True
        }
        self.assertEqual(self.cd.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()
