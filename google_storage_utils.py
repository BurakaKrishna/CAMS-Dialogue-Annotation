# Imports the Google Cloud client library
import traceback

from google.cloud import storage
from google.cloud.storage import Blob
import json

# Instantiates a client
class GoogleStorage:

    def __init__(self, user_data_path, run_locally):

        # Set the default bucket name
        self.bucket_name = "ca-dialouge-tagger.appspot.com"

        # Set the storage path on the bucket
        self.user_data_path = user_data_path

        # If running locally need to authenticate
        if run_locally:
            self.storage_client = storage.Client.from_service_account_json('C:/Users/Nate/CA-Dialouge-Tagger-90a92d6b6650.json')
        else:
            self.storage_client = storage.Client(project='ca-dialogue-tagger')

    def get_user_file_list(self, bucket_name):

        # Get the bucket
        bucket = self.storage_client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs())
        file_list = [file.name.split(self.user_data_path) for file in blobs if self.user_data_path in file.name]
        print(file_list)
        file_list = [name[1] for name in file_list]
        print(file_list)
        return file_list

    def user_file_exists(self, user_filename):

        # Get a list of all the files in the bucket
        user_file_list = self.get_user_file_list(self.bucket_name)

        if user_filename in user_file_list:
            return True
        else:
            return False

    def load_json_data(self, path, file_name):
        try:
            # Get the bucket
            bucket = self.storage_client.get_bucket(self.bucket_name)
            # Get the blob (file)
            blob = Blob(path + file_name + ".json", bucket)

            json_in_bytes = blob.download_as_string(self.storage_client)

            json_data = json_in_bytes.decode('utf8')
        except (IOError, ValueError):
            traceback.print_exc()
            return False

        return json.loads(json_data)

    def save_json_data(self, path, file_name, data):
        try:
            # Get the bucket
            bucket = self.storage_client.get_bucket(self.bucket_name)
            # Get the blob (file)
            blob = Blob(path + file_name + ".json", bucket)

            blob.upload_from_string(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        except (IOError, ValueError):
            traceback.print_exc()
            return False

        return True

    def save_users(self, data):
        try:
            # Get the bucket
            bucket = self.storage_client.get_bucket(self.bucket_name)
            # Get the blob (file)
            blob = Blob("users.json", bucket)

            blob.upload_from_string(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        except (IOError, ValueError):
            traceback.print_exc()
            return False

        return True

    def load_users(self):
        try:
            # Get the bucket
            bucket = self.storage_client.get_bucket(self.bucket_name)
            # Get the blob (file)
            blob = Blob("users.json", bucket)

            json_in_bytes = blob.download_as_string(self.storage_client)

            json_data = json_in_bytes.decode('utf8')
        except (IOError, ValueError):
            traceback.print_exc()
            return False

        return json.loads(json_data)
