from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="bridge-decision-robot",
    version="0.1.0",
    author="Bridge AI Bot",
    author_email="bridge-ai-bot@local.dev",
    description="专业级桥牌决策机器人 - 融合桥牌专业知识、AI算法和复杂工程架构",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bridge-decision-robot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "pandas>=2.0.0",
        "stable-baselines3>=2.0.0",
        "gymnasium>=0.29.0",
        "sqlalchemy>=2.0.0",
        "h5py>=3.8.0",
        "click>=8.1.0",
        "python-dateutil>=2.8.0",
        "pytz>=2023.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "rl": [
            "tensorboard>=2.13.0",
            "tqdm>=4.66.0",
        ],
        "cli": [
            "rich>=13.5.0",
            "typer>=0.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bridge-robot=bridge_decision_robot.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bridge-decision-robot/issues",
        "Source": "https://github.com/yourusername/bridge-decision-robot",
    },
)
