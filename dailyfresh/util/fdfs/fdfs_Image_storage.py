from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FDFSImageStorage(Storage):
    #文件存储
    def _save(self, name, content):
       client_conf_dir = settings.CLIENT_CONF_DIR
       client = Fdfs_client(client_conf_dir)
       ret = client.upload_by_buffer(content.read())
       if ret.get('Status') != 'Upload successed.':
           raise Exception('文件上传失败')
       file_id = ret.get('Remote file_id')
       return  file_id

    def exists(self, name):
        return False

    def url(self, name):
        return settings.FDFS_SERVER_URL+name
