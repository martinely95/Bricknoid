from load_levels import Levels
import unittest


class TestLevels(unittest.TestCase):

    def setUp(self):
        self.levels = Levels()

    def test_loading_levels(self):
        for i in range(1, self.levels.return_number_of_levels() + 1):
            self.levels.load_level(i)
            current_level = self.levels.return_loaded_level()
            self.assertIsNot(current_level, [])
            print("current level:")
            print()
            for row in current_level:
                print(row)
            print()


if __name__ == '__main__':
    unittest.main()
