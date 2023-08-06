import click
import boto3
import keyring
import base64
import configparser
import os
from warrant.aws_srp import AWSSRP
import botocore
from warrant import Cognito

# Initialize config file dictionary object
config = configparser.ConfigParser()
config.read('config.ini')

# Returns True if Auth successful, False otherwise.
def authenticate_warrant(username: str, password: str):
    client = boto3.client('cognito-idp')
    aws = AWSSRP(
        username=username, 
        password=password, 
        pool_id=config['AWS']['user_pool_id'], 
        client_id=config['AWS']['app_client_id'], 
        client=client
    )
    #u = Cognito(config['AWS']['user_pool_id'], config['AWS']['app_client_id'], username=username)
    try:
        tokens = aws.authenticate_user()
    except:
        return False
        print('Exception!')
    access_token = tokens['AuthenticationResult']['AccessToken']
    refresh_token = tokens['AuthenticationResult']['RefreshToken']
    id_token = tokens['AuthenticationResult']['IdToken']

    # Save tokens to KeyChain
    keyring.set_password('SpikitAPI', "AccessToken", access_token)
    keyring.set_password('SpikitAPI', "RefreshToken", refresh_token)
    keyring.set_password('SpikitAPI', "IdToken", id_token)

    return True

@click.group()
def apis():
    # Refresh tokens if they already exist.
    refresh()
    """Welcome to Spikit. Where we Drop Trou and Get Raw."""
    
# Refreshes existing Cognito tokens.
def refresh():
    # Check if tokens are still valid.
    u = Cognito(
        config['AWS']['user_pool_id'], 
        config['AWS']['app_client_id'],
        id_token=keyring.get_password('SpikitAPI', "IdToken"),
        refresh_token=keyring.get_password('SpikitAPI', "RefreshToken"),
        access_token=keyring.get_password('SpikitAPI', "AccessToken")
    )

    resp = u.check_token()
    if resp:
        # Add new tokens to Keychain.
        click.echo(resp)
    else:
        # Already authorized, pass
        pass

@apis.command()
def login():
    """Authenticate with Spikit -- to run all of your functions."""
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str, hide_input=True)
    if authenticate_warrant(username=username, password=password):
        click.echo("Successfully authenticated with Spikit!")
    else:
        click.echo("Invalid username and password. Login")

@apis.command()
def print():
    """Print the AccessToken for user"""
    click.echo(str(keyring.get_password('SpikitAPI', "SessionToken")))

@apis.command()
@click.option('--dataset', type=str, default=None, help='DatasetID for the dataset that you want to pull')
def pull(dataset):
    """Pull Dataset for User"""
    # print(str(config['AWS']['bucket_name']))
    prefix = os.path.join('datasets', 'exported', str(dataset))

    resource = boto3.resource('s3', 
        aws_access_key_id=keyring.get_password('SpikitAPI', "AccessKeyId"), 
        aws_secret_access_key=keyring.get_password('SpikitAPI', 'SecretKey'),
        aws_session_token=keyring.get_password('SpikitAPI', "SessionToken")
    )
    bucket = resource.Bucket(str(config['AWS']['bucket_name']))

    for obj in bucket.objects.filter(Prefix = prefix):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, 'spikit_dataset') 

if __name__ == '__main__':
    refresh()
    # Refresh Token
    apis(prog_name='spikit')