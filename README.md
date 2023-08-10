# Blob mapping utility

When your code needs to access many mapped blobs as a mounted folder, the utility to make translation between blob urls and filepaths easier was made.
It can be configured using the configuration json file.

You can also use this utility to download and uploads the blobs to/from the local file system without having to worry about the filepaths.

Configuration file example:

``` json
{
  "blob_mounting_configurations": [
    {
      "storage_account_name": "examplestagingstrgacc",
      "storage_account_url": "https://examplestagingstrgacc.blob.core.windows.net/",
      "container_name": "example-container-raw",
      "mount_point": "/mnt/example-container-raw"
    }
  ]
}
```

## How to use

```python
from blob_mounting_helper_utility import BlobMappingUtility
json_config_file = "blob_mapping_config.json"

# read the file into a dictionary
with open(json_config_file) as json_file:
    config = json.load(json_file)["blob_mounting_configurations"]

# create the utility object
blob_mapping_utility = BlobMappingUtility(config)

filepath1 = "/mnt/example-container-raw/cool_picture.png
blob_url = blob_mapping_utility.get_url_from_mounted_filepath(filepath1) # -> https://examplestagingstrgacc.blob.core.windows.net/example-container-raw/cool_picture.png

filepath2 = get_mounted_filepath_from_url(blob_url) # -> /mnt/example-container-raw/cool_picture.png
```

Also, if you were to pass the azure storage account key you can download and upload the blob to a local file path:

```python
from blob_mounting_helper_utility import BlobMappingUtility
json_config_file = "blob_mapping_config.json"

# read the file into a dictionary
with open(json_config_file) as json_file:
    config = json.load(json_file)["blob_mounting_configurations"]

azure_storage_account_key = "example_key"
# create the utility object
blob_mapping_utility = BlobMappingUtility(config, azure_storage_account_key)
url = "https://examplestagingstrgacc.blob.core.windows.net/example-container-raw/cool_picture.png"
blob_mapping_utility.download_blob(url) # -> Downloads the blob to the local file path "/mnt/example-container-raw/cool_picture.png"
local_filepath = "/mnt/example-container-raw/cool_picture.png"
do_something_to_file(local_filepath)
blob_mapping_utility.upload_blob(local_filepath) # -> Uploads the file to the blob url
blob_mapping_utility.cleanup_files() # cleans both downloaded and uploaded files from the local file system

```
