from setuptools import find_namespace_packages, setup

setup(
    name="sensai",
    version="0.1.0",
    description="Sensai",
    author="yudhisteer",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.115.11",
        "uvicorn>=0.34.0",
        "pydantic>=2.10.6",
        "httpx>=0.28.1",
        "requests>=2.32.3",
    ],
    extras_require={
        "dev": [
            "black>=25.1.0",
            "isort>=6.0.1",
            "mypy>=1.0.0",
        ],
    },
)
