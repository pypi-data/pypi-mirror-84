import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Varya', # Replace with your own username
    version='0.0.3',
    author='Kritik Seth',
    author_email='sethkritik@gmail.com',
    description='Machine Learning Tools',
    py_modules=[''],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kritikseth',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning'
    ],
    install_requires=[
      ],
    python_requires='>=3.6'
)