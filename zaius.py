import requests
import json
import boto3
from boto3.session import Session
import botocore
import os

class ZaiusClient():
    def __init__(self, creds):
        self.creds = creds
        self.headers = {'x-api-key': self.creds, 'Content-Type': 'application/json', 'Accept':'application/json'}

    def CreateBackup(self):
        """
        # Generate a backup file on remote S3 server
        """
        payload = "{\"objects\": [\"customers\"], \"delimiter\": \"comma\", \"format\":\"csv\"}"
        post = requests.post('https://api.zaius.com/v3/exports', data=payload, headers=self.headers )
        return json.loads(post.text)
    
    def BackupStatus(self, backupID):
        """
        # Get status of backup as a dictionary
        """
        get = requests.get('https://api.zaius.com/v3/exports/{}'.format(backupID), headers=self.headers)
        output = json.loads(get.text)
        return {'state': output['state'], 'path':output['path']}

class AmazonS3Client():

    def __init__(self, accessKey, secretKey, bucket, prefix, path):
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.bucket = bucket
        self.prefix = prefix
        self.path = path
        self.client = self._s3_client()
    
    def _s3_client(self):
        """
        #Internal function for S3 Client to use specified credentials.
        """
        client = boto3.client('s3', 
                      aws_access_key_id=self.accessKey, 
                      aws_secret_access_key=self.secretKey,)
        return client
    
    def make_directory(self):
        """
        # Make the local directory where files will be placed 
        """
        try:
            os.mkdir(self.path)
        except OSError:
            print("{} already exist".format(self.path))
        else:
            print("Created {}".format(self.path))

    def list_files(self):
        """
        # List files in the specified bucket with prefix
        """
        s3_client = self.client
        file_list = []
        response = s3_client.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix, Delimiter='/')
        for object in response['Contents']:
         if object['Key'].startswith(self.prefix):
             file_list.append(object['Key'])
        return file_list


    def download_files(self, file_list):
        """
        # Download files to the local directory
        # Takes local function list_files as a variable
        """
        s3_client = self.client
        for file in file_list:
            output = "{}/{}".format(self.path, file.replace(self.prefix, ''))
            with open(output, 'wb') as data:
                s3_client.download_fileobj(self.bucket, file, data)
                


amazon = AmazonS3Client('Access_KEY', 'Secret_KEY', 'Zaius_Bucket', 'SUB_DIRECTORY', "LOCAL_DIRECTORY")
amazon.make_directory()
files = amazon.list_files()
amazon.download_files(files)
