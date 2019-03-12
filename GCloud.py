import os
import cloudstorage as gcs
from google.appengine.api import app_identity

class GCloud(object):
    def __init__(self):
        self.tmp_filenames_to_clean_up = []

    def getDefaultStorageBucket(self):
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())

        return bucket_name

    def writeFile(self, fileContent, fileName, fileType='image/jpg'):
        """Create a file.

        The retry_params specified in the open call will override the default
        retry params for this particular file handle.

        Args:
            filename: filename.
        """
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(fileName,
                            'w',
                            content_type=fileType,
                            retry_params=write_retry_params)
        gcs_file.write(fileContent)
        gcs_file.close()
        self.tmp_filenames_to_clean_up.append(fileName)
        return gcs_file

    def getFile(self, fileName):
        self.response.write('Reading the full file contents:\n')

        gcs_file = gcs.open(fileName)
        contents = gcs_file.read()
        gcs_file.close()
        return contents

    def delete_files(self):
        for filename in self.tmp_filenames_to_clean_up:
            try:
                gcs.delete(filename)
            except gcs.NotFoundError:
                pass