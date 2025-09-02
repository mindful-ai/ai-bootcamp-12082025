import mlflow
import time
import argparse
import os

def genmetric(a, b):
    return a**2 + b**2

def main(in1, in2):

    # Create an experiment
    mlflow.set_experiment("MLflow Starter Experiment")

    # MLflow run
    with mlflow.start_run():

        # Log parameters, metrics, tags
        mlflow.set_tag("Version", "1.0.0")

        mlflow.log_param("param1", in1)
        mlflow.log_param("param2", in2)

        metric = genmetric(in1, in2)
        mlflow.log_metric("Metric", metric)

        # Creation of log directory and logging
        try:
            os.mkdir("logs")
        except:
            print("Directory exits")
        log_file = os.path.join("logs", "logs.txt")
        with open(log_file, "w") as f:
            f.write(f"Artifact created at time {time.asctime()}")

        # Log the artifact
        mlflow.log_artifact(log_file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--param1", "-p1", type=int, default=5)
    parser.add_argument("--param2", "-p2", type=int, default=5)
    args = parser.parse_args()

    main(args.param1, args.param2)