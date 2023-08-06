import datetime

from researcher.globals import DATE_FORMAT, RESULTS_NAME
from researcher.results import Results

class Experiment():
    def __init__(self, data):
        if data[RESULTS_NAME]:
            self.results = Results(data[RESULTS_NAME])
        else:
            self.results = None
        
        self.data = data
        self.timestamp = datetime.datetime.strptime(self.data["timestamp"], DATE_FORMAT)
    
    def is_trial(self):
        return "trial" in self.data and self.data["trial"]

    def get_hash(self):
        return self.data["hash"]

    def identifier(self):
        title = self.data["title"] + "_" if "title" in self.data else ""

        id = title + self.data["hash"][:8]

        if self.is_trial():
            id = "trial_" + id
        
        return id