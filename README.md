# lost112-web-crawler

https://www.lost112.go.kr/find/findList.do

경찰청 유실물 종합관리시스템으로부터 유실물 텍스트 설명과 이미지 데이터를 크롤링하는 도구입니다.

### 사용 방법

project working directory에서 아래와 같이 main.py를 실행합니다.

```
python main.py
```

YYYYMMDD의 형식으로, 시작 날짜와 끝 날짜를 입력합니다. (e.g. 20240331)
그러면 그 날짜에서부터 시작해 끝 날짜를 포함한 날짜까지의 기간 동안 경찰청 유실물 종합관리시스템에 등록된 유실물들의 정보를 크롤링합니다.

log 디렉토리 밑에 `log/YYYYMMDD.log`와 `log/YYYYMMDD.error.log`가 생성되니, 문제가 있을 시 확인 바랍니다.

### 제작자

yechan24680@gmail.com
이예찬 (Yechan Lee)

### 저작권

이 레퍼지토리의 모든 코드는 언제든 사용, 복제, 수정하셔도 좋습니다.
You are totally free to use, copy and modify all the codes in this repository.
