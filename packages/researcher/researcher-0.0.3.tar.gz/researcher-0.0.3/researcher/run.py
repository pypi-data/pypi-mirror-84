import datetime
import os
import time
import gc
import json
import copy

import numpy as np

from researcher.records import *
from researcher.globals import *

def reduced_params(params):
    """Create a copy of the given parameters without descriptive (human-directed) fields.
    """
    return {k: params[k] for k in params.keys() - {'title', 'notes'}}

def run_experiment(params, experiment_fn, save_path):
    cloned_params = copy.deepcopy(params)
    param_hash = get_hash(cloned_params)

    print("Commencing experiment {}\n".format(param_hash))

    # experiment_fn must return a Results instance.
    results = experiment_fn(identifier=param_hash, **reduced_params(cloned_params))

    cloned_params["hash"] = param_hash
    cloned_params["timestamp"] = datetime.datetime.now().strftime(DATE_FORMAT)
    save_experiment(save_path, "{}_{}".format(cloned_params["title"], param_hash), parameters=cloned_params, results=results.view())
    
    print("Finished experiment {}\n".format(param_hash))

    return results

