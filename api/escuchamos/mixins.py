from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpRequest
import os

class StoresFileMixin:
    def store_file(self, file, destination_path='', file_name=None):
        file_name = file_name or file.name
        destination_path = destination_path.strip('/')  # Remove any leading/trailing slashes
        stored_path = os.path.join(destination_path, file_name)
        
        # Use default_storage to save the file
        file_path = default_storage.save(stored_path, ContentFile(file.read()))
        
        # Generate the relative path within the media directory
        relative_path = file_path
        
        return relative_path, os.path.splitext(file.name)[-1], file.size

    def put_file(self, file, destination_path='', file_name=None):
        stored_path, file_extension, file_size = self.store_file(file, destination_path, file_name)
        
        # Generate the URL based on the stored path
        file_url = default_storage.url(stored_path)
        
        return {
            'url': file_url,
            'extension': file_extension,
            'size': file_size,
        }
