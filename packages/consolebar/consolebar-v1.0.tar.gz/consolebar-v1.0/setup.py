from distutils.core import setup

VERSION = "v1.0"

setup(
    name = "consolebar",
    packages = ["consolebar"],
    version = VERSION,
    license = "MIT",
    description = "Stunning progress bars for consoles for showing progress of python loops!",
    author = "Abhay Tripathi",
    author_email = "abhay.triipathi@gmail.com",
    url = "https://github.com/AbhayTr/ConsoleBar",
    download_url = "https://github.com/AbhayTr/ConsoleBar/archive/" + VERSION + ".tar.gz",
    keywords = ["Console", "Progress Bar", "Python Progress Bar", "Console Progress Bar"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
