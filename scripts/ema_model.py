import pickle
import time

from ema_workbench import Model, RealParameter, ScalarOutcome
from ema_workbench.em_framework.evaluators import MPIEvaluator
# Import ema logging
from ema_workbench.util import ema_logging


def some_model(x1=None, x2=None, x3=None):
    # Print current time in seconds, HH:MM;SS, without the date
    # print(f"Starting: {time.strftime('%H:%M:%S', time.localtime())}")
    # Sleep 10 seconds
    time.sleep(0.2)
    y = x1 * x2 + x3
    # print(f"Ending: {time.strftime('%H:%M:%S', time.localtime())}, y = {y}")

    return {"y": y}


if __name__ == "__main__":
    ema_logging.log_to_stderr(level=20, set_root_logger_levels=True)

    model = Model("simpleModel", function=some_model)  # instantiate the model

    # specify uncertainties
    model.uncertainties = [
        RealParameter("x1", 0.1, 10),
        RealParameter("x2", -0.01, 0.01),
        RealParameter("x3", -0.01, 0.01),
    ]
    # specify outcomes
    model.outcomes = [ScalarOutcome("y")]

    with MPIEvaluator(model) as evaluator:
        results = evaluator.perform_experiments(scenarios=25)

    with open("ema_test.pickle", "wb") as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
