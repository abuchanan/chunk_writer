import os
import shutil
from tempfile import mkdtemp
import unittest

from nose.tools import eq_, ok_

import chunk_writer as cw


CHUNK_SIZE = 10


class Tests(unittest.TestCase):

    def setUp(self):
        self.TMP_DIR = mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.TMP_DIR)
        

    def test_ChunkWriter(self):

        with cw.ChunkWriter(CHUNK_SIZE, dir=self.TMP_DIR) as writer:
            for x in range(1, 20):
                writer.write(x)

        eq_(len(writer.chunks), 2)

        eq_(writer.chunks[0].name, os.path.join(self.TMP_DIR, 'chunk_1'))
        eq_(writer.chunks[1].name, os.path.join(self.TMP_DIR, 'chunk_2'))

        a = open(writer.chunks[0].name).read()
        eq_('12345678910', a)

        a = open(writer.chunks[1].name).read()
        eq_('111213141516171819', a)

        ok_(writer.chunks[0]._fh.closed)
        ok_(writer.chunks[1]._fh.closed)


    def test_DirChunkWriter(self):

        with cw.DirChunkWriter(CHUNK_SIZE, dir=self.TMP_DIR) as writer:
            for x in range(1, 20):
                writer.write(x)

        eq_(len(writer.chunks), 2)

        eq_(writer.chunks[0].name, os.path.join(self.TMP_DIR, 'chunk_1', 'chunk_data'))
        eq_(writer.chunks[1].name, os.path.join(self.TMP_DIR, 'chunk_2', 'chunk_data'))

        a = open(writer.chunks[0].name).read()
        eq_('12345678910', a)

        a = open(writer.chunks[1].name).read()
        eq_('111213141516171819', a)

        ok_(writer.chunks[0]._fh.closed)
        ok_(writer.chunks[1]._fh.closed)
