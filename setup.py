from setuptools import setup

setup(
    name="snapper",
    version="1.0.0",
    packages=[
        "snapper",
        "snapper.data",
        "snapper.models",
        "snapper.widgets",
    ],
    author="Lucas Sousa",
    description="App to take screenshots and add a color background.",
    long_description=open("README.md").read(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
    ],
    install_requires=["pystray==0.19.4", "python-dotenv==1.0.0"],
    python_requires=">=3.10.0",
    entry_points={
        "console_scripts": [
            "snapper = snapper.__main__:main",
        ]
    }
)
