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

import logging

LOG = logging.getLogger('AtlasS3Hook')


class ClientError(Exception):
    """
    The base exception class for all exceptions this library raises.
    """
    message = 'Unknown Error'

    def __init__(self, message=None):
        self.message = message or self.__class__.message
        super(ClientError, self).__init__()

    def __str__(self):
        exception_message = "Unexpected client-side error: %s" % self.message
        LOG.error(exception_message)
        return exception_message


class S3ClientMissingArg(ClientError):
    def __init__(self):
        super().__init__(
            message="You need to provide a s3_end_point, s3_access_key, s3_secret_key, "
                    "s3_token to connect to a s3 sever")
