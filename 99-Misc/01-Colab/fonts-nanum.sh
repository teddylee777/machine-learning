#! /bin/bash
wget http://data.jaen.kr/download?download_path=%2Fdata%2Ffiles%2FmySUNI%2Fdatasets%2FNanumGothic.zip -O NanumGothic.zip
rm -rf NanumGothic
mkdir NanumGothic
unzip NanumGothic.zip -d NanumGothic
rm -rf /usr/share/fonts/truetype/nanum
mkdir /usr/share/fonts/truetype/nanum
yes | cp -r NanumGothic/NanumGothic.ttf /usr/share/fonts/truetype/nanum/NanumGothic.ttf
fc-cache -f -v
rm -rf NanumGothic
