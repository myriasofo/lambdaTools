
### IMPORT LIBRARIES
import base64
import importlib
import os
import subprocess
import sys 
import zipfile

# Import libs from virtual environment (.venv)
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(SCRIPT_DIR + '/.venv/lib/python3.6/site-packages')
import boto3
import yaml
lambdaClient = boto3.client('lambda')


### CONSTANTS
CONFIG_FILE_NAME = 'lambdat.yml'
ZIP_TEMP_FILE = 'lambda.zip'

### FOR RUNNING VIA BASH
def run():
    if len(sys.argv) == 2:
        runLambdat(sys.argv[1], None)
    elif len(sys.argv) == 3:
        runLambdat(sys.argv[1], sys.argv[2])
    else:
        raise Exception('Invalid number of args:', len(sys.argv))

def runLambdat(command, lambdaFunctionName):
    lambdaFunctionName = getLambdaFunctionName(lambdaFunctionName)

    if (command == 'invoke'):
        invokeLambda(lambdaFunctionName)
    elif (command == 'deploy'):
        deployLambda(lambdaFunctionName)
    else:
        raise Exception('Invalid command:', command)


### MAIN FUNCTIONS
def invokeLambda(lambdaFunctionName):
    response = lambdaClient.invoke(
        FunctionName=lambdaFunctionName,
        InvocationType='RequestResponse',
        LogType='Tail'
    )

    printLog(response)

def deployLambda(lambdaFunctionName):
    saveZip(ZIP_TEMP_FILE)
    uploadZipToAws(lambdaFunctionName, ZIP_TEMP_FILE)


### HELPERS
def getLambdaFunctionName(lambdaFunctionName):
    if lambdaFunctionName == None:
        lambdaFunctionName = guessLambdaFuntionName()
    assertValidLambdaFunctionName(lambdaFunctionName)
    print('Lambda function:', lambdaFunctionName)
    return lambdaFunctionName

def guessLambdaFuntionName():
    if os.path.isfile(CONFIG_FILE_NAME):
        lambdatFile = open(CONFIG_FILE_NAME, 'r')
        lambdatConfig = yaml.load(lambdatFile)
        lambdaFunctionName = lambdatConfig['lambdaFunctionName']
        return lambdaFunctionName
    else:
        cwd = os.getcwd()
        dirName = os.path.split(cwd)[1]
        return dirName

def assertValidLambdaFunctionName(lambdaFunctionName):
    response = lambdaClient.get_function(
        FunctionName=lambdaFunctionName,
    )

def printLog(response):
    rawLog = response['LogResult']
    log = base64.b64decode(rawLog).decode('utf-8')
    print(log)

def saveZip(zipFile):
    # Note - zip creation doesn't update anything removed
    if os.path.isfile(zipFile): 
        os.remove(zipFile)
    subprocess.run(['zip', '-r', zipFile, '.'])

    #fileNames = ['lambda_function.py']
    #with zipfile.ZipFile(source, 'w') as zipped:
    #    for fileName in fileNames:
    #        zipped.write(fileName)

def uploadZipToAws(lambdaFunctionName, zipFile):
    zipFileAsByte = open(zipFile, 'rb').read()
    response = lambdaClient.update_function_code(
        FunctionName=lambdaFunctionName,
        ZipFile=zipFileAsByte
    )


if __name__ == "__main__":
    run()

