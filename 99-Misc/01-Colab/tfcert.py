import subprocess

try:
    import google.colab
    IN_COLAB = True
except:
    IN_COLAB = False
    
if IN_COLAB:
    print('==='*20)
    print('설치환경: Google Colab')
    print('TensorFlow 시험환경을 구성중입니다. 잠시만 기다려 주세요.\n(설치는 약 1~5분 정도 소요 됩니다)')
    print('==='*20)
else:
    print('==='*20)
    print('설치환경: Local')
    print('TensorFlow 시험환경을 구성중입니다. 잠시만 기다려 주세요.\n(설치는 약 1~5분 정도 소요 됩니다)')
    print('==='*20)

subprocess.run(['pip', 'install', 'tensorflow==2.9.0'])
subprocess.run(['pip', 'install', 'tensorflow-datasets==4.6.0'])
subprocess.run(['pip', 'install', 'numpy==1.22.4'])
subprocess.run(['pip', 'install', 'Pillow==9.0.0'])
subprocess.run(['pip', 'install', 'scipy==1.7.3'])
subprocess.run(['pip', 'install', 'pandas==1.4.2'])
subprocess.run(['pip', 'install', 'urllib3'])
subprocess.run(['pip', 'install', 'protobuf==3.19.6'])
subprocess.run(['pip', 'install', 'tensorflow-metadata==1.12.0'])

print('==='*20)
print('[알림] TensorFlow 시험환경 구성이 완료 되었습니다.')
print('==='*20)
    
