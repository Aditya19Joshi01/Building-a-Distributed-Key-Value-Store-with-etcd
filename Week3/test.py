import unittest

# Import the functions to be tested
from main import put_key_value, get_value_for_key, delete_key, list_all_keys

class TestEtcdOperations(unittest.TestCase):
    def setUp(self):
    # Setup method: put test data into etcd before each test case
        put_result1 = put_key_value("test_key1", "test_value1")
        put_result2 = put_key_value("test_key2", "test_value2")
        print("Put result 1:", put_result1)
        print("Put result 2:", put_result2)
        print("Keys before test:", list_all_keys())

    def test_list_all_keys(self):
    # Test listing all keys
        keys = list_all_keys()
        print("Keys during test:", keys)
        self.assertIn("test_value1", keys)
        self.assertIn("test_value2", keys)

    def tearDown(self):
        print("Cleaning up test data...")
        result1 = delete_key("test_key1")
        print("Deletion result 1:", result1)
        result2 = delete_key("test_key2")
        print("Deletion result 2:", result2)


    def test_put_and_get(self):
        # Test putting a key-value pair and retrieving its value
        put_key_value("test_key", "test_value")
        self.assertEqual(get_value_for_key("test_key"), "test_value")

    def test_delete(self):
        # Test deleting a key
        delete_key("test_key")
        self.assertIsNone(get_value_for_key("test_key"))

if __name__ == '__main__':
    unittest.main()
