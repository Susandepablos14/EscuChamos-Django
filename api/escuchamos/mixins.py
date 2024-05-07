import os
from django.core.files.storage import default_storage
from django.utils.text import slugify
import uuid

class StoresFileMixin:
    def store_file(self, file, destination_path='', file_name=None):
        file_extension = os.path.splitext(file.name)[-1]
        if file_name is None:
            file_name = str(uuid.uuid4())  # Generar un nombre único si no se proporciona uno
        stored_file_name = f"{file_name}{file_extension}"
        stored_path = os.path.join(destination_path, stored_file_name)
        with default_storage.open(stored_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return stored_path, file_extension, file.size

    def put_file(self, file, destination_path='', file_name=''):
        stored_path, file_extension, file_size = self.store_file(file, destination_path, file_name)
        return {
            'path': stored_path,
            'extension': file_extension,
            'size': file_size,
        }
