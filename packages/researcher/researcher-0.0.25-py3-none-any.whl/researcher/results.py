from collections import defaultdict

import numpy as np

from researcher.globals import *

class Results():
    """Results provides an api to handle the collection and analysis of experiment results
    """
    def __init__(self, results):
        """ self.fold_results holds a mapping from each fold to each metric and from each metric to 
        all the recorded metric scores for that metric.
        fold -> metric -> [value, value, value, ...]
        """

        if results is None:
            self.results = {
                FOLD_RESULTS_NAME: [],
                GENERAL_RESULTS_NAME: {},
            }
        elif isinstance(results, dict):
            if FOLD_RESULTS_NAME not in results and GENERAL_RESULTS_NAME not in results:
                # assume we are just being passed some general results
                self.results = {
                    FOLD_RESULTS_NAME: [],
                    GENERAL_RESULTS_NAME: results,
                }
            elif FOLD_RESULTS_NAME in results and GENERAL_RESULTS_NAME in results and len(results) == 2:
                    self.results = results
            elif FOLD_RESULTS_NAME in results and len(results) == 1:
                self.results = results
                self.results[GENERAL_RESULTS_NAME] = {}
            elif GENERAL_RESULTS_NAME in results and len(results) == 1:
                self.results = results
                self.results[FOLD_RESULTS_NAME] = []
            else:
                raise ValueError(f"cannot initialize a Results instance from {results}")
        elif isinstance(results, list):
            self.results = {
                FOLD_RESULTS_NAME: results,
                GENERAL_RESULTS_NAME: {},
            }
        else:
            raise ValueError(f"cannot initialize a Results instance from {results} of type {type(results)}")

        self.fold_results = self.results[FOLD_RESULTS_NAME]
        self.general_results = self.results[GENERAL_RESULTS_NAME]

class ResultBuilder(Results):
    def __init__(self):
        super().__init__(None)

        self.__fold_metric_names = set()

    def __add_fold_value(self, fold, name, value):
        self.fold_results[fold][name].append(value)

    def __integrate(self, fold, name):
        if len(self.fold_results) == fold:
            self.fold_results.append(defaultdict(lambda : []))
        if len(self.fold_results) < fold:
            raise ValueError("Attempt to write to fold {} when results {} only contains {} folds. It looks like a fold has been skipped".format(fold, self.fold_results, len(self.fold_results)))
        if len(self.fold_results) > fold + 1:
            raise ValueError("Attempt to write to fold {} when results {} contains {} folds already. We shouldn't be writing to already finalized folds.".format(fold, self.fold_results, len(self.fold_results)))

    def set_general_metric(self, name, value):
        self.add(GENERAL_RESULTS_NAME, name, value)

    def set_general_metrics(self, result_dict):
        for key, value in result_dict.items():
            self.add(GENERAL_RESULTS_NAME, key, value)

    def add(self, fold, name, value):
        if fold is None or fold == GENERAL_RESULTS_NAME:
            if name in  self.__fold_metric_names:
                raise ValueError(f"metric name {name} has already been given to a fold metric {self.fold_results}, adding it to general results")
            if name in self.general_results.keys():
                raise ValueError(f"metric name {name} already exists in general results: {self.general_results}")
            
            self.general_results[name] = value

        else:
            if name in self.general_results.keys():
                raise ValueError(f"metric name {name} already exists in general results {self.general_results}, adding it to the results fold {fold} would create ambiguity")

            self.__integrate(fold, name)
            self.__add_fold_value(fold, name, value)
            self.__fold_metric_names.add(name)

    def add_multiple(self, fold, name, values):
        self.__integrate(fold, name)

        for value in values:
            self.__add_fold_value(fold, name, value)

    def active_fold(self):
        return len(self.fold_results) - 1

class FinalizedResults(Results):
    def __init__(self, results):
        super().__init__(results=results)

    def get_metric(self, target_metric):
        if target_metric in self.general_results:
            return self.general_results[target_metric]

        return [metrics[target_metric] for metrics in self.fold_results]

    def has_metric(self, target_metric):
        if target_metric in self.general_results:
            return True

        # It is assumed that if a metric is in one fold it will be in every fold.
        # TODO: actually implement this constraint when metrics are being added.
        for metrics in self.fold_results:
            if not target_metric in metrics:
                return False
        return True

    def get_final_metric_values(self, target_metric):
        return [metrics[target_metric][-1] for metrics in self.fold_results]

    def get_fold_aggregated_metric(self, target_metric, agg_fn):
        fold_wise = []
        for metrics in self.fold_results:
            fold_wise.append(metrics[target_metric])

        return agg_fn(np.array(fold_wise), axis=0)
    

