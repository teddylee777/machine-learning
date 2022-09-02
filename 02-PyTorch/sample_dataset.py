# 이미지 데이터셋 다운로드
import urllib.request
import zipfile
import glob
import os
import random
from PIL import Image, UnidentifiedImageError,ImageFile

from torchvision import transforms
from torch.utils.data import Dataset, DataLoader


SEED = 123


# 이미지 Validation을 수행하고 Validate 여부를 return 합니다.
def validate_image(filepath):
    try:
        # PIL.Image로 이미지 데이터를 로드하려고 시도합니다.
        img = Image.open(filepath).convert('RGB')
        img.load()
    except (IOError, OSError): # Truncated (잘린) 이미지에 대한 에러를 출력합니다.
        print(f'Truncated Image is found at: {filepath}')
        return False
    except UnidentifiedImageError: # corrupt 된 이미지는 해당 에러를 출력합니다.
        print(f'Corrupted Image is found at: {filepath}')
        return False
    else:
        return True
    
    
def download_dataset(download_url, folder, default_folder='tmp'):
    # 데이터셋을 다운로드 합니다.
    urllib.request.urlretrieve(download_url, 'datasets.zip')

    # 다운로드 후 tmp 폴더에 압축을 해제 합니다.
    local_zip = 'datasets.zip'
    zip_ref = zipfile.ZipFile(local_zip, 'r')
    zip_ref.extractall(f'{default_folder}/')
    zip_ref.close()

    # 잘린 이미지 Load 시 경고 출력 안함
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    # image 데이터셋 root 폴더
    root = f'{default_folder}/{folder}' 

    dirs = os.listdir(root)

    for dir_ in dirs:
        folder_path = os.path.join(root, dir_)
        files = os.listdir(folder_path)

        images = [os.path.join(folder_path, f) for f in files]
        for img in images:
            valid = validate_image(img)
            if not valid:
                # corrupted 된 이미지 제거
                os.remove(img)

    folders = glob.glob(f'{default_folder}/{folder}/*')
    print(folders)
    return folders


def split_dataset(folders, test_size=0.2):
    # train / test 셋의 파일을 나눕니다.
    train_images = []
    test_images = []

    for folder in folders:
        label = os.path.basename(folder)
        files = sorted(glob.glob(folder + '/*'))

        # 각 Label별 이미지 데이터셋 셔플
        random.seed(SEED)
        random.shuffle(files)

        idx = int(len(files) * test_size)
        train = files[:-idx]
        test = files[-idx:]

        train_images.extend(train)
        test_images.extend(test)

    # train, test 전체 이미지 셔플
    random.shuffle(train_images)
    random.shuffle(test_images)

    # Class to Index 생성
    class_to_idx = {os.path.basename(f):idx for idx, f in enumerate(folders)}

    # Label 생성
    train_labels = [f.split('/')[-2] for f in train_images]
    test_labels = [f.split('/')[-2] for f in test_images]

    print('==='*10)
    print(f'train images: {len(train_images)}')
    print(f'train labels: {len(train_labels)}')
    print(f'test images: {len(test_images)}')
    print(f'test labels: {len(test_labels)}')
    
    return (train_images, train_labels), (test_images, test_labels), class_to_idx


class CustomImageDataset(Dataset):
    def __init__(self, files, labels, class_to_idx, transform):
        super(CustomImageDataset, self).__init__()
        self.files = files
        self.labels = labels
        self.class_to_idx = class_to_idx
        self.transform = transform
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        # file 경로
        file = self.files[idx]
        # PIL.Image로 이미지 로드
        img = Image.open(file).convert('RGB')
        # transform 적용
        img = self.transform(img)
        # label 생성
        lbl = self.class_to_idx[self.labels[idx]]
        # image, label return
        return img, lbl
    
    
def cats_and_dogs(train_transform, test_transform, test_size=0.2):
    download_url = 'https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip'
    folders = download_dataset(download_url, folder='PetImages')
    
    (train_images, train_labels), (test_images, test_labels), class_to_idx = split_dataset(folders, test_size=test_size)
    
    # train, test 데이터셋 생성
    train_dataset = CustomImageDataset(train_images, train_labels, class_to_idx, train_transform)
    test_dataset = CustomImageDataset(test_images, test_labels, class_to_idx, test_transform)
    
    # train, test 데이터 로더 생성 => 모델 학습시 입력하는 데이터셋
    train_loader = DataLoader(train_dataset, 
                              batch_size=32, 
                              shuffle=True,
                              num_workers=8
                             )

    test_loader = DataLoader(test_dataset, 
                             batch_size=32, 
                             shuffle=True,
                             num_workers=8
                            )
    return train_loader, test_loader