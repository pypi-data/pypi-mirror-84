from setuptools import setup,find_packages

classifiers = [
'Development Status :: 5 - Production/Stable',
'Intended Audience :: Education',
'Operating System :: Microsoft :: Windows',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3'
]

setup(
	name='ktgitclone',
	version='0.0.1',
	description='Basic pyGithub operations to clone a public repository and push it to users remote repository',
	Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	url='https://github.com/kristej/pyGithub-git-operations.git',
	author='Krishna Teja',
	author_email='krishnatv104@gmail.com',
	License='MIT',
	classifiers=classifiers,
	keywords=['pygithub','clone'],
	packages=find_packages(),
	install_requires=['git','os','tempfile','fnmatch','argparse','sys','shutil','stat','github','Github','subprocess']

)