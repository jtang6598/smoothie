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

After the prerequisites are completed, create a virtual environment using your favorite method. If you're on Mac or Linux and would like to run the demo notebook, you can expedite things by adding these two lines to `venv/bin/activate`, filling in your respective Spotify application client ID and secret (developer.spotify.com):

```
export SPOTIFY_CLIENT_ID=<SPOTIFY_CLIENT_ID>
export SPOTIFY_CLIENT_SECRET=<SPOTIFY_CLIENT_SECRET>
```

You can use the following command to activate your virtualenv.

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

### Deploy Stack

To deploy the stack to your personal account, run

```
$ cdk bootstrap aws://<AWS account id>/<region>
```

This command only needs to be run once. To deploy the actual stack, run

```
$ cdk synth && cdk deploy SmoothieStack
```
