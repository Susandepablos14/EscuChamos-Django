from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.http import HttpRequest

class StoresFileMixin:
    def store_file(self, file, destination_path='', file_name=None):
        file_name = file_name or file.name
        stored_path = os.path.join(settings.MEDIA_ROOT, destination_path, file_name)
        
        # Use default_storage to save the file
        default_storage.save(stored_path, ContentFile(file.read()))
        
        # Generate the relative path within the media directory
        relative_path = os.path.join(destination_path, file_name)
        
        return relative_path, os.path.splitext(file.name)[-1], file.size

    def put_file(self, file, destination_path='', file_name=''):
        stored_path, file_extension, file_size = self.store_file(file, destination_path, file_name)
        
        # Generate the URL based on request (works in both development and production)
        request = HttpRequest()
        absolute_url = request.build_absolute_uri(settings.MEDIA_URL + stored_path)
        
        return {
            'url': absolute_url,
            'extension': file_extension,
            'size': file_size,
        }
