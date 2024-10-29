import requests
from bs4 import BeautifulSoup
import pandas as pd

# 엑셀 파일 로드
file_path = './div_links_data_unique1.xlsx'
data = pd.read_excel(file_path)


# 수정된 데이터프레임을 새 엑셀 파일로 저장
data.to_excel('updated_div_links_data2.xlsx', index=False)
