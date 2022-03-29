#! /bin/bash
cd /tmp && wget "https://www.dropbox.com/s/9xls0tgtf3edgns/mecab-0.996-ko-0.9.2.tar.gz?dl=1" && tar zxfv mecab-0.996-ko-0.9.2.tar.gz?dl=1 && cd mecab-0.996-ko-0.9.2 && ./configure && make && make check && make install && ldconfig

cd /tmp && \
wget "https://www.dropbox.com/s/i8girnk5p80076c/mecab-ko-dic-2.1.1-20180720.tar.gz?dl=1" && \
apt install -y autoconf && \
tar zxfv mecab-ko-dic-2.1.1-20180720.tar.gz?dl=1 && \
cd mecab-ko-dic-2.1.1-20180720 && \
./autogen.sh && \
./configure && \
make && \
make install && \
ldconfig

cd /tmp && \
git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git && \
cd mecab-python-0.996 && \
python setup.py build && \
python setup.py install

pip install konlpy

