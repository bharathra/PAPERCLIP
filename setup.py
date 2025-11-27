from setuptools import setup, find_packages

setup(
    name="paperclip",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main", "note_manager", "note_window", "styles"],
    install_requires=[
        "PyQt6",
    ],
    entry_points={
        "console_scripts": [
            "paperclip=main:main",
        ],
    },
)
