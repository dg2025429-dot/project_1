# 🚇 서울 지하철 혼잡도 분석 웹앱

서울교통공사 지하철 혼잡도 데이터를 활용한 Streamlit 기반 데이터 시각화 서비스입니다.

## 주요 기능

* 역별 혼잡도 조회
* 시간대별 혼잡도 분석
* 호선별 비교
* 혼잡도 TOP10 역 조회
* 인터랙티브 Plotly 차트

## 데이터

서울교통공사 지하철 혼잡도 정보

파일명

서울교통공사_지하철혼잡도정보_20260331.csv

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
streamlit run main.py
```

## 프로젝트 구조

```text
main.py
pages/
 ├─ 01_역별_혼잡도.py
 ├─ 02_시간대_분석.py
 ├─ 03_호선_비교.py
 └─ 04_혼잡도_TOP10.py
```

## 사용 라이브러리

* Streamlit
* Pandas
* Plotly
* NumPy
