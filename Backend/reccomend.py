"""
Copyright David Suh, 2024. 

Given two dataframes of spotify songs (a history and a candidate list), we
return the best candidate possible. 
"""

import pandas as pd

from sklearn.neighbors import KDTree

def feats(df: pd.DataFrame) -> pd.DataFrame:
    df = df.select_dtypes(float).drop(columns=['tempo'])
    df = (df - df.mean()) / df.std()

    return df


def get_recommends(hist: pd.DataFrame, cand: pd.DataFrame) -> pd.DataFrame: 
    kd = KDTree(feats(hist))

    dists, idxs = kd.query(feats(cand), k=10)
    cand = pd.concat([cand,
                      pd.Series(dists.sum(axis=1)).rename('dst_sum')], 
                      axis=1)
    cand = cand.sort_values('dst_sum')

    return cand.iloc[:10]
