import os
import sys
from unittest import TestCase

# get the current file path
# current_path = os.path.dirname(os.path.abspath(__file__))
# src_path = os.path.normpath(os.path.abspath(os.path.join(current_path, os.pardir, "src")))
# sys.path.insert(0, src_path)
from blob_mounting_helper_utility import BlobMappingUtility


class TestGetBlobFolderAndFileNameFromBlobUrl(TestCase):
    def test_blob_url_with_mount_point(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/blob.txt"
        expected_result = ("/mnt/container", "blob.txt")
        assert blob_util.get_mounted_folder_details_from_url(url) == expected_result

    def test_blob_url_with_multiple_mount_points(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            },
            {
                "storage_account_name": "another_example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "another_container",
                "mount_point": "/mnt/another_container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/blob.txt"
        expected_result = ("/mnt/container", "blob.txt")
        assert blob_util.get_mounted_folder_details_from_url(url) == expected_result

    def test_blob_url_with_no_matching_mount_point(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "another_example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "another_container",
                "mount_point": "/mnt/another_container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/blob.txt"
        self.assertRaises(ValueError, blob_util.get_mounted_folder_details_from_url, url)

    def test_blob_url_with_no_mount_points_defined(self):
        blob_util = BlobMappingUtility([])
        url = "https://example.blob.core.windows.net/container/blob.txt"
        expected_result = (False, "", "")
        self.assertRaises(ValueError, blob_util.get_mounted_folder_details_from_url, url)

    def test_blob_url_with_different_case_mount_point(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/MNT/CONTAINER"  # uppercase folder are valid in linux
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/blob.txt"
        expected_result = ("/MNT/CONTAINER", "blob.txt")
        assert blob_util.get_mounted_folder_details_from_url(url) == expected_result

    def test_blob_url_with_subdirectory(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/subfolder/blob.txt"
        expected_result = ("/mnt/container", "subfolder/blob.txt")
        assert blob_util.get_mounted_folder_details_from_url(url) == expected_result

    def test_blob_url_with_special_characters(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/folder with spaces/blob@123.txt"
        expected_result = ("/mnt/container", "folder with spaces/blob@123.txt")
        assert blob_util.get_mounted_folder_details_from_url(url) == expected_result

    def test_blob_url_with_encoded_special_characters(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/folder%20with%20spaces/blob%40123.txt"
        expected_result = ("/mnt/container", "folder%20with%20spaces/blob%40123.txt")
        assert blob_util.get_mounted_folder_details_from_url(url) == expected_result

    def test_blob_url_with_trailing_slash(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        url = "https://example.blob.core.windows.net/container/"
        self.assertRaises(ValueError, blob_util.get_mounted_folder_details_from_url, url)


class TestGetUrlFromMountedFolderAndFilename(TestCase):
    def test_get_blob_url_from_folder_and_filename(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container"
        filename = "blob.txt"
        expected_result = "https://example.blob.core.windows.net/container/blob.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_get_blob_url_from_folder_and_filename_non_mapped_folder(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/another_container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container"
        filename = "blob.txt"
        self.assertRaises(ValueError, blob_util.get_url_from_mounted_folder_and_filename, folder, filename)

    def test_filename_with_subpath(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container"
        filename = "subdir/blob.txt"
        expected_result = "https://example.blob.core.windows.net/container/subdir/blob.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_folder_with_subdirectories(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container/subdir"
        filename = "blob.txt"
        expected_result = "https://example.blob.core.windows.net/container/subdir/blob.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    # def test_empty_mounting_configurations(self):
    #     blob_mounting_configurations_list = []
    #     folder = "/mnt/container"
    #     filename = "blob.txt"

    def test_multiple_mounting_configurations(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            },
            {
                "storage_account_name": "another_example",
                "storage_account_url": "https://another_example.blob.core.windows.net",
                "container_name": "another_container",
                "mount_point": "/mnt/another_container"
            },
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container"
        filename = "blob.txt"
        expected_result = "https://example.blob.core.windows.net/container/blob.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_none_or_empty_folder(self):
        filename = "blob.txt"
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        for folder in [None, ""]:
            self.assertRaises(ValueError, blob_util.get_url_from_mounted_folder_and_filename, folder, filename)

    def test_none_or_empty_filename(self):
        folder = "/mnt/container"
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        for filename in [None, ""]:
            self.assertRaises(ValueError, blob_util.get_url_from_mounted_folder_and_filename, folder, filename)

    def test_nested_subdirectories(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container/subdir/subdir2"
        filename = "blob.txt"
        expected_result = "https://example.blob.core.windows.net/container/subdir/subdir2/blob.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_filename_with_special_characters(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container"
        filename = "blob@123.txt"
        expected_result = "https://example.blob.core.windows.net/container/blob@123.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_leading_trailing_spaces_in_folder_and_filename(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = " /mnt/container "
        filename = " blob.txt "
        expected_result = "https://example.blob.core.windows.net/container/blob.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder.strip(), filename.strip()) == expected_result

    def test_different_file_extensions(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container"
        for ext in ["txt", "jpg", "png", "csv", "docx"]:
            filename = f"blob.{ext}"
            expected_result = f"https://example.blob.core.windows.net/container/blob.{ext}"
            assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_long_folder_and_filename(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container" + "/subdir" * 100
        filename = "blob" + "extra" * 100 + ".txt"
        expected_result = "https://example.blob.core.windows.net/container" + "/subdir" * 100 + "/" + "blob" + "extra" * 100 + ".txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_filename_as_filepath(self):
        blob_mounting_configurations_list = [{
            "storage_account_name": "example",
            "storage_account_url": "https://example.blob.core.windows.net",
            "container_name": "container",
            "mount_point": "/mnt/container"
        }]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        folder = "/mnt/container"
        filename = "subdir/blob.txt"
        expected_result = "https://example.blob.core.windows.net/container/subdir/blob.txt"
        assert blob_util.get_url_from_mounted_folder_and_filename(folder, filename) == expected_result

    def test_invalid_mounting_configurations(self):
        for blob_mounting_configurations_list in [
            [{}],  # empty dict
            [{"storage_account_url": "https://example.blob.core.windows.net"}],
            # missing container_name and mount_point
            [{"container_name": "container"}],  # missing storage_account_url and mount_point
            [{"mount_point": "/mnt/container"}],  # missing storage_account_url and container_name
        ]:
            self.assertRaises(ValueError, BlobMappingUtility, blob_mounting_configurations_list)


class TestGetMountPointFromContainerName(TestCase):
    def test_get_mount_point_from_container_name(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        assert blob_util.get_mount_point_from_container_name("container") == "/mnt/container"

    def test_get_mount_point_from_container_name_not_mapped(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        self.assertRaises(ValueError, blob_util.get_mount_point_from_container_name, "not_mapped")

    def test_get_mount_point_from_multiple_container_names(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container1",
                "mount_point": "/mnt/container1"
            },
            {
                "storage_account_name": "example2",
                "storage_account_url": "https://example2.blob.core.windows.net",
                "container_name": "container2",
                "mount_point": "/mnt/container2"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        assert blob_util.get_mount_point_from_container_name("container1") == "/mnt/container1"
        assert blob_util.get_mount_point_from_container_name("container2") == "/mnt/container2"

    def test_get_mount_point_from_case_sensitive_container_name(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "Container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        self.assertRaises(ValueError, blob_util.get_mount_point_from_container_name, "container")

    def test_get_mount_point_from_empty_container_name(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        self.assertRaises(ValueError, blob_util.get_mount_point_from_container_name, "")

    def test_get_mount_point_from_none_container_name(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "example",
                "storage_account_url": "https://example.blob.core.windows.net",
                "container_name": "container",
                "mount_point": "/mnt/container"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        self.assertRaises(ValueError, blob_util.get_mount_point_from_container_name, None)

    def test_get_url_from_mounted_filepath_similar_named_containers(self):
        blob_mounting_configurations_list = [
            {
                "storage_account_name": "examplestagingstrgacc",
                "storage_account_url": "https://examplestagingstrgacc.blob.core.windows.net/",
                "container_name": "example-container-raw",
                "mount_point": "/mnt/example-container-raw"
            },
            {
                "storage_account_name": "examplestagingstrgacc",
                "storage_account_url": "https://examplestagingstrgacc.blob.core.windows.net/",
                "container_name": "example-container-raw-cog",
                "mount_point": "/mnt/example-container-raw-cog"
            }
        ]
        blob_util = BlobMappingUtility(blob_mounting_configurations_list)
        # assert blob_util.get_mount_point_from_container_name("example-container-raw") == "/mnt/example-container-raw"
        assert blob_util.get_url_from_mounted_filepath(
            "/mnt/example-container-raw/data/incremental/2023/06/15/11/EXAMPLE01_23/EX1234.json") == "https://examplestagingstrgacc.blob.core.windows.net/example-container-raw/data/incremental/2023/06/15/11/EXAMPLE01_23/EX1234.json"
        assert blob_util.get_url_from_mounted_filepath(
            "/mnt/example-container-raw-cog/data/incremental/2023/06/15/11/EXAMPLE01_23/EX1234.json") == "https://examplestagingstrgacc.blob.core.windows.net/example-container-raw-cog/data/incremental/2023/06/15/11/EXAMPLE01_23/EX1234.json"
