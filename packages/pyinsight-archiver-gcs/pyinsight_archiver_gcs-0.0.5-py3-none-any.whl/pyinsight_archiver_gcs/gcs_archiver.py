import json
import logging
import gcsfs
import google.auth
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage
from google.api_core.exceptions import NotFound
from pyinsight import archiver
from pyinsight.utils.core import remove_none, get_fields_from_filter

class GCSArchiver(archiver.Archiver):
    def __init__(self):
        super().__init__()
        self.data_encode = 'blob'
        self.data_format = 'parquet'
        self.data_store = 'file'
        self.supported_encodes = ['blob']
        self.supported_formats = ['parquet']
        self.bucket_location = 'eu'
        self.bucket_storage_class = 'STANDARD'
        self.project_id = ''
        self.fs = None

    def set_bucket_attributes(self, location, storage_class):
        self.bucket_location = location
        self.bucket_storage_class = storage_class

    def init_topic(self, topic_id):
        project_id = google.auth.default()[1]
        storage_client = storage.Client()
        bucket_name = '-'.join([project_id, topic_id])
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = self.bucket_storage_class
        try:
            storage_client.get_bucket(bucket_name)
        except NotFound:
            storage_client.create_bucket(bucket, location=self.bucket_location)

    def set_fs(self, project_id, fs: gcsfs.GCSFileSystem):
        self.project_id = project_id
        self.fs = fs

    def _merge_workspace(self):
        if len(self.workspace) > 1:
            self.workspace[:] = [pa.concat_tables(self.workspace, True)]

    def set_current_topic_table(self, topic_id, table_id):
        self.topic_id = topic_id
        self.table_id = table_id
        self.table_path = 'gs://' + self.project_id + '-' + self.topic_id + '/' + self.table_id + '/'

    def add_data(self, data: list):
        ds = pa.Table.from_pandas(pd.DataFrame(data, dtype='object'))
        self.workspace_size += ds.nbytes
        self.workspace.append(ds)

    def remove_data(self):
        self.merge_key, self.workspace, self.workspace_size = '', list(), 0

    def get_data(self) -> list:
        if len(self.workspace) == 0:
            return []
        if len(self.workspace) > 1:
            self._merge_workspace()
        return json.loads(self.workspace[0].to_pandas().to_json(orient='records'), object_hook=remove_none)

    def archive_data(self):
        if len(self.workspace) == 0:
            return ''
        if len(self.workspace) > 1:
            self._merge_workspace()
        archive_file_name = self.table_path + self.merge_key + '.parquet'
        pq.write_table(self.workspace[0], archive_file_name, compression='gzip', filesystem=self.fs)
        return archive_file_name

    def read_data_from_file(self, data_encode, data_format, file_path):
        if data_encode not in self.supported_encodes:
            logging.error("{}-{}: Encode {} not supported".format(self.topic_id, self.table_id, data_encode))
        elif data_format not in self.supported_formats:
            logging.error("{}-{}: Format {} not supported".format(self.topic_id, self.table_id, data_encode))
        elif not self.fs.exists(file_path):
            logging.error("{}-{}: Path {} not found / compatible".format(self.topic_id, self.table_id, file_path))
        else:
            meta_data = pq.ParquetDataset(file_path, filesystem=self.fs)
            pq_data = meta_data.read()
            return json.loads(pq_data.to_pandas().to_json(orient='records'), object_hook=remove_none)

    def append_archive(self, append_merge_key, fields=None):
        field_list = fields
        append_filename = self.table_path + append_merge_key + '.parquet'
        meta_data = pq.ParquetDataset(append_filename, filesystem=self.fs)
        available_fields = set([f.name for f in meta_data.schema])
        fields_to_be_loaded = list(set(fields)  & available_fields)
        ds = meta_data.read(columns=fields_to_be_loaded)
        self.workspace.append(ds)
        self.workspace_size += ds.nbytes

    def remove_archives(self, merge_key_list):
        for merge_key in merge_key_list:
            self.fs.rm(self.table_path + merge_key + '.parquet')
