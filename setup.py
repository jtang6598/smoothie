import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="smoothie",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={
        "api": "api",
        "database": "database",
        "settings": "settings",
        "website": "website,"
    },
    packages=setuptools.find_packages(where="smoothie"),

    install_requires=[
        "aws-cdk.core==1.125.0",
        "aws-cdk.aws-apigateway==1.125.0",
        "aws_cdk.aws_lambda==1.125.0",
        "aws_cdk.aws_iam==1.125.0",
        "aws_cdk.aws_dynamodb==1.125.0",
        "aws_cdk.aws_s3==1.125.0",
        "python_settings>=0.2.2"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
