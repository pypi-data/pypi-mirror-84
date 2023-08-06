from setuptools import find_packages, setup

setup(
    name='mozart_framework',
    packages=find_packages(),
    version='1.0.9',
    description='Pacote de Framework RPA da TQI',
    long_description='### Introduction\n\nPython language framework for Robot Process Automation.\n\n### Supported Python Versions\n\nPython 3.4+\n\n### Installation\n\n```sh\n$ pip install mozart_framework\n```',
    long_description_content_type = 'text/markdown',
    author='Leander Ribeiro',
    author_email='leander.ribeiro@tqi.com.br',
    url='https://github.com/usuario/meu-pacote-python',
    install_requires=["mysql" , "psycopg2" , "pyodbc" , "openpyxl" , "requests" , "jsonpickle" , "logging" , "datetime" , "tika" , "pillow" , "pywinauto" , "selenium" , "chromedriver_autoinstaller" , "geckodriver_autoinstaller"],
    license='MIT',
    keywords=['rpa'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
)
