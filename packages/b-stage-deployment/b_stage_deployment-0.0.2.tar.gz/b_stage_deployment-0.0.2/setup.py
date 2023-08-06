from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_stage_deployment',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'b_stage_deployment_test'
    ]),
    description=(
        'AWS CDK resource that creates a stage deployment. Original one '
        'has too many bugs.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'aws-cdk.core>=1.54.0,<2.0.0',
        'aws-cdk.aws-apigatewayv2>=1.54.0,<2.0.0',
        'aws-cdk.aws-lambda>=1.54.0,<2.0.0',
        'boto3>=1.10.46,<1.16.0',
        'pytest>=6.0.2,<7.0.0',
        'b-aws-testing-framework>=0.0.13,<1.0.0'
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@biomapas.com',
    keywords='AWS API Gateway Stage Deployment',
    url='https://github.com/biomapas/B.StageDeployment.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
