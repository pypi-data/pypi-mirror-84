from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='larkinlab',
    version='0.0.13',
    description='A collection of code I have either made or found that helps streamline things. For Data Analysis.',
    long_description= open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Conor Larkin',
    author_email='conor.larkin16@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='data',
    packages=find_packages(),
    install_requires=["pandas", "numpy", "matplotlib", "seaborn"]
)