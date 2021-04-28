import sqlite3
import pandas as pd
import FinanceDataReader as fdr
import numpy as np
import datetime
from scipy import stats

def get_date(start, terms):
    return pd.bdate_range(end = start,tz='Asia/Seoul',periods=terms).date

meta = fdr.StockListing('KOSPI')
meta.dropna(how='all',subset=meta.columns[3:],inplace=True)

#평균 관리선
avg_thres_st_ed = 3 #시가 종가 비교 3%이상 -> 둘다 동일 양봉 음봉
avg_thres_h_l = 5
avg_thres_dtd = 3

#위험 관리선
dager_thres_st_ed = -7
dager_thres_h_l = -7
dager_thres_dtd = -7

#각 주식별 수치 구하기
names = {}
codes = meta['Symbol'].unique()
stocks_P = {}
stocks_V = {}

#기간 정하기
ana_period = 120
show_period = 30

for code in codes:
    
    #find meta & read datas
    name = meta.loc[meta['Symbol']==code, "Name"].values[0]
    finance = fdr.DataReader(code)
    
    #drop na
    finance.replace(0,np.NaN,inplace=True)
    
    #각 주식별 수익성,변동성 변수 초기화
    profits = []
    variances = []
    
    for n in range(show_period) :
        subset = finance[::-1].iloc[n:n+ana_period].copy()
        
        #수익성 점수
        subset['YM'] = subset.index.year.astype(str) + subset.index.month.astype(str)
        temp = subset.groupby('YM').mean()['Open']
        temp = (temp - temp.shift(1))/temp * 100
        profit = temp.values[1:].sum()*20
        
        #시가 종가 비교수치
        day_percent_st_ed = (subset['Open']-subset['Close'])/subset['Open']
        day_count_st_ed=(day_percent_st_ed.abs()*100 > avg_thres_st_ed).sum()
        
        cond = day_percent_st_ed*100 < dager_thres_st_ed
        day_count_st_ed_dag = day_percent_st_ed[cond].abs().sum()*100

        #고가 저가 비교수치
        day_percent_h_l = (subset['High']-subset['Low'])/subset['Open']
        day_count_h_l=(day_percent_h_l.abs()*100 > avg_thres_h_l).sum()
        
        cond = day_percent_h_l*100 < dager_thres_h_l
        day_count_h_l_dag = day_percent_h_l[cond].abs().sum()*100

        #일간 종가 수치 비교
        day_to_day_ed = subset['Change']
        day_to_day_count=(day_to_day_ed.abs()*100 > avg_thres_dtd).sum()
        
        cond = day_to_day_ed*100 < dager_thres_dtd
        day_to_day_dag = day_to_day_ed[cond].abs().sum()*100
        
        totalCount = day_count_st_ed+day_count_st_ed_dag+day_count_h_l+day_count_h_l_dag+day_to_day_count+day_to_day_dag
    
        #결과 저장
        profits.append(profit)
        variances.append(totalCount)        
    
    #정규화    
    profits = stats.zscore(profits)
    variances = stats.zscore(variances)
    score = profits - variances

    #각 주식별 점수 저장
    names[name] = score
    stocks_P[name] = profits
    stocks_V[name] = variances
    
    print(name,score)
    

push = pd.DataFrame(names,index=get_date(datetime.datetime.now(),30)[::-1])

goods = []
bads = []
recos = []

for i in range(len(push)):
    good = push.iloc[i,:].sort_values(ascending=False)[:10].mean()
    bad = push.iloc[i,:].sort_values(ascending=False)[10:10+50].mean()
    reco = push.iloc[i,:].sort_values(ascending=False)[:10].index.to_list()
    reco = ",".join(reco)
    
    goods.append(good)
    bads.append(bad)
    recos.append(reco)
    
# 풀 차트에 들어갈 테이블
push2 = pd.DataFrame({"Good":goods,"Bad":bads,"Recommend":recos})
push2.index = push.index
push2 = push2.reset_index()
push2.index.name = "id"

# 개별 추적 subplot에 들어갈 테이블
push3 = push.unstack()
push3_pv = pd.concat(
    [
        pd.DataFrame(stocks_P,index=get_date(datetime.datetime.now(),30)[::-1]).unstack(),
        pd.DataFrame(stocks_V,index=get_date(datetime.datetime.now(),30)[::-1]).unstack(),
    ],

    axis=1,
    )
push3 = pd.concat([push3,push3_pv],axis=1)
push3.reset_index(inplace=True)

push3.columns = ['Name','Date','Score','Profit','Variances']
push3.index.name = "id"
print(push3)

#DB연결
db_path = "capstone/db.sqlite3"
con = sqlite3.connect(db_path)

#DB데이터 푸시
push2.to_sql("Fullplot",con,if_exists="replace")
push3.to_sql("Subplots",con,if_exists="replace")