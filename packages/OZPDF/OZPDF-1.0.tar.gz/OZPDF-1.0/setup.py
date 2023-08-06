import setuptools
from pathlib import Path
setuptools.setup(
    name="OZPDF",
    version=1.0,
    lon_description=Path("README.md").read_text(),
    packeges=setuptools.find_packages(exclude=["tests", "data"])
)
