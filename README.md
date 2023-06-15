# Blob mapping utility

When your code needs to access many mapped blobs as a mounted folder, the utility to make translation between blob urls and filepaths easier was made.
It can be configured using the configuration json file.

Configuration file example:

``` json
{
  "blob_mounting_configurations": [
    {
      "storage_account_name": "oseoinfrastagingstrgacc",
      "storage_account_url": "https://oseoinfrastagingstrgacc.blob.core.windows.net/",
      "container_name": "heightstore-dsm1m-raw",
      "mount_point": "/mnt/heightstore-dsm1m-raw"
    },
    {
      "storage_account_name": "oseoinfrastagingstrgacc",
      "storage_account_url": "https://oseoinfrastagingstrgacc.blob.core.windows.net/",
      "container_name": "heightstore-dsm25cm-raw",
      "mount_point": "/mnt/heightstore-dsm25cm-raw"
    },
    {
      "storage_account_name": "oseoinfrastagingstrgacc",
      "storage_account_url": "https://oseoinfrastagingstrgacc.blob.core.windows.net/",
      "container_name": "heightstore-dtm1m-raw",
      "mount_point": "/mnt/heightstore-dtm1m-raw"
    },
    {
      "storage_account_name": "oseoinfrastagingstrgacc",
      "storage_account_url": "https://oseoinfrastagingstrgacc.blob.core.windows.net/",
      "container_name": "rss-rgbi25cm16bittiff-raw",
      "mount_point": "/mnt/rss-rgbi25cm16bittiff-raw"
    }
  ]
}
```