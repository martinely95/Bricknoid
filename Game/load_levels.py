import os
import os.path


class Levels:

    def __init__(self):
        self.current_levels = []
        self._loaded_level = []
        number_of_levels = sum(1 for item in os.listdir("levels")
                               if os.path.isfile(os.path.join("levels", item))
                               )
        for level in range(1, number_of_levels + 1):
            current_level = []
            with open('levels/' + str(level) + '.txt') as level_file:
                for line in level_file:
                    current_level.append(line)
            self.current_levels.append(current_level)

    def load_level(self, level):
        self._loaded_level = self.current_levels[level-1]

    def return_loaded_level(self):
        return self._loaded_level

    def return_number_of_levels(self):
        return len(self.current_levels)
