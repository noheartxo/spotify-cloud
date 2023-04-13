
### **Purpose**
Utilize the Python Spotify Web API wrapper, [Spotipy](https://github.com/spotipy-dev/spotipy) to create playlists containing previously played songs and integrate automation through an AWS cloud environment.

### **Prerequisites**
Install required packages 
``` 
pip install spotipy
pip install pymysql
pip install boto3
pip install argparse
```

Configure AWS credentials file with [AWS CLI](https://aws.amazon.com/cli/)
```
aws configure
```

Configure envrionment variables for Spotipy to access Spotify [development application](https://developer.spotify.com/documentation/web-api/concepts/apps)
```
SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI
```

### **cloud/main.py**
Allows for retreiving initial access token from Spotify and can upload the file to an S3 bucket or download any file from the S3 bucket in a CLI format

```
usage: main.py [-h] [-a {request}] [-b BUCKET_NAME] [-f FILENAME] [-k KEY] [-r REGION] [-u UPLOAD] [-d DOWNLOAD]

Create initial access token from Spotify and upload/download to or from S3 bucket

options:
  -h, --help            show this help message and exit
  -a {request}, --access-token {request}
                        Request for an access token from Spotify
  -b BUCKET_NAME, --bucket_name BUCKET_NAME
                        S3 Bucket Name
  -f FILENAME, --filename FILENAME
                        File containing access token
  -k KEY, --key KEY     Filename given when uploading to the bucket
  -r REGION, --region REGION
                        Region where the S3 bucket is located
  -u UPLOAD, --upload UPLOAD
                        Upload file to S3 bucket
  -d DOWNLOAD, --download DOWNLOAD
                        Download file from S3 bucket
```