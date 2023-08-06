from setuptools import setup


setup(
    name="papermill-mlflow-handler",
    description="MLFlow handler for papermill.",
    long_description="MLFlow handler for papermill.",
    long_description_content_type="text/x-rst",
    version="1.0.1",
    license=["MIT"],
    packages=["papermill_mlflow_handler"],
    python_requires=">=3.6",
    install_requires=[
        "papermill",
        "mlflow",
        "google-cloud-storage"
    ],
    entry_points={"papermill.io": ["mlflow://=papermill_mlflow_handler:mlflow_handler"]},
)
