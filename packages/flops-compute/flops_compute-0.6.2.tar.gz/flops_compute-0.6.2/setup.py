from setuptools import find_packages, setup

readme = open('README.md').read()

VERSION = '0.6.2'

requirements = [
    'torch',
]

setup(
    # Metadata
    name='flops_compute',
    version=VERSION,
    author='junxi',
    author_email='843525908@qq.com',
    # url='https://github.com/sovrasov/flops-counter.pytorch',
    description='Flops counter for convolutional networks in'
                'pytorch framework',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',

    # Package info
    packages=find_packages(exclude=('*test*',)),

    #
    zip_safe=True,
    install_requires=requirements,

    # Classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
