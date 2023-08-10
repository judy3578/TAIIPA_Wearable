#!/usr/bin/env python
# coding: utf-8


import folium
import numpy as np
import pandas as pd
from tqdm import tqdm
import glob
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


#원하는 폴더 고르기
folder = './20230531_GalaxyWatch4_1_3XSF__S7_C00_walking_syj_L'

#검토할 폴더 안의 모든 txt 불러오기
files = sorted(glob.glob('{}/*.txt'.format(folder)))
print("파일개수:",np.shape(files)[0])

#파일 이름 몇개 찍어보기
print(files[:5])

# readme 파일 제외 및 읽기
txt_files = []

for i in files:
    if not i.endswith('readme.txt'):
        txt_files.append(i)
    else:
        with open(i, "r", encoding='utf-8') as f:
            data = f.read()
            print(data)

# 모든 txt 파일을 하나의 df로 만들기
# all_data = pd.DataFrame()
all_data = []
for i in txt_files:
    data = pd.read_csv(i, sep="\t", header=None)
    data = np.array(data)
    all_data.append(data) #, ignore_index=True)
all_data = np.array(all_data)
dim = np.shape(all_data)[-1]
print(dim)
all_data = all_data.reshape(-1, dim)
print(np.shape(all_data))
all_data = pd.DataFrame(all_data)
print(np.shape(all_data))

if dim == 15:
    all_data.columns = ['acc_time', 'gyro_time', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'lacc_x', 'lacc_y', 'lacc_z', 'longitude', 'latitude', 'speed', 'step']
else:
    all_data.columns = ['acc_time', 'gyro_time', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'lacc_x',
                        'lacc_y', 'lacc_z', 'longitude', 'latitude']


df = all_data


# ### 경로 클릭하면 정보 출력


# 데이터에서 고유한 위치를 가져옵니다.
locations = df[['latitude', 'longitude']].drop_duplicates().values

# 시작점과 끝점을 정의합니다.
start_location = locations[0]
end_location = locations[-1]

start_location = list(start_location)
end_location = list(end_location)

# folium으로 지도를 생성합니다. 시작점을 중심으로 하며, 적절한 줌 레벨을 설정합니다.
m = folium.Map(location=start_location, zoom_start=14)

# 경로를 그립니다. 각 위치에 대해 경로에 라인을 추가합니다.
folium.PolyLine(locations, color="red", weight=2.5, opacity=1).add_to(m)

# 시작점과 끝점에 마커를 추가합니다. 시작점의 색상은 빨간색, 끝점의 색상은 파란색으로 설정합니다.
folium.Marker(start_location, popup='Start', icon=folium.Icon(color='red')).add_to(m)
folium.Marker(end_location, popup='End', icon=folium.Icon(color='blue')).add_to(m)

# 각 위치에 대해 팝업을 추가합니다. 팝업에는 speed와 longitude, latitude 정보, 그리고 step 정보가 포함됩니다.
# 이번에는 folium.Circle를 이용해 작게 표시합니다.
for location in locations[1:-1]:  # 시작점과 끝점을 제외합니다.
    location = list(location)
    row = df.loc[(df['latitude'] == location[0]) & (df['longitude'] == location[1])].iloc[0]
    if dim == 15:
        folium.Circle(location,
                      radius=1,  # Circle의 크기를 설정합니다. 필요에 따라 조정 가능합니다.
                      popup=f"Speed: {row['speed']}<br>Longitude: {row['longitude']}<br>Latitude: {row['latitude']} <br>Step: {row['step']}",
                      color='blue', fill=True, fill_color='blue').add_to(m)
    else:
        folium.Circle(location,
                      radius=1,  # Circle의 크기를 설정합니다. 필요에 따라 조정 가능합니다.
                      popup=f"Longitude: {row['longitude']}<br>Latitude: {row['latitude']}",
                      color='blue', fill=True, fill_color='blue').add_to(m)


# 지도를 출력합니다.
m.save('map.html')


### 마우스 위치 가져다 대면 정보 출력

# 데이터에서 고유한 위치를 가져옵니다.
locations = df[['latitude', 'longitude']].drop_duplicates().values
locations = list(locations)

# 시작점과 끝점을 정의합니다.
start_location = locations[0]
end_location = locations[-1]

start_location = list(start_location)
end_location = list(end_location)

# folium으로 지도를 생성합니다. 시작점을 중심으로 하며, 적절한 줌 레벨을 설정합니다.
m = folium.Map(location=start_location, zoom_start=14)

# 이전의 코드에서 반복문을 사용하여 데이터의 각 행을 순회
for i in range(len(df)):
    # 데이터에서 위도, 경도, 스피드, 스텝 정보 추출
    lat = df.loc[i, 'latitude']
    lon = df.loc[i, 'longitude']
    # speed = df.loc[i, 'speed']
    # step = df.loc[i, 'step']

    # 이 정보들을 tooltip으로 표시
    #tooltip_text = f"Speed: {speed}, Step: {step} \n lat: {lat} lon: {lon}"
    tooltip_text = f"lat: {lat} lon: {lon}"

    # 시작점과 끝점에 대한 Marker 처리
    if i == 0:
        folium.Marker([lat, lon], popup='<i>Start</i>', tooltip=tooltip_text, icon=folium.Icon(color='red')).add_to(m)
    elif i == len(df)-1:
        folium.Marker([lat, lon], popup='<i>End</i>', tooltip=tooltip_text, icon=folium.Icon(color='blue')).add_to(m)
    else:
        folium.Circle([lat, lon], radius=1, tooltip=tooltip_text).add_to(m)



m.save('map2.html')

print('finish...')


