import streamlit as st
from skimage import io
from keras.models import load_model
import autokeras as ak
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os

from io import StringIO

st.title("이미지 분류기")

def predict_image_from_url(url, model, labels):
    # image 다운로드, 로드
    image = io.imread(url)

    # 시각화
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(image)
    ax.axis('off')
    

    # 스케일, resize
    image = image / 255.0
    image = tf.image.resize(image, size=(224, 224))

    # 예측
    x = image.numpy()
    x = np.expand_dims(x, 0)
    pred = model.predict(x)
    pred_idx = pred[0].argmax()

    print(labels)
    output_ = labels[pred_idx]

    print(f'예측 결과: {pred[0]}')
    st.subheader('예측 결과')
    st.write(f'**{output_}**(확률: {pred[0].max()*100:.2f}%)')
    st.pyplot(fig)

# form 생성
form = st.form("my_form")
model_file = form.file_uploader("모델 파일 업로드", type=['h5'])
label_file = form.file_uploader("Label 파일 업로드", type=['txt'])

filepath = None

if model_file is not None:
    dir_name = 'tmp'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    
    filepath = os.path.join(dir_name, model_file.name)
    with open(filepath, 'wb') as f:
        f.write(model_file.getbuffer())

file_url = form.text_input('사진 URL', 'https://health.chosun.com/site/data/img_dir/2022/05/04/2022050401754_0.jpg')

# 제출 버튼
form_submit = form.form_submit_button("예측")

if form_submit:
    if filepath is not None:
        loaded_model = load_model(filepath)
        if label_file is not None:
            bytes_data = label_file.getvalue()
            stringio = StringIO(label_file.getvalue().decode("utf-8"))
            label = dict()
            while True:
                line = stringio.readline()
                if not line: 
                    break
                k, v = line.strip().split()
                label[int(k)] = v

        predict_image_from_url(file_url, loaded_model, label)
    else:
        st.write('업로드한 모델이 제대로 된 파일이 아닙니다ㅜ 다시 시도해 주세요.')

    