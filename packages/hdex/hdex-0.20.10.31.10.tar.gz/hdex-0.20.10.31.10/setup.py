from setuptools import setup

def readme():
    with open('README.md') as f:
         return f.read()


setup(name="hdex",
	version="V0.20.10.31.10",
	description="It will genarate dictionary for your keywords",
	long_description=readme(),
    long_description_content_type='text/markdown',
	author="harsh pratap bhardwaj",
    author_email='harshpratap652@gmail.com',
	license='MIT',
	packages=['hdex'],
	install_requires=[])
