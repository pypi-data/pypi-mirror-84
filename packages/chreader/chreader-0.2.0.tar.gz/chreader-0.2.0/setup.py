from setuptools import setup


# get the dependencies and installs
with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = []
    for line in f:
        req = line.split("#", 1)[0].strip()
        if req and not req.startswith("--"):
            requires.append(req)


VERSION = {}
with open("chreader/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)


setup(
    name="chreader",
    version=VERSION["VERSION"],
    description="An open-source Chinese NLP Dataset Reader library, built on allennlp & pytorch.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="allennlp deep learning chinese dataset reader",
    url="https://github.com/wangyuxinwhy/chreader",
    author="wangyuxin",
    author_email="wangyuxinwhy@gmail.com",
    license="MIT",
    packages=["chreader"],
    install_requires=requires,
    entry_points="""
        [console_scripts]
        chreader=scripts.cli:chreader_cli
    """,
    python_requires=">=3.6.1",
)
