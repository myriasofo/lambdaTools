
'''
WANT: in directory, just run this script
it'll invoke the lambda function
'''

import base64
import boto3
import os
lambdaClient = boto3.client('lambda')


def invokeLambda(lambdaFunctionName=None):
    if lambdaFunctionName == None:
        lambdaFunctionName = guessLambdaFuntionName()

    response = lambdaClient.invoke(
        FunctionName=lambdaFunctionName,
        InvocationType='RequestResponse',
        LogType='Tail'
    )

    printLog(response)

def guessLambdaFuntionName():
    cwd = os.getcwd()
    dirName = os.path.split(cwd)[1]
    return dirName

def printLog(response):
    rawLog = response['LogResult']
    log = base64.b64decode(rawLog).decode('utf-8')
    print(log)


def main():
    invokeLambda()

main()

