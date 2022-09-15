## AutoKeras 튜토리얼

![](https://autokeras.com/img/row_red.svg)

AutoKeras는 딥러닝 프레임워크인 `Keras` 기반의 AutoML 시스템입니다.

Texas A&M University의 DATA Lab에서 개발 및 유지보수하고 있으며 AutoKeras의 목표는 모든 사람이 머신러닝에 접근할 수 있도록 하는 것입니다.

- 웹사이트 [**(링크)**](https://autokeras.com/)
- 이미지 분류 튜토리얼 [**(링크)**](https://autokeras.com/tutorial/image_classification/)

간단한 예제(이미지 분류기 생성)

```python
import autokeras as ak

clf = ak.ImageClassifier()
clf.fit(x_train, y_train)
results = clf.predict(x_test)
```

설치

```bash
pip install autokeras
```
