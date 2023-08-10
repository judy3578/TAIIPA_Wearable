# Wearable 관련 코드

```
├── README.md
└── data_preprocessing_and_training : Wearable 데이터 처리 및 학습 코드
    └── 01_[dataset]_pickle.ipynb : 공개 데이터셋을 전처리하여 학습 형태로 만들어 저장 (PAMAP2, SBHAR, MotionSense, KU-HAR)
    └── 02_all_data_combined_pickle.ipynb : 여러 공개 데이터셋을 합쳐서 하나의 데이터 셋으로 저장
    └── 03_HAR_combined_data_learning.ipynb : 데이터를 모델 학습 (Conv1d, LSTM, GRU)
    └── 03_HAR_combined_data_learning_transformer.ipynb : 데이터를 모델 학습 (Transformer)
    └── 04_blind_test.ipynb : 학습된 모델을 이용하여 blind test
    └── out : 학습 모델 저장 폴더
    
└── data_visualization : 데이터 시각화
    └── watch_data_map : wearable 데이터의 gps 정보를 활용하여 map 시각화
    └── watch_data_review : 수집된 wearable 데이터 확인 및 정리를 위한 tool
```

## 상세 내용 노션 페이지 참고
[https://dune-bear-fac.notion.site/TAIIPA_Wearable-4a25c42a226248d7a51a3b5d14b91df4?pvs=4](https://www.notion.so/TAIIPA_Wearable-4a25c42a226248d7a51a3b5d14b91df4?pvs=21)

노션 페이지에 각 코드의 실행 화면 및 설명을 작성하였습니다
