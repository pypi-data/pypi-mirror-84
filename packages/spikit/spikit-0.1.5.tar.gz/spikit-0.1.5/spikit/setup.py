from setuptools import setup, find_packages

setup(
    name='spikit',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'boto3',
        'keyring',
        'warrant',
        's3fs',
        'zarr',
        'torch'
    ],
    entry_points='''
        [console_scripts]
        spikit=main:apis
    ''',
)