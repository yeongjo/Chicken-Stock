import pandas as pd

dfstockcode = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

# 종목코드에 값을 6자리 문자열로 설정 
#    종목코드의 숫자값을 6자리 문자열로 변환
#    채우는 자리는 0으로 채우기
dfstockcode.종목코드 = dfstockcode.종목코드.map('{:06d}'.format)

# 필요한 컬럼만으로 DataFrame을 설정
dfstockcode = dfstockcode[['회사명', '종목코드']]

# 컬럼명을 한글에서 영어로 변경 
dfstockcode = dfstockcode.rename(columns={'회사명':'name', '종목코드':'code'})

dfstockcode.set_index('name', inplace=True)