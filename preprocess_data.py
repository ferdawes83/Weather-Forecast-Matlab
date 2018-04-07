import pandas as pd
import numpy as np
import re

cols = ['time','temperature','heat_index','dew_point','humidity','pressure','visibility','wind_direction','wind_speed','gust_speed','precipitation','events','conditions']
df = pd.read_csv('weatherdata.csv',names=cols)


#convert date to datetime format
# df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y')

#Remove units, convert data type into float
remove_unit_cols = ['temperature','heat_index','dew_point','humidity','pressure','visibility']
for col in remove_unit_cols:
    df[col] = df[col].map(lambda x: x.rstrip(' °C%hPakm') if x!='-' else np.nan)
    df[col] = df[col].astype('float16')

df['wind_speed'] = df['wind_speed'].map(lambda x: x[0:x.find('k')] if x!='Calm' else 0)
df['wind_speed'] = df['wind_speed'].map(lambda x: np.nan if x=='' else x)
df['wind_speed'] = df['wind_speed'].astype('float16')

#Scaling for numerical variables
df['humidity'] = df['humidity']/100
scaling_cols = ['temperature','heat_index','dew_point','pressure','visibility','wind_speed']
for col in scaling_cols:
    df[col] = df[col].map(lambda x: ((x - df[col].min())/(df[col].max() - df[col].min())))

#Label Encoding vs One hot encoding for categorical variables

# lst = df['wind_direction'].unique()
# direction = {}
# label = 1
# for d in lst:
#     direction[d] = label
#     label = label + 1
# df['wind_direction'] = df['wind_direction'].map(direction)

df = pd.get_dummies(df,columns=['wind_direction'])

df['target'] = df['conditions'].map(lambda x: 0 if 'rain' not in x.lower() else 1)
df['target'] = df['target'].astype('int8')


df.drop(['gust_speed','precipitation','events','conditions','time'],axis=1,inplace=True)

#heat_index has too many null
#print (df.isnull().sum())

df.drop('heat_index',axis=1,inplace=True)
df.dropna(inplace=True)

df.to_csv('train.csv',index=False)
