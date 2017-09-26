
'''
WANT: in directory, just run this script
it'll zip + deploy
'''

import boto3
import os
import subprocess
import zipfile
lambdaClient = boto3.client('lambda')

ZIP_TEMP_FILE = 'lambda.zip'

def uploadDirToAwsLambda():
    lambdaFunctionName = getLambdaFunctionName()
    assertValidLambdaFunctionName(lambdaFunctionName)
    print('Lambda function:', lambdaFunctionName)
    saveZip()
    uploadZipToAws(lambdaFunctionName)

def getLambdaFunctionName():
    cwd = os.getcwd()
    dirName = os.path.split(cwd)[1]
    return dirName

def assertValidLambdaFunctionName(lambdaFunctionName):
    response = lambdaClient.get_function(
        FunctionName=lambdaFunctionName,
    )

def saveZip():
    # Note - zip creation doesn't update anything removed
    if os.path.isfile(ZIP_TEMP_FILE): 
        os.remove(ZIP_TEMP_FILE)
    subprocess.run(['zip', '-r', ZIP_TEMP_FILE, '.'])

    #fileNames = ['lambda_function.py']
    #with zipfile.ZipFile(source, 'w') as zipped:
    #    for fileName in fileNames:
    #        zipped.write(fileName)

def uploadZipToAws(lambdaFunctionName):
    zipFileAsByte = open(ZIP_TEMP_FILE, 'rb').read()
    response = lambdaClient.update_function_code(
        FunctionName=lambdaFunctionName,
        ZipFile=zipFileAsByte
    )


def main():
    uploadDirToAwsLambda()

main()

