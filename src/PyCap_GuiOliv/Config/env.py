import os

def env(key : str) -> str:
    return os.getenv(key)