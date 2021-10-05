# smoothie

## Setup

### Prerequisites
- Create a personal AWS account
- Create an IAM user with [programmatic access](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) and administrator permissions.
     1. Click "Add User" in the IAM user console
     2. Name your user and check "Access key - Programmatic access" under "Select AWS access type"
     3. Click "Attach existing policies directly" and search and select "AdministratorAccess"
     4. Skip Tags and download the user's access key and secret access key
- [Install AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Install AWS CDK Toolkit](https://docs.aws.amazon.com/cdk/latest/guide/work-with.html#work-with-prerequisites)
- Configure AWS CDK to use your administrator IAM user's credentials
    1. Run
    ```
    aws configure
    ```
    2. Enter your IAM user's access key and secret access key when prompted

### Setup Project

After the prerequisites are completed, you can use the following command to activate your virtualenv.

For Mac

```
$ source .venv/bin/activate
```

For Windows

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```
