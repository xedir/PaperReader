
#%%
import pandas as pd
phrases = pd.read_csv("phrases.csv", encoding='utf-8')
phrases.to_csv("example.csv",encoding='utf-8', index=None, header=1)
phrases.columns