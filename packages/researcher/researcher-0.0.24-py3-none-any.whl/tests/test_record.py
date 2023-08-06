import unittest
import os
import glob

import researcher as rs

from tests.tools import TEST_DATA_PATH, TEST_EXPERIMENT_PATH

class TestSavingExperiment(unittest.TestCase):  
    def setUp(self):
        files = glob.glob(TEST_EXPERIMENT_PATH + "*")
        for f in files:
            os.remove(f)

    def test_records_correctly(self):
        params = {
            "title": "cool_experiment",
            "learning_rate": 0.003,
            "batch_size": 32,
            "alpha": 2e-9,
            "model": "rnn",
        }

        res = rs.ResultBuilder()

        for i in range(3):
            for j in range(1, 8):
                res.add(i, "rmse", 0.98 / j)

        rs.record_experiment(params, res, TEST_EXPERIMENT_PATH)

        self.assertTrue(os.path.isfile(TEST_EXPERIMENT_PATH + "cool_experiment_d45dee5991986a5b8215706f5e904b3e.json"))

    def test_records_correctly_if_given_dict(self):
        params = {
            "title": "cool_experiment",
            "learning_rate": 0.003,
            "batch_size": 32,
            "alpha": 2e-9,
            "model": "rnn",
        }

        res = rs.ResultBuilder()

        for i in range(3):
            for j in range(1, 8):
                res.add(i, "rmse", 0.98 / j)

        rs.record_experiment(params, res.fold_results, TEST_EXPERIMENT_PATH)

        self.assertTrue(os.path.isfile(TEST_EXPERIMENT_PATH + "cool_experiment_d45dee5991986a5b8215706f5e904b3e.json"))
