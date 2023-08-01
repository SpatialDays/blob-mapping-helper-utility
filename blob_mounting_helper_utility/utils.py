import os.path
import logging
logger = logging.getLogger(__name__)
from typing import Tuple, List
from urllib.parse import urlparse, urljoin
from azure.storage.blob import BlobClient


class BlobMappingUtility:
    downloaded_paths = []
    uploaded_paths = []

    def __init__(self, blob_mounting_configurations_list: List, azure_storage_account_key: str = None):
        if blob_mounting_configurations_list is None:
            raise ValueError("blob_mounting_configurations_list cannot be None")

        for config in blob_mounting_configurations_list:
            if not all(key in config for key in
                       ("storage_account_url", "container_name", "storage_account_name", "mount_point")):
                raise ValueError(f"Invalid blob_mounting_configurations_list: {blob_mounting_configurations_list}")

        self.blob_mounting_configurations_list = blob_mounting_configurations_list
        self.azure_storage_account_key = azure_storage_account_key

    @staticmethod
    def _get_details_from_blob_url(url: str) -> Tuple[str, str, str]:
        parsed_url = urlparse(url)
        path = parsed_url.path[1:]  # Remove leading slash

        container_name, _, blob_name = path.partition('/')
        account_name = parsed_url.netloc.split('.')[0]

        if not container_name or not blob_name or not account_name:
            raise ValueError(f"Invalid blob URL: {url}")

        return account_name, container_name, blob_name

    def get_container_name_from_mount_point(self, mount_point: str) -> str:
        for config in self.blob_mounting_configurations_list:
            if config["mount_point"] == mount_point:
                return config["container_name"]
        raise ValueError(f"Mount point {mount_point} is not a part of any mounted folder")

    def get_mount_point_from_container_name(self, container_name: str) -> str:
        for config in self.blob_mounting_configurations_list:
            if config["container_name"] == container_name:
                return config["mount_point"]

        raise ValueError(f"Container name {container_name} is not a part of any mounted folder")

    def get_mounted_folder_details_from_url(self, url: str) -> Tuple[str, str]:
        storage_account_name, container_name, blob_name = self._get_details_from_blob_url(url)

        for config in self.blob_mounting_configurations_list:
            if config["storage_account_name"] == storage_account_name and config["container_name"] == container_name:
                return config["mount_point"], blob_name

        raise ValueError(f"Blob URL {url} is not a part of any mounted folder")

    def get_mount_point_from_url(self, url: str) -> str:
        mount_point, _ = self.get_mounted_folder_details_from_url(url)
        return mount_point

    def get_mounted_filepath_from_url(self, url: str) -> str:
        mount_point, blob_name = self.get_mounted_folder_details_from_url(url)
        return os.path.join(mount_point, blob_name)

    def get_url_from_mounted_filepath(self, file_path: str) -> str:
        if not file_path:
            raise ValueError(f"Invalid file path: {file_path}")
        folder, file = os.path.split(file_path)
        return self.get_url_from_mounted_folder_and_filename(folder, file)

    def get_url_from_mounted_folder_and_filename(self, folder_path: str, filename: str) -> str:
        if not folder_path or not filename:
            raise ValueError(f"Invalid folder path or filename: {folder_path}, {filename}")

        # Sort the configurations by the length of the mount_point in descending order
        sorted_configurations = sorted(self.blob_mounting_configurations_list,
                                       key=lambda config: -len(config["mount_point"]))

        for config in sorted_configurations:
            # Check if the folder_path starts with the mount_point
            if folder_path.startswith(config["mount_point"]):
                # Remove the mount point from the folder path to get the subdirectory path
                subdirectory_path = folder_path.replace(config["mount_point"], "").lstrip("/")
                # Append subdirectory path and filename to the url
                url = urljoin(config['storage_account_url'], config['container_name'])
                url = urljoin(url + '/', subdirectory_path)
                url = urljoin(url + '/', filename)
                return url

        raise ValueError(f"Folder path {folder_path} is not a mounted folder")

    def download_blob(self, url: str) -> None:
        logger.debug(f"Downloading blob from {url}")
        blob_client = BlobClient.from_blob_url(url, credential=self.azure_storage_account_key)
        download_file_path = self.get_mounted_filepath_from_url(url)
        if not os.path.exists(download_file_path):
            os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            logger.debug(f"Downloaded blob to {download_file_path}")
            self.downloaded_paths.append(download_file_path)
        else:
            logger.debug(f"Blob already downloaded to {download_file_path}")

    def upload_blob(self, file_path: str) -> None:
        logger.debug(f"Uploading blob from {file_path}")
        blob_client = BlobClient.from_blob_url(self.get_url_from_mounted_filepath(file_path),
                                               credential=self.azure_storage_account_key)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        if file_path not in self.uploaded_paths:
            self.uploaded_paths.append(file_path)
        logger.debug(f"Uploaded blob from {file_path}")

    def cleanup_files(self) -> None:
        logger.debug("Cleaning up files")
        for file_path in self.downloaded_paths:
            logger.debug(f"Removing downloaded file {file_path}")
            os.remove(file_path)
            # remove the directory if it is empty
            try:
                os.rmdir(os.path.dirname(file_path))
            except OSError:
                pass
        for file_path in self.uploaded_paths:
            logger.debug(f"Removing uploaded file {file_path}")
            os.remove(file_path)
            # remove the directory if it is empty
            try:
                os.rmdir(os.path.dirname(file_path))
            except OSError:
                pass
        self.downloaded_paths = []
        self.uploaded_paths = []
        logger.debug("Cleaned up files")
