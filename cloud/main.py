from S3 import S3
import argparse
from authenticate import Authenticate
from authenticate import list_scopes

def create_access_token():
    scope = list_scopes()
    auth = Authenticate(scope)
    client = auth.get_spotipy_client()

    results = client.current_user_saved_tracks(limit=2)
    # need to call one of the functions in order to save the cache file
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " - ", track['name'])

def upload_to_s3(bucket_name, filename, key, region, create_bucket=False):
    s3_client = S3(region)
    if create_bucket == True:
        s3_client.create_bucket(bucket_name)
    s3_client.upload_object_to_bucket(bucket_name, filename, key)

def download_from_s3(bucket_name, file, region):
    s3_client = S3(region)
    response = s3_client.get_object_from_bucket(bucket_name, file)
    decoded = str(response.decode('utf-8'))
    return decoded

def main():
    parser = argparse.ArgumentParser(description="Create initial access token from Spotify \
                                     and upload/download to or from S3 bucket")
    parser.add_argument("-a", "--access-token", required=False, choices=['request'], nargs=1, 
                        help="Request for an access token from Spotify")
    parser.add_argument("-b", "--bucket_name", type=str, nargs=1, required=False, help="S3 Bucket Name")
    parser.add_argument("-f", "--filename", type=str, required=False, help="File containing access token")
    parser.add_argument("-k", "--key", type=str, nargs=1, required=False, 
                        help="Filename given when uploading to the bucket")
    parser.add_argument("-r", "--region", type=str, nargs=1, required=False,
                         help="Region where the S3 bucket is located")
    parser.add_argument("-u", "--upload", required=False, help="Upload file to S3 bucket")
    parser.add_argument("-d", "--download", required=False, help="Download file from S3 bucket")
    args = parser.parse_args()
    
    if args.access_token != None and args.upload == None:
        create_access_token()
    elif args.upload != None:
        if args.access_token != None:
            create_access_token()
        with open(args.filename) as access_file:
            content = str(access_file.read())
        upload_to_s3(args.bucket_name[0], args.key[0], content, args.region[0])
    elif args.download != None:
        download_from_s3(args.bucket_name[0], args.key[0], args.region[0])

if __name__ == '__main__':
    main()