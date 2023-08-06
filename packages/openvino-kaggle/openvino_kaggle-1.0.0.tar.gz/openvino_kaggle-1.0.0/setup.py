from setuptools import setup

setup(long_description="""This package provides Intel's OpenVINO Toolkit installation and easy usage in the Kaggle Notebooks.The OpenVINO Toolkit allows edge AI application optimization and deployment on Kaggle using Kaggle Notebooks. It is also possible to choose to download all 5 or individual supported model dependencies directly in the notebook.

Github Link: https://www.github.com/alihussainia/openvino-kaggle

Linkedin Link: https://www.linkedin.com/in/alihussainia
""",
      name='openvino_kaggle',
      version='1.0.0',
      description='OpenVINO toolkit package for Kaggle Notebooks',
      packages=['openvino_kaggle'],
      author = 'Muhammad Ali',
      author_email = 'malirashid1994@gmail.com',
      zip_safe=False)
