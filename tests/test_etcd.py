from twisted.internet.task import react
from twisted.internet.defer import inlineCallbacks

import txaio
from txaioetcd import Client, KeySet

import numpy as np
import pandas as pd
import pyarrow as pa
import lmdb

import zlmdb
from zlmdb._pmap import _StringKeysMixin, PersistentMap

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


class _DataFrameValuesMixin(object):
    def __init__(self, marshal=None, unmarshal=None):
        self._marshal = marshal or self._zlmdb_marshal
        self._unmarshal = unmarshal or self._zlmdb_unmarshal

    def _serialize_value(self, value):
        return pa.serialize(value).to_buffer()

    def _deserialize_value(self, data):
        return pa.deserialize(data)


class MapStringDataFrame(_StringKeysMixin, _DataFrameValuesMixin, PersistentMap):
    """
    Persistent map with string (utf8) keys and OID (uint64) values.
    """

    def __init__(self, slot=None, compress=None):
        PersistentMap.__init__(self, slot=slot, compress=compress)


class MySchema(zlmdb.Schema):

    samples: MapStringDataFrame

    def __init__(self):
        self.samples = MapStringDataFrame(1)



@inlineCallbacks
def main(reactor):
    etcd = Client(reactor)
    status = yield etcd.status()
    print(status)

    with TemporaryDirectory() as dbpath:
        print('Using temporary directory {} for database'.format(dbpath))

        schema = MySchema()

        with zlmdb.Database(dbpath) as db:
            with db.begin(write=True) as txn:
                for i in range(10):
                    if i % 2:
                        key = 'key{}'.format(i)
                        value = pd.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])
                        schema.samples[txn, key] = value

        with zlmdb.Database(dbpath) as db:
            with db.begin() as txn:
                for i in range(10):
                    key = 'key{}'.format(i)
                    value = schema.samples[txn, key]
                    print('key={} : value=\n{}'.format(key, value))


    def on_change(kv):
        key = kv.key.decode()
        df = pa.deserialize(kv.value)
        print('on_change: value={} key=\n{}'.format(key, df))

    ks = [KeySet('k'.encode(), prefix=True)]
    d = etcd.watch(ks, on_change)

    for i in range(5):
        print('watching for 1s ..')
        yield txaio.sleep(1)

        key = 'key{}'.format(i).encode()

        df = pd.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])
        value = pa.serialize(df).to_buffer()

        etcd.set(key, value)

    print('watching for 1s ..')
    yield txaio.sleep(1)

    d.cancel()

    # db_file = '/data/scratch/test1.db'
    # db1_name = 'db1'.encode()

    # env = lmdb.Environment(db_file, max_dbs=5, map_size=16*(2**20), writemap=False, meminit=False, subdir=False)
    # db1 = env.open_db(db1_name)

    # df = pd.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])

    # key1 = 'key1'.encode()
    # value1 = pa.serialize(df).to_buffer()

    # with env.begin(db=db1, write=True) as txn:
    #     txn.put(key1, value1)

    # env.sync()
    # print('transaction {} complete.'.format(env.info()['last_txnid'] - 1))

    # with env.begin(db=db1, buffers=True) as txn:
    #     data_buffer = txn.get(key1)
    #     df = pa.deserialize(data_buffer)

if __name__ == '__main__':
    txaio.start_logging(level='info')
    react(main)