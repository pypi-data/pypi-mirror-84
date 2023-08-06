from setuptools import setup

setup(
    name = 'BFClust',
    version = '0.1.26.1',
    description = 'Boundary Forest Clustering',
    url = 'https://github.com/dsurujon/BFClust-python',
    author = 'Defne Surujon',
    author_email = 'defnesurujon@gmail.com',
    packages = ['BFClust'],
    scripts = ['scripts/BFC.py', 'scripts/BFCaugment.py'],
    install_requires = ['numpy', 'pandas', 'joblib', 'scikit-learn', 'biopython','threadpoolctl==2.1.0', 'pandas', 'biopython', 'scipy', 'joblib==0.11']
)