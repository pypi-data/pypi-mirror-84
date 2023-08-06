import pathlib
from setuptools import setup


# This call to setup() does all the work
setup(
    name="airflow-ecs-fargate-executor",
    version="0.7",
    description="Apache Airflow Executor for AWS ECS and AWS Fargate",
    url="https://github.com/aelzeiny/Airflow-AWS-ECS-Fargate-Executor",
    author="Ahmed Elzeiny",
    author_email="ahmed.elzeiny@gmail.com",
    license="MIT",
    keywords = ['Apache', 'Airflow', 'AWS', 'Executor', 'Fargate', 'ECS'],
    python_requires='>=3.6.0',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=[""],
    include_package_data=True,
    install_requires=["boto3", "apache-airflow"]
)
