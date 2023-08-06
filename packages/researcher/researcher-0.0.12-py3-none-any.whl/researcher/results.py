from collections import defaultdict

import numpy as np

VAL_PREFIX = "val_"

class Results():
    """Results provides an api to handle the collection and analysis of experiment results
    """
    def __init__(self, results=None):
        """ self.__results holds a mapping from each fold to each metric and from each metric to 
        all the recorded metric scores for that metric.
        fold -> metric -> [value, value, value, ...]
        """
        self.__results = results or []
    
    def __add_value(self, fold, name, value):
        self.__results[fold][name].append(value)

    def __integrate(self, fold, name):
        if len(self.__results) == fold:
            self.__results.append(defaultdict(lambda : []))
        if len(self.__results) < fold:
            raise ValueError("Attempt to write to fold {} when results {} only contains {} folds. It looks like a fold has been skipped".format(fold, self.__results, len(self.__results)))
        if len(self.__results) > fold + 1:
            raise ValueError("Attempt to write to fold {} when results {} contains {} folds already. We shouldn't be writing to already finalized folds.".format(fold, self.__results, len(self.__results)))

    def add(self, fold, name, value):
        self.__integrate(fold, name)
        self.__add_value(fold, name, value)

    def add_all(self, fold, name, values):
        self.__integrate(fold, name)

        for value in values:
            self.__add_value(fold, name, value)

    def get_metric(self, target_metric):
        return [metrics[target_metric] for metrics in self.__results]

    def has_metric(self, target_metric):
        # It is assumed that if a metric is in one fold it will be in every fold.
        # TODO: actually implement this constraint when metrics are being added.
        for metrics in self.__results:
            if not target_metric in metrics:
                return False
        return True

    def get_final_metric_value(self, target_metric):
        return [metrics[target_metric][-1] for metrics in self.__results]
    def get_final_val_metric_value(self, target_metric):
        return [metrics[VAL_PREFIX + target_metric][-1] for metrics in self.__results]

    def get_val_metric(self, target_metric):
        return [metrics[VAL_PREFIX + target_metric] for metrics in self.__results]

    def get_fold_aggregated_metric(self, target_metric, agg_fn):
        fold_wise = []
        for metrics in self.__results:
            fold_wise.append(metrics[target_metric][-1])

        return agg_fn(np.array(fold_wise), axis=0)
    
    def active_fold(self):
        return len(self.__results) - 1
    
    def view(self):
        return self.__results