from cloud.authenticate import list_scopes, Authenticate
from cloud.S3 import S3

def get_access_token():
    scope = list_scopes()
    auth = Authenticate(scope)
    client = auth.get_spotipy_client()

    results = client.current_user_saved_tracks()
    # need to call one of the functions in order to save the cache file
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " - ", track['name'])

def upload_to_s3(bucket_name, filename, key, region, create_bucket=False):
    s3_client = S3(region)
    if create_bucket == True:
        s3_client.create_bucket(bucket_name)
    else: 
        s3_client.upload_to_bucket(bucket_name, filename, key)

def main():
    get_access_token()
    upload_to_s3('token-bucket', '.cache', '.cache', 'us-east-2')

if __name__ == '__main__':
    main()