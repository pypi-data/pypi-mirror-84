# papermill-mlflow-handler

A simple handler for logging papermill outputs to a running MLFlow server.

## Usage

Ensure that an MLFlow server is running and configured.

```
papermill [OPTIONS] NOTWEBOOK_PATH mlflow://output.ipynb
```

This will log the artificat to MLFlow's tracking server at the path ``output.ipynb``.
