from setuptools import setup 
#python setup.py sdist upload -r pypi

# reading long description from file 
with open('sentianalyse/DESCRIPTION.rst') as file: 
	long_description = file.read() 


# specify requirements of your package here 
REQUIREMENTS = ['pandas','matplotlib','textblob'] 

# some more details 
CLASSIFIERS = [ 
	'Development Status :: 3 - Alpha', 
	'Intended Audience :: Developers', 
	'Topic :: Internet', 
	'License :: OSI Approved :: MIT License', 
	'Programming Language :: Python', 
	'Programming Language :: Python :: 2', 
	'Programming Language :: Python :: 2.6', 
	'Programming Language :: Python :: 2.7', 
	'Programming Language :: Python :: 3', 
	'Programming Language :: Python :: 3.3', 
	'Programming Language :: Python :: 3.4', 
	'Programming Language :: Python :: 3.5'
	] 

# calling the setup function 
setup(name='sentianalyse', 
	version='0.0.1', 
	description='A small tool for sentiment analysis of texts.', 
	long_description=long_description,
	url='https://github.com/garain/sentianalyse', 
	author='Avishek Garain', 
	author_email='avishekgarain@gmail.com', 
	license='MIT', 
	packages=['sentianalyse'],
	package_data={'sentianalyse': ['DESCRIPTION.rst']},
	classifiers=CLASSIFIERS, 
	install_requires=REQUIREMENTS, 
	keywords='sentiment polarity emotion texts'
	) 
