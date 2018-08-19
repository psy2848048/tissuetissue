# TissueTissue NLP

[![Build Status](https://travis-ci.org/psy2848048/tissuetissue.svg?branch=master)](https://travis-ci.org/psy2848048/tissuetissue) <br>

TissueTissue에서 제작한 NLP 모듈 모음입니다.
추후 Code 정리, Packaging, 오프라인 구동 기능 및 DB 업데이트 기능 추가를 통하여 간편하게 사용할 수 있도록 업데이트 할 예정입니다.

------

### 1. 복합명사 분해기

해당 모듈을 import해서 사용하실 수 있습니다.<br>
현재는 원격 DB에 접속해서 구동하고 있기 때문에 필히 **인터넷에 연결**되어 있어야 구동이 가능합니다.

noun/compound_noun_analyzer.py

```python
from compound_noun_analyzer import analyzer

res = analyzer('한국전력공사')
# ['한국', '전력', '공사']
```

<br>
<br>
Batch로 테스트하고 싶으면 다음과 같이 CSV 파일을 넣어 사용하실 수 있습니다.

```python
python3 compound_noun_analyzer.py -i ../testdata/input.txt

# Input 텍스트 파일은 다음과 같은 형식을 따라야 합니다.

# 한국전력공사
# 이스탄불
# 아시아나항공
# ...
```

결과는 output.txt로 출력되며, 형식은 다음과 같습니다.

```text
한국 전력 공사
이스탄불
아시아나 항공
....
```

