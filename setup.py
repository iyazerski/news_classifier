import setuptools

from news_classifier import __version__

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

requirements = set()
for file in ['communicator', 'worker']:
    with open(f'requirements/{file}.txt', encoding='utf-8') as fp:
        for line in fp:
            line = line.strip()
            if line.startswith('git'):  # handle private repositories
                requirements.add(f'{line.split("/")[-1].split(".git")[0]} @ {line}')
            elif not line or line.startswith('-') or line.startswith('#'):
                continue  # ignore other files including and comments
            else:
                requirements.add(line)

setuptools.setup(
    name='news_classifier',
    version=__version__,
    author='Ihar Yazerski',
    author_email='ihar.yazerski@gmail.com',
    description='Demo API for news classification',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://nws_classifier.iyazerski.me',
    packages=setuptools.find_packages(exclude=('tests*',)),
    install_requires=sorted(requirements),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
