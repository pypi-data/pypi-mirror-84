#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import s3fs
from s3fs import S3FileSystem
from atlas_s3_hook.S3PathClass import S3PathClass
from atlas_s3_hook.S3PathType import S3PathType


class S3MetadataClient:
    def __init__(self, s3_end_point: str, s3_access_key: str, s3_secret_key: str, s3_token: str):
        self.s3_end_point = s3_end_point
        self.fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': 'http://' + s3_end_point}, key=s3_access_key,
                                    secret=s3_secret_key,
                                    token=s3_token)

    def get_fs(self) -> S3FileSystem:
        return self.fs

    def get_end_point(self) -> str:
        return self.s3_end_point

    @staticmethod
    def get_class_from_entity_meta(entity_metadata: dict) -> S3PathClass:
        path_class = entity_metadata['StorageClass']
        if path_class == 'BUCKET':
            return S3PathClass.BUCKET
        elif path_class == 'DIRECTORY':
            return S3PathClass.DIR
        elif path_class == 'STANDARD':
            return S3PathClass.OBJECT
        else:
            raise ValueError

    @staticmethod
    def get_type_from__entity_meta(entity_metadata: dict) -> S3PathType:
        path_type = entity_metadata['type']
        if path_type == 'directory':
            return S3PathType.directory
        elif path_type == 'file':
            return S3PathType.file
        else:
            raise ValueError

    def get_path_meta_data(self, entity_path: str) -> dict:
        meta_data = self.fs.stat(entity_path)
        return meta_data

    def get_class_from_path(self, entity_path: str) -> S3PathClass:
        entity_metadata = self.get_path_meta_data(entity_path)
        return self.get_class_from_entity_meta(entity_metadata)

    def get_type_from_path(self, entity_path: str) -> S3PathType:
        entity_metadata = self.get_path_meta_data(entity_path)
        return self.get_type_from__entity_meta(entity_metadata)
