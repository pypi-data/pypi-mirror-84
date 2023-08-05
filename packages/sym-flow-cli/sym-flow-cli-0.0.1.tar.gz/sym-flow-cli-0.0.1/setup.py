from typing import Any, Dict

import setuptools

version: Dict[str, Any] = {}
exec(open("sym/flow/cli/version.py").read(), version)

with open("DESCRIPTION.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sym-flow-cli",
    version=version["__version__"],
    author="SymOps, Inc.",
    author_email="pypi@symops.io",
    description="The CLI for authoring Sym Flows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symopsio/runtime/sym-flow-cli",
    packages=setuptools.find_namespace_packages(include=["sym.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Click",
        "PyYAML",
        "sentry-sdk",
        "validators",
        "analytics-python",
        "boto3",
        "immutables",
        "portalocker",
        "policy-sentry",
        "sym-cli",
    ],
    entry_points="""
        [console_scripts]
        symflow=sym.flow.cli.symflow:symflow
    """,
)
