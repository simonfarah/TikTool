from setuptools import setup

with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setup(
    name="TikTool",
    version="0.0.1",
    description="A full Tiktok library for Python",
    url="https://github.com/simonfarah/TikTool",
    author="Simon Farah",
    author_email="simonfarah@pm.me",
    license="MIT",
    package_dir={"TikTool": "TikTool"},
    packages=["TikTool"],
    install_requires=requirements,
)
