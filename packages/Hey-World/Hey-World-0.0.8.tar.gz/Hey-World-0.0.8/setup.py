from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='Hey-World',
    version='0.0.8',
    description='Simple hi world pip package',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Rahul Kumar',
    author_email='rahulbits2015@gmail.com',
    keywords=['Hey world'],
    url='https://github.com/RahulnKumar/Hi-World',
    download_url='https://pypi.org/project/heyworld/'
)

install_requires = [ ]

if __name__ == '__main__':
    setup(**setup_args)