import sys
from setuptools import setup, find_packages

install_requires = [
    "typing-extensions",
    "dictknife",  # for metashape.outputs
]
if sys.version_info < (3, 8):
    install_requires.append("typing-inspect")

tests_requires = ["pytest", "magicalimport"]
extras_require = {
    "testing": tests_requires,
    "dev": tests_requires + ["black", "flake8"] + ["mypy"],
    "input": ["json2python-models"],  # todo: omit
    "output": ["dictknife>=0.13.0", "prestring>=0.9.0", "magicalimport"],
}
extras_require["cli"] = (
    extras_require["input"] + extras_require["output"] + ["magicalimport>=0.9.1"]
)

setup(
    classifiers=[
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">3.7",
    packages=find_packages(exclude=["metashape.tests"]),
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=tests_requires,
    test_suite="metashape.tests",
    package_data={"metashape": ["py.typed"]},
)
