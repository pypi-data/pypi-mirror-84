import datetime

from researcher.globals import DATE_FORMAT, RESULTS_NAME, GENERAL_RESULTS_NAME
from researcher.results import FinalizedResults

class Experiment(FinalizedResults):
    def __init__(self, data):
        fold_results = data[RESULTS_NAME] if RESULTS_NAME in data else None
        general_results = data[GENERAL_RESULTS_NAME] if GENERAL_RESULTS_NAME in data else None

        super().__init__(fold_results, general_results)
        
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