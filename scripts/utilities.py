
import os 

class Log: 

    def __init__(self, full_path=None, unix_file=False): 

        self.experiment_name = None
        self.timestamp = None
        self.stage = None
        self.threshold = None
        self.path = full_path 
        self.unix_file = unix_file
        if full_path is not None: 
            _, log_title = os.path.split(full_path)
            details = log_title.split("_")
            self.timestamp = details[0][len(details[0]) - 19:]
            self.stage = int(details[1][5:])
            j = 0 
            while details[2][j] != ".": 
                j += 1 
            self.threshold = float(details[2][6:j]) / 100.0