import os

from upyun import upyun
from django.db import models
from django.core.files.storage import Storage
from django.utils.six.moves.urllib.parse import urljoin
from django.utils.encoding import filepath_to_uri
from django.utils.deconstruct import deconstructible

# Custom storage
# upyun docs: https://github.com/upyun/python-sdk
@deconstructible
class UpYunStorage(Storage):
  BUCKET_NAME = os.environ.get('UPYUN_BUCKET_NAME') or 'dogrod-media-test'
  USERNAME = os.environ.get('UPYUN_USERNAME') or 'dogrodtest'
  PASSWORD = os.environ.get('UPYUN_PASSWORD') or '123456abc'
  BASE_URL = os.environ.get('UPYUN_BASE_URL') or '//static.dogrod.xyz/'

  up = upyun.UpYun(BUCKET_NAME, USERNAME, PASSWORD, timeout = 30, endpoint = upyun.ED_AUTO)

  def _save(self, name, content):
    full_url = self.BASE_URL + name
    try:
        res = self.up.put(name, content.read(), checksum = False)
    except Exception as e:
        raise

    return full_url

  # find if file existed
  def exists(self, name):
    try:
      self.up.getinfo(name)
    except Exception as e:
      return False

    return True

  # TODO: return real list directory
  def listdir(self, path):
    pass

  # TODO: return real file size
  def size(self, name):
    return 0

  def url(self, name):
    return filepath_to_uri(name)

# Create your models here.
class UpyunMedia(models.Model):
  name = models.CharField(max_length = 40, blank = True, verbose_name = u'file_name')
  url = models.FileField(upload_to = 'media', storage = UpYunStorage(), verbose_name = u'URL')
  create_at = models.DateTimeField(auto_now_add = True)