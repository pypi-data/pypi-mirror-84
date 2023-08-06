from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="eda-fe-model",
    version="0.3.0",
    description="A python package to handle EDA and feature extraction and also return the best hyperparameters for a tabular classification problem.",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=find_packages(),
    author=["Akshat Mehrotra", "Mohammad Shaheer Khan"],
    author_email="akshat117@gmail.com",
    keywords = ['EDA', 'Feature_selection', 'Model_hyper_parametrs'],
    url="https://github.com/Akkimehr/eda-fe-model",
    include_package_data=True
)

install_requires=[
        "numpy>=1.18.5",
        "pandas>=1.0.5",
        "scikit-learn>=0.23.1",
        "statsmodels>=0.11.1",
        "tensorflow>=2.1.0"
]

if __name__=='__main__':
    setup(**setup_args, install_requires=install_requires)