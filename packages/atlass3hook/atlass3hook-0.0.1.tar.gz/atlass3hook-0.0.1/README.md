# Apache Atlas S3 hook in Python

This python client uses a s3 client package s3fs to get the metadata of s3 entities such as Bucket, pseudo_dir and 
object, then it inserts these metadata into Atlas instances.


## Quick start

### Create a client to connect to an Atlas instance
```python
from atlas_client.client import Atlas
# login with your token
hostname = "https://atlas.lab.sspcloud.fr"
port = 443
oidc_token = "<your_token>"
atlas_client = Atlas(hostname, port, oidc_token=oidc_token)

# login with your username and password
atlas_client = Atlas(hostname, port, username='',password='')
```
### Create a s3 metadata client to collect metadata of s3 entities
```python
from atlas_s3_hook.S3MetadataClient import S3MetadataClient

s3_end_point = ''
s3_access_key = ''
s3_secret_key = ''
s3_token = ''

s3_client = S3MetadataClient(s3_end_point, s3_access_key, s3_secret_key, s3_token)


```

### Load a single s3 entity into atlas 
If you want to load the metadata of a single s3 entity, you can use the following code example
```python
from atlas_s3_hook.S3Hook import S3Hook

# Indicate the path of the entity which you want to 
path=''
description=''
s3_hook = S3Hook(s3_client, atlas_client)
# Get the class of the s3 entity
path_class = s3_client.get_class_from_path(path)
print(path_class)

# Get the metadata of the s3 entity
meta_data = s3_client.get_path_meta_data(path)

# based on the class of the s3 entity, s3 hook provides different loaders. You need to choose the correct one

# bucket loader 
s3_hook.create_atlas_bucket(meta_data,description)

# directory loader
s3_hook.create_atlas_ps_dir(meta_data,description)

# object loader
s3_hook.create_atlas_object(meta_data,description)


``` 


### Load multiple s3 entities into atlas 
If you want to load the metadata of multiple s3 entities, you can use the following code example. The S3Scanner class 
takes a path of s3 entity and load all the metadata of its contents (e.g. sub-directory, objects). 

```python
from atlas_s3_hook.S3Scanner import S3Scanner

s3_entity_path=''
entity_owner=''

minio_scanner = S3Scanner(minio_client, atlas_client, owner=entity_owner)
minio_scanner.scan_path(s3_entity_path)

```

## Prerequisites

This tool only requires python 3.7 or above

## Supported OS

Windows XP/7/8/10

Linux  

MacOS


## Authors

* **Pengfei Liu** 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgement

This package was created by using [s3fs](<https://pypi.org/project/s3fs/>) project