from setuptools import setup

setup(name='clean_folder_serzhu',
      version='0.0.5',
      description='Sort files in folders',
      url='https://github.com/serzhu/python-core-homework-07',
      author='serzhu',
      author_email='sergej_zhu@ukr.net',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.main:run']}
    )