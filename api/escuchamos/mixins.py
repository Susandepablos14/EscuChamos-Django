import os
from django.core.files.storage import default_storage
from django.utils.text import slugify

class StoresFileMixin:
    def store_file(self, file, destination_path='', file_name=None):
        file_name = file_name or file.name
        stored_path = os.path.join(destination_path, file_name)
        
        # Verificar y crear el directorio si no existe
        directory = os.path.dirname(stored_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(stored_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return stored_path, os.path.splitext(file.name)[-1], file.size

    def put_file(self, file, destination_path='', file_name=''):
        stored_path, file_extension, file_size = self.store_file(file, destination_path, file_name)
        return {
            'path': stored_path,
            'extension': file_extension,
            'size': file_size,
        }
