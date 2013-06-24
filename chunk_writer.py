__version__ = '0.1'


class ChunkWriter(object):

    def __init__(self, chunk_size, name_tpl='chunk_{chunk_num}'):
        self._current_chunk = None
        self.name_tpl = name_tpl
        self.chunk_size = chunk_size
        self.chunks = []
        self.count = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_exc_value, traceback):
        self.close()

    def _next_chunk(self):
        if self._current_chunk:
            self._current_chunk.close()

        chunk_num = len(self.chunks) + 1
        name = self.name_tpl.format(chunk_num=chunk_num)

        fh = open(name, 'w')
        self.chunks.append(fh)
        self._current_chunk = fh
        self.count = 0

    @property
    def current_chunk(self):
        if not self._current_chunk or self.count >= self.chunk_size:
            self._next_chunk()

        return self._current_chunk

    def write(self, data, increment=1):
        self.current_chunk.write(data)
        self.count += increment

    def close(self):
        for chunk in self.chunks:
            chunk.close()
