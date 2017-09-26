## Why use this?
To quickly deploy or invoke functions in AWS Lambda


## To use
To invoke a Lambda function, run this in the terminal:
```
lambdat invoke myFunctionName
```

You can skip the function name if you're in the code's directory, or have a `lambdat.yml` (explained below):
```
lambdat invoke
```

To deploy:
```
lambdat invoke
```

## To install
0. Make sure you have python 3.6 installed

1. Clone this repo:
    ```
    git clone git@github.com:myriasofo/lambdaTools
    ```
2. Install python modules
    * Option 1: Installing globally:
      ```
      pip3 install -r requirements.txt
      ```
    * Option 2: Installing in a virtual environment:
      ```
      python3 -m venv .venv
      source .venv/bin/activate
      pip3 install -r requirements.txt
      ```
    
3. Create an alias for bash. In your `~/.bash_profile`, add this:
    ```
    alias lambdat='python3 ~/path/to/lambdat/__init__.py
    ```
    
4. Make sure to you've set up AWS creds. (For help, see: http://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html. Additionally, make your user has permission to access Lambda programmatically.)

## Advanced usage
You can add a `lambda.yml` to to the directory of your lambda code. An example is provided in the repo. All you need is this line:
```
lambdaFunctionName: myFunctionName
```
