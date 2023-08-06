import mlflow
from papermill.iorw import LocalHandler


class MLFlowHandler(LocalHandler):
    def write(self, buf, path):
        super().write(buf, path)
        mlflow.log_artifact(path)


__version__ = "1.0.0"
