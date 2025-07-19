from setuptools import setup, find_packages

setup(
    name='DuckChat_Tor',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.27.1'  # Укажите минимальную версию Selenium
    ],
    author='Tolik',
    author_email='None',
    description='Краткое описание вашей библиотеки',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='None',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
