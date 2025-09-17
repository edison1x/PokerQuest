class TargetScoreCalculator:
    """
    A class to calculate target scores based on predefined base score data.

    This class maintains a dictionary of base scores for different levels,
    including scores for defeating small bosses and big bosses.

    Attributes:
        base_score_data (dict): A dictionary mapping levels to their score requirements.
    """
    def __init__(self):
        """
        Initialises the TargetScoreCalculator with predefined base score data.

        The base score data contains the score requirements for different levels,
        including base score, small boss score, and big boss score.
        """
        self.base_score_data = {
    0: {"Base Score": 300, "Small Boss": 450, "Big Boss": 600},
    1: {"Base Score": 500, "Small Boss": 750, "Big Boss": 1125},
    2: {"Base Score": 700, "Small Boss": 1050, "Big Boss": 1575},
    3: {"Base Score": 900, "Small Boss": 1350, "Big Boss": 2025},  # 2.25x from the third above
    4: {"Base Score": 1100, "Small Boss": 1650, "Big Boss": 2475},
    5: {"Base Score": 1300, "Small Boss": 1950, "Big Boss": 2925},  
    6: {"Base Score": 1800, "Small Boss": 2700, "Big Boss": 4050},  # 2x from the third above 
    7: {"Base Score": 2300, "Small Boss": 3450, "Big Boss": 5175},  
    8: {"Base Score": 2800, "Small Boss": 4200, "Big Boss": 6300}, 
    9: {"Base Score": 3600, "Small Boss": 5400, "Big Boss": 8100},  # 2x from the third above
    10: {"Base Score": 4500, "Small Boss": 6750, "Big Boss": 10125},
    11: {"Base Score": 5500, "Small Boss": 8250, "Big Boss": 12375},
    12: {"Base Score": 7200, "Small Boss": 10800, "Big Boss": 16200},  # 2x from the third above
    13: {"Base Score": 9000, "Small Boss": 13500, "Big Boss": 20250},
    14: {"Base Score": 11000, "Small Boss": 16500, "Big Boss": 24750},
    15: {"Base Score": 14400, "Small Boss": 21600, "Big Boss": 32400},  # 2x from the third above
    16: {"Base Score": 17000, "Small Boss": 25500, "Big Boss": 38250},
    17: {"Base Score": 20000, "Small Boss": 30000, "Big Boss": 45000},
    18: {"Base Score": 25200, "Small Boss": 37800, "Big Boss": 56700},  # 1.75x from the third above
    19: {"Base Score": 32000, "Small Boss": 48000, "Big Boss": 72000},
    20: {"Base Score": 25000, "Small Boss": 37500, "Big Boss": 56250},
    21: {"Base Score": 37800, "Small Boss": 56700, "Big Boss": 85050},  # 1.5x from the third above
    22: {"Base Score": 50000, "Small Boss": 75000, "Big Boss": 112500}  
}

    def get_score_requirements(self, level):
        """
        Get the base score requirements for a given level.
        
        Parameters:
            level (int): The level for which score requirements are requested (0-22).
            
        Returns:
            dict: A dictionary containing score requirements for "Base Score", "Small Boss", and "Big Boss".

        Raises:
            ValueError: If the provided level is not between 0 and 22.
        """

        if level in self.base_score_data:
            return self.base_score_data[level]
        else:
            raise ValueError("Invalid level. Please choose a level between 0 and 10.")
