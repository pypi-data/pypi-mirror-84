import datetime

from researcher.globals import DATE_FORMAT, RESULTS_NAME
from researcher.results import FinalizedResults

class Experiment(FinalizedResults):
    def __init__(self, data):
        if RESULTS_NAME in data:
            results = data[RESULTS_NAME]
        else:
            results = None

        super().__init__(results=results)
        
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