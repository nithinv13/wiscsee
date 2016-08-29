import argparse
import random

from sqlitedb import *


VALUE_SIZE = 100 # 100 is the default value size in leveldb
KEY_SIZE = 16 # 16 is the default key size in leveldb
# commit_period = 10


def parse_args():
    parser = argparse.ArgumentParser(
            description="Example: python bench.py -f /tmp/tmp.db -n 100 -p random")
    parser.add_argument('-f', '--dbpath', action='store', required=True)
    parser.add_argument('-n', '--ninsertions', action='store', required=True)
    parser.add_argument('-p', '--pattern', action='store', required=True)
    parser.add_argument('-e', '--period', action='store', required=True)
    args = parser.parse_args()

    return args


class Bench(object):
    def __init__(self, db_path, n_insertions, pattern, commit_period):
        self.db_path = db_path
        self.n_insertions = n_insertions
        self.pattern = pattern
        self.commit_period = commit_period
        # 100 is the default value size in leveldb
        # 16 is the default key size in leveldb
        self.value_size = 100
        self.key_size = 16

        self.db = SqliteDB(db_path)
        self.db.open()
        self.db.initialize()

    def run(self):
        if self.pattern == 'sequential':
            self.insert_sequentially()
        elif self.pattern == 'random':
            self.insert_randomly()
        elif self.pattern == 'preload_and_random':
            self.preload_and_randomly_insert()
        else:
            raise NotImplementedError()

        self.db.commit()

        # print self.db.select_all()

        self.db.close()

    def insert_sequentially(self):
        print 'insert sequentially'
        for i in range(self.n_insertions):
            self.db.insert(key=self.encode_key(i), value='v' * self.value_size)
            if i % self.commit_period == 0 and i > 0:
                self.db.commit()


    def insert_randomly(self):
        print 'insert randomly'
        keys = range(self.n_insertions)
        random.shuffle(keys)
        for i, k in enumerate(keys):
            self.db.insert(key=self.encode_key(k), value='v' * self.value_size)
            if i % self.commit_period == 0 and i > 0:
                self.db.commit()

    def preload_and_randomly_insert(self):
        # preload
        print 'preload_and_randomly_insert'
        for i in range(self.n_insertions):
            self.db.insert(key=self.encode_key(i), value='v' * self.value_size)
        self.db.commit()
        print 'Preloaded', self.n_insertions, 'keys'

        self.update_randomly()

    def update_randomly(self):
        keys = range(self.n_insertions)
        random.shuffle(keys)
        for i, k in enumerate(keys):
            self.db.update(key=self.encode_key(k), value='x' * self.value_size)
            if i % self.commit_period == 0 and i > 0:
                self.db.commit()

    def encode_key(self, key):
        return str(key).zfill(self.key_size)




def main():
    args = parse_args()

    # run(args.dbpath, int(args.ninsertions), args.pattern, int(args.period))
    b = Bench(db_path = args.dbpath,
          n_insertions = int(args.ninsertions),
          pattern = args.pattern,
          commit_period = int(args.period)
            )
    b.run()




if __name__ == '__main__':
    main()





