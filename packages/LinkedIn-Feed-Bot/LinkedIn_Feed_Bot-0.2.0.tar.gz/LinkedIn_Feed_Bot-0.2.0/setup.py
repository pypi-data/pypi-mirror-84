import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LinkedIn_Feed_Bot",
    version="0.2.0",
    author="Adriel Martins",
    author_email="am.adriel.martins@gmail.com",
    description="LinkedIn Feed crawler with Selenium.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Martins6/LinkedIn_Feed_Bot",
    packages=setuptools.find_packages(), 
    install_requires=[
          'selenium',
          'pandas',
          'xhtml2pdf',
          'markdown',
          'webdriver_manager'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.0',
    
)