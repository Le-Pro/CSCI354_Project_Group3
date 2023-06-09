from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "coursepy",
    version = "1.0.1",
    description = "A course organizer that lets students map their college courses",
    packages = find_packages(include=["coursepy"]),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Le-Pro/CSCI354_Project_Group3",
    author = "Hrishav Sapkota, Sameer Acharya, Victor Iyke-Osuji",
    author_email = "hrishav.sapkota@bison.howard.edu, sameer.acharya@bison.howard.edu, victor.iykeosuji@bison.howard.edu",
    license = "MIT",
)