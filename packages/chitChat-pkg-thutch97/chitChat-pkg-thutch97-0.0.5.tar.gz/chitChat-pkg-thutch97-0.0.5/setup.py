import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='chitChat-pkg-thutch97',
      version='0.0.5',
      author='Tom Hutchinson',
      author_email='thomas.3.hutchinson@bt.com',
      description='A python chat server package.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires = [
            'Flask==1.1.2',
		'Flask-RESTful==0.3.8',
		'requests==2.24.0',
		'bcrypt==3.2.0'
      ],
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6'
      # package_data={
      #       'chitChat-pkg-thutch97':['users.db']
      # }
     )