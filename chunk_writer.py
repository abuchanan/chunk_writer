import os


__version__ = '1.0.0'


class FullChunk(Exception): pass

class FileChunk(object):

    def __init__(self, size, name):
        self.size = size
        self.count = 0
        self._fh = open(name, 'w')

    def _write_data(self, data):
        self._fh.write(str(data))

    def write(self, data, increment=1):

        if self.count >= self.size:
            raise FullChunk()

        self._write_data(data)
        self.count += increment

    @property
    def name(self):
        return self._fh.name

    def close(self):
        self._fh.close()


class ChunkWriter(object):

    Chunk = FileChunk

    def __init__(self, chunk_size, name_tpl='chunk_{chunk_num}', dir=None):
        self.chunk_size = chunk_size
        self.name_tpl = os.path.join(dir, name_tpl)
        self.chunks = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_exc_value, traceback):
        self.close()

    def _next_chunk(self):
        num = len(self.chunks) + 1
        name = self.name_tpl.format(chunk_num=num)
        chunk = self.Chunk(self.chunk_size, name)
        self.chunks.append(chunk)

    @property
    def current(self):
        if self.chunks:
            return self.chunks[-1]

    def write(self, *args, **kwargs):

        if not self.current:
            self._next_chunk()

        try:
            return self.current.write(*args, **kwargs)

        except FullChunk:
            self._next_chunk()
            return self.write(*args, **kwargs)

    def close(self):
        for chunk in self.chunks:
            chunk.close()


class DirChunk(FileChunk):

    def __init__(self, size, name):
        self.dir = os.path.dirname(name)
        os.makedirs(self.dir)
        super(DirChunk, self).__init__(size, name)


class DirChunkWriter(ChunkWriter):

    Chunk = DirChunk

    def __init__(self, size, dir_tpl='chunk_{chunk_num}', file_name='chunk_data',
                 dir=None):

        self.dir_tpl = dir_tpl
        self.file_name = file_name
        tpl = os.path.join(self.dir_tpl, self.file_name)
        super(DirChunkWriter, self).__init__(size, tpl, dir=dir)
