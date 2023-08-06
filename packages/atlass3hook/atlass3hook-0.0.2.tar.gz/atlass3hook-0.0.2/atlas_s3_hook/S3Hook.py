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

import os
from datetime import datetime
from atlas_client.client import Atlas
from atlas_client.entity_management.s3.S3BucketManager import S3BucketManager
from atlas_client.entity_management.s3.S3ObjectManager import S3ObjectManager
from atlas_client.entity_management.s3.S3PsDirManager import S3PsDirManager
from atlas_s3_hook.S3MetadataClient import S3MetadataClient


class S3Hook:
    def __init__(self, s3_client: S3MetadataClient, atlas_client: Atlas):
        self.s3_end_point = s3_client.get_end_point()
        self.fs = s3_client.get_fs()
        self.s3_bucket_manager = S3BucketManager(atlas_client)
        self.s3_ps_dir_manager = S3PsDirManager(atlas_client)
        self.s3_object_manager = S3ObjectManager(atlas_client)

    def create_atlas_bucket(self, bucket_metadata: dict, bucket_description: str) -> None:
        entity_name = bucket_metadata['name']
        qualified_bucket_name = "s3://" + self.s3_end_point + "/" + entity_name
        domain = self.s3_end_point
        date = bucket_metadata['CreationDate']
        create_time_stamp = round(datetime.timestamp(date) * 1000)
        print("timestamp =", create_time_stamp)
        self.s3_bucket_manager.create_entity(entity_name, domain,
                                             qualified_bucket_name,
                                             bucket_description, create_time=create_time_stamp)

    def create_atlas_ps_dir(self, ps_dir_metadata: dict, ps_dir_description: str) -> None:
        names = ps_dir_metadata['name'].split("/")
        bucket_name = names[0]
        entity_name = "/".join(names[1:])
        qualified_bucket_name = "s3://" + self.s3_end_point + "/" + bucket_name
        qualified_entity_name = qualified_bucket_name + "/" + entity_name
        prefix = entity_name + "/"
        self.s3_ps_dir_manager.create_entity(entity_name, qualified_entity_name,
                                             qualified_bucket_name, prefix, description=ps_dir_description)

    def create_atlas_object(self, object_metadata: dict, owner: str, object_description: str) -> None:
        names = object_metadata['name'].split('/')
        entity_name = names[-1]
        qualified_entity_name = "s3://" + object_metadata['name']
        qualified_ps_dir_name = "s3://" + "/".join(names[:-1])
        ps_dir_prefix = "/".join(names[1:-1]) + "/"
        extension = str(os.path.splitext(entity_name)[1])[1:]
        date = object_metadata['LastModified']
        last_modified_stamp = round(datetime.timestamp(date) * 1000)
        size = object_metadata['size']
        self.s3_object_manager.create_entity(entity_name, qualified_entity_name,
                                             qualified_ps_dir_name, ps_dir_prefix, extension,
                                             owner,
                                             object_description, create_time=last_modified_stamp,
                                             update_time=last_modified_stamp, size=size)
