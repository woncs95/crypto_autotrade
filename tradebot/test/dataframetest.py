import pandas as pd

dic1={'best':1,'b':2,'c':3}
dic2={'best':4,'b':5,'c':6}
dic3={'best':7,'b':8,'c':9}

dic={'dic1':dic1,'dic2':dic2,'dic3':dic3}
df=pd.DataFrame(dic)
dics=df['dic1']['best']
#print(dics['best'])

#print(df[dic1]['a'])
