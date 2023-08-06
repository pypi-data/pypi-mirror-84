# easyrocks
simple interface to rocksdb

How to install

```
# https://github.com/facebook/rocksdb/blob/master/INSTALL.md
sudo apt-get install build-essential libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev liblz4-dev libzstd-dev
git clone https://github.com/facebook/rocksdb.git
cd rocksdb
NUM_PROCS=$(nproc)
sudo make -j NUM_PROCS install
# Also see this for Python installation:
# https://pypi.org/project/python-rocksdb/
```

