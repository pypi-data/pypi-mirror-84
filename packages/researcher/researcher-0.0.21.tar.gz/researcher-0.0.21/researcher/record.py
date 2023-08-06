import datetime
import os
import time
import gc
import json
import copy

import numpy as np

from researcher.fileutils import *
from researcher.globals import *

def reduced_params(params, unwanted_keys):
    """Create a copy of the given parameters without descriptive (human-directed) fields.
    """

    if not isinstance(unwanted_keys, set):
        unwanted_keys = set(unwanted_keys)

    return {k: params[k] for k in params.keys() - unwanted_keys}


def record_experiment(params, result_data, save_path, duration=None):
    cloned_params = copy.deepcopy(params)
    param_hash = get_hash(cloned_params)

    cloned_params["hash"] = param_hash
    cloned_params["timestamp"] = datetime.datetime.now().strftime(DATE_FORMAT)

    if duration is not None:
        cloned_params["duration"] = duration.total_seconds()

    if "title" in cloned_params:
        title = cloned_params["title"]
    else:
        title = "no_title"

    save_experiment(save_path, "{}_{}".format(title, param_hash), parameters=cloned_params, results=result_data)

