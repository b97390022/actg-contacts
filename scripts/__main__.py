import subprocess


def prepare():
    subprocess.run(["pre-commit install"], check=False, shell=True)

def audit():
    subprocess.run(["pip-audit -r ./requirements.txt"], check=False, shell=True)

def lint():
    subprocess.run(["pylint ./src"], check=False, shell=True)

def build(option: str):
    subprocess.run([
        f"poetry export --without-hashes --format=requirements.txt > requirements.txt && docker buildx build --platform linux/amd64 -t shau1943/actg-contacts:latest . {option}",
    ], check=False, shell=True)

def build_load():
    build("--load")

def build_push():
    build("--push")

def start():
    subprocess.run([
        "python -m src.main",
    ], check=False, shell=True)

def test():
    subprocess.run([
        "pytest tests/",
    ], check=False, shell=True)
