import os
import re
import pandas as pd
from glob import glob
from fuzzywuzzy import fuzz, process

# lab_pre.xlsx 파일 읽기
lab_pre_df = pd.read_excel('lab_pre.xlsx')

# data 폴더에서 모든 키워드 파일 읽기
keyword_files = glob('data/keyword*.csv')

# 연구자 이름과 키워드 데이터를 저장할 딕셔너리
keyword_data = {}

# 각 키워드 파일에서 연구자 이름과 키워드 추출
for keyword_file in keyword_files:
    try:
        print(f"Reading {keyword_file} with UTF-8 encoding.")
        df = pd.read_csv(keyword_file)
        print(df.head())  # 데이터프레임의 첫 몇 줄을 출력하여 확인
        for index, row in df.iterrows():
            researcher_name = row['Researcher Name']
            keywords = row['Keywords']
            if researcher_name not in keyword_data:
                keyword_data[researcher_name] = []
            keyword_data[researcher_name].append(keywords)
    except UnicodeDecodeError:
        try:
            print(f"Reading {keyword_file} with Latin-1 encoding.")
            df = pd.read_csv(keyword_file)
            print(df.head())  # 데이터프레임의 첫 몇 줄을 출력하여 확인
            for index, row in df.iterrows():
                researcher_name = row['Researcher Name']
                keywords = row['Keywords']
                if researcher_name not in keyword_data:
                    keyword_data[researcher_name] = []
                keyword_data[researcher_name].append(keywords)
        except Exception as e:
            print(f"Error reading {keyword_file}: {e}")

# Check if keyword_data is empty
if not keyword_data:
    print("No keywords data found. Please check the keyword files.")
    exit()

# 각 연구자별로 키워드를 최대 개수로 정렬하여 열을 생성
max_keywords = max(len(keywords) for keywords in keyword_data.values())
print(f"Maximum number of keywords per researcher: {max_keywords}")

# 새로운 키워드 열 이름 생성
keyword_columns = [f'Keywords{i+1}' for i in range(max_keywords)]

# 기존 데이터프레임에 키워드 열 추가
for col in keyword_columns:
    lab_pre_df[col] = ""

# 유사한 이름 매칭
def find_best_match(name, choices):
    best_match = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    return best_match[0] if best_match else None

# 데이터프레임 병합
for index, row in lab_pre_df.iterrows():
    researcher_name = row['Title']
    best_match = find_best_match(researcher_name, keyword_data.keys())
    if best_match:
        for i, keyword in enumerate(keyword_data[best_match]):
            lab_pre_df.at[index, f'Keywords{i+1}'] = keyword

# 병합된 데이터프레임을 CSV 파일로 저장
output_path = 'merged_lab_pre_keywords.csv'
lab_pre_df.to_csv(output_path, index=False, encoding='utf-8')

print(f'병합된 파일이 {output_path}에 성공적으로 저장되었습니다.')
