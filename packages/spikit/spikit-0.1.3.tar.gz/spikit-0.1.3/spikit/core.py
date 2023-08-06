from torch.utils.data import IterableDataset
import zarr
import s3fs
import os
import configparser
import keyring
from botocore.credentials import RefreshableCredentials, CredentialProvider, DeferredRefreshableCredentials
from botocore.session import get_session

from boto3 import Session
# Subclass IterableDataset PyTorch class -- to load straight into DataLoader
# -> Essentially tells Pytorch how to load the data.
class SpikitDataset(IterableDataset):
    def __init__(self, dataset_id, start=None, end=None):
        super(SpikitDataset, self).__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')
        # Path to Zarr group in S3.
        s3_path = os.path.join('s3://'+config['AWS']['bucket_name'], 'datasets', 'exported', dataset_id)
        print(s3_path)
        # Initialize S3FS File System -- with authenticated credentials
        s3 = s3fs.S3FileSystem(
            key=keyring.get_password('SpikitAPI', "AccessKeyId"), 
            secret=keyring.get_password('SpikitAPI', "SecretKey"),
            token=keyring.get_password('SpikitAPI', "SessionToken")
        )
        store = s3fs.S3Map(root=s3_path, s3=s3, check=False)
        # Point Zarr to Exported composite dataset stored in S3.
        root = zarr.group(store=store)
        self.array = root['dataset/']
        if start is None:
            start = 0
        if end is None:
            end = self.array.shape[0]
        assert end > start
        self.start = start
        self.end = end
    def __iter__(self):
        return islice(self.array, self.start, self.end)
    
def islice(arr, start=None, end=None):
    if len(arr.shape) == 0:
        # Same error as numpy
        raise TypeError("iteration over a 0-d array")
    if start is None:
        start = 0
    if end is None:
        end = arr.shape[0]
    # Avoid repeatedly decompressing chunks by iterating over the chunks
    # in the first dimension.
    chunk_size = arr.chunks[0]
    chunk = None
    for j in range(start, end):
        if j % chunk_size == 0:
            chunk = arr[j: j + chunk_size]
        # init chunk if we start offset of chunk borders
        elif chunk is None:
            chunk_start = j - j % chunk_size
            chunk_end = chunk_start + chunk_size
            chunk = arr[chunk_start:chunk_end]
        yield chunk[j % chunk_size]

# class AWSAuthorizer():
#     def make_session(self):
#         session = get_session()
#         cred_provider = session.get_component('credential_provider')

#         cred_provider.insert_before('env', CustomCredentialProvider())

#         boto3_session = Session(botocore_session=session)

# class CustomCredentialProvider(CredentialProvider):
#     def load(self):
#         # These creds will be automatically refreshed using the _refresh method if the current creds
#         # are going to expire in 15 minutes or less.
#         creds = DeferredRefreshableCredentials(refresh_using=self._refresh, method="sts-assume-role",)
#         return creds
#     def _refresh(self):
#         # Refresh your AWS creds using custom process
#         response=self._custom_aws_cred_refresh()

#     def _custom_aws_cred_refresh(self):

#         # Your custom AWS cred refresh code
#         return response