import setuptools
import os

__version__ = "0.0.3"

dir_name = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir_name, "readme.md"), encoding="utf-8") as f:
	long_description = f.read()

setuptools.setup(
    name="mangamon",
    version=__version__,
    description="Manga Downloader",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="https://github.com/akhilmaskeri/mangamon",
    author="akhil maskeri",
    author_email="akhil.maskeri@gmail.com",
    license="GPLv3",
    packages=["mangamon"],
    entry_points={
        'console_scripts': ["mangamon=mangamon.command_line:main"]
    },
    classifiers=[
	'Development Status :: 3 - Alpha',
        'Programming Language :: Python',   
        'License :: Public Domain',
        'Environment :: Console',
    ],
    python_requires=">=3",
    setup_requires=["wheel"],
    install_requires=[
        "argparse >= 1.4.0",
        "requests >= 2.24.0",
        "bs4 >= 0.0.1",
        "img2pdf >= 0.4.0",
        "tabulate >= 0.8.7"
    ]
)
