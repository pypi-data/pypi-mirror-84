from contextlib import contextmanager
import os
import shutil
import uuid

META_EXTENSION = '.pickle'

class FileStorage:

    def __init__(self, directory_path, levels=None):

        if not os.path.exists(directory_path) and os.path.isdir(directory_path):
            raise ValueError("FileStorage: directory_path does not exist")

        self._levels = levels if levels is not None else 4

        self._temp_root_path = os.path.join(directory_path, 'temp')
        self._meta_root_path = os.path.join(directory_path, 'meta')
        self._data_root_path = os.path.join(directory_path, 'data')

        try:
            shutil.rmtree(self._temp_root_path)
        except FileNotFoundError:
            pass

        os.mkdir(self._temp_root_path)

        if not (os.path.exists(self._meta_root_path) and os.path.isdir(self._meta_root_path)):
            os.mkdir(self._meta_root_path)

        if not (os.path.exists(self._data_root_path) and os.path.isdir(self._data_root_path)):
            os.mkdir(self._data_root_path)

        self._directory_path = directory_path

        self._temp_files = {}


    @property
    def root_path(self):
        return self._directory_path


    def _relative_key_path(self, key):
        if len(key) < self._levels:
            raise ValueError("Key is too short")

        path_components = list(key[:self._levels])
        path_components.append(key[self._levels:])
        return  os.path.join(*path_components)


    #noinspection PyTypeChecker
    def __iter__(self):
        for dirpath, dirnames, filenames in os.walk(self._meta_root_path):
            prefix_dirpath = dirpath[len(self._meta_root_path):]
            prefix = ''.join(prefix_dirpath.split(os.sep))
            for filename in filenames:
                 suffix = filename[:-len(META_EXTENSION)]
                 key = prefix + suffix
                 yield key


    def _meta_path(self, key):
        return os.path.join(self._meta_root_path,
            self._relative_key_path(key) + META_EXTENSION)


    def open_temp(self, mode='w', encoding=None):
        temp_filename = str(uuid.uuid4())
        temp_path = os.path.join(self._temp_root_path, temp_filename)
        if encoding is None and 'b' not in mode:
            mode += 'b'
        temp_file = open(temp_path, mode=mode, encoding=encoding)
        self._temp_files[temp_file.fileno()] = temp_path
        return temp_file


    def promote_temp(self, fileno, key):
        if fileno not in self._temp_files:
            raise ValueError("No such file.")
        data_path = self.path(key)
        dir_path = os.path.dirname(data_path)
        os.makedirs(dir_path, exist_ok=True)
        os.rename(self._temp_files[fileno], data_path)
        del self._temp_files[fileno]

    def remove_temp(self, fileno):
        if fileno not in self._temp_files:
            raise ValueError("No such file")
        os.remove(self._temp_files[fileno])
        del self._temp_files[fileno]

    def open_meta(self, key, mode='r'):
        meta_path = self._meta_path(key)
        dir_path = os.path.dirname(meta_path)
        os.makedirs(dir_path, exist_ok=True)
        if 'b' not in mode:
            mode += 'b'
        meta_file = open(meta_path, mode)
        return meta_file

    def path(self, key):
        return os.path.join(self._data_root_path,
            self._relative_key_path(key))

    def open_data(self, key, mode='r', encoding=None):
        # TODO: We should write the file to a temporary path then atomically move it into place
        data_path = self.path(key)
        dir_path = os.path.dirname(data_path)
        os.makedirs(dir_path, exist_ok=True)
        if encoding is None and 'b' not in mode:
            mode += 'b'
        datafile = open(data_path, mode=mode, encoding=encoding)
        return datafile

    # TODO: At some point we should make the files read only

    def remove(self, key):
        os.remove(self._meta_path(key))
        os.remove(self.path(key))

    def close(self):
        self._directory_path = None
    




