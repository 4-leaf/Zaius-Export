import requests
import json

class ZaiusClient():
    def __init__(self, creds):
        self.creds = creds
        self.headers = {'x-api-key': self.creds, 'Content-Type': 'application/json', 'Accept':'application/json'}

    def CreateBackup(self):
        """
        # Generate a backup file on remote S3 server
        """
        objects =  {'objects': ['customers'], 'delimiter': 'comma', 'format':'csv'}
        post = requests.post('https://api.zaius.com/v3/exports', data=objects, headers=self.headers)
        return json.loads(post.text)
    
    def BackupStatus(self, backupID):
        get = requests.get('https://api.zaius.com/v3/exports/{}'.format(backupID), headers=self.headers)
        output = json.loads(get.text)
        #return {'state': output['state'], 'path':output['path']}
        return output

zaius = ZaiusClient(ZAIUS_SECRET_KEY_HERE)
print(zaius.CreateBackup())

class AmazonS3Client():

    def __init__(self, key, secretKey, bucket):
        self.key = key
        self.secretKey = secretKey
        self.bucket = bucket
