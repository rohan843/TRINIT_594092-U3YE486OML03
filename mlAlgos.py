# Core
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
sns.set(style='darkgrid', font_scale=1.4)
from imblearn.over_sampling import SMOTE
import itertools
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import time

# Sklearn
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score, f1_score
from sklearn.metrics import roc_auc_score, plot_confusion_matrix, plot_roc_curve, roc_curve
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.feature_selection import mutual_info_classif
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import eli5
from eli5.sklearn import PermutationImportance
from sklearn.utils import resample

# Models
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.naive_bayes import GaussianNB


files = ["/kaggle/input/crop-recommendation-dataset/Crop_recommendation.csv","/kaggle/input/rainfall-in-india/rainfall in india 1901-2015.csv","/kaggle/input/rainfall-in-india/district wise rainfall normal.csv"]
crop_recomendation_df=pd.read_csv(files[0])
district_wise_rainfall_df = pd.read_csv(files[2])
rainfall_in_india_df=pd.read_csv(files[1])

# crop_recomendation_df.head()

# crop_recomendation_df.info()

# crop_recomendation_df.describe()

# crop_recomendation_df.label.describe()

temp_df=pd.read_csv("/kaggle/input/crop-recommendation-dataset/Crop_recommendation.csv")

temp_df=pd.get_dummies(temp_df)
#temp_df.head()

temp_df = temp_df[['temperature', 'humidity', 'rainfall', 'label_apple', 'label_banana', 'label_blackgram', 'label_chickpea', 'label_coconut', 'label_coffee', 'label_cotton', 'label_grapes', 'label_jute', 'label_kidneybeans', 'label_lentil', 'label_maize', 'label_mango', 'label_mothbeans', 'label_mungbean', 'label_muskmelon', 'label_orange', 'label_papaya', 'label_pigeonpeas', 'label_pomegranate', 'label_rice', 'label_watermelon','N', 'P', 'K','ph']]

#temp_df.head()

# Models
#ToDO
N_model = DecisionTreeClassifier()
N_model.fit(temp_df.iloc[:,:-4].values,temp_df.iloc[:,-4].values)

#N_model.predict([[20.130175,81.604873262,2.717340,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]])

P_model = DecisionTreeClassifier()
P_model.fit(temp_df.iloc[:,:-4].values,temp_df.iloc[:,-3].values)
# P_model.predict([[20.130175,81.604873,2.717340,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]])

K_model = DecisionTreeClassifier()
K_model.fit(temp_df.iloc[:,:-4].values,temp_df.iloc[:,-2].values)

#K_model.predict([[20.130175,81.604873,2.717340,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]])


Ph_model = DecisionTreeRegressor()
Ph_model.fit(temp_df.iloc[:,:-4].values,temp_df.iloc[:,-1].values)
# Ph_model.predict([[20.130175,81.604873,2.717340,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]])

# sns.histplot(data=crop_recomendation_df, x="label")
# rainfall_in_india_df.head()
# rainfall_in_india_df.info()
rainfall_in_india_df=rainfall_in_india_df.dropna()
# rainfall_in_india_df.info()

def getValues(subdivision,month):
    df_new = rainfall_in_india_df[['SUBDIVISION',month,'YEAR']]
    df_new = df_new[df_new['SUBDIVISION']==subdivision]
    df_new = df_new.drop(['SUBDIVISION'],axis=1)
    final_list = df_new.values.tolist()
    return final_list

# getValues('ANDAMAN & NICOBAR ISLANDS','JAN') 
# district_wise_rainfall_df.head()  
# district_wise_rainfall_df.info()
# district_wise_rainfall_df.describe()

all_agriculture_price_df=pd.read_csv("/kaggle/input/all-agriculture-related-datasets-for-india/csv")
# all_agriculture_price_df.head()
# all_agriculture_price_df.info()
# all_agriculture_price_df.commodity.unique()
# s1=set([i.lower() for i in crop_recomendation_df.label.unique()])
# s2=set([i.lower() for i in all_agriculture_price_df.commodity.unique()])
# print(s1 & s2)

temp_df1=all_agriculture_price_df[['state','commodity','modal_price']]
# temp_df1.head()

def getDetails(state):
    df_new = temp_df1[temp_df1['state']==state]
    df_new = df_new.drop(['state'],axis=1)
    final_list = df_new.values.tolist()
    return final_list

#getDetails('Andaman and Nicobar')   

#Soil Details to crop
knn_model = KNeighborsClassifier()
knn_model.fit(crop_recomendation_df.iloc[:,:-1].values,crop_recomendation_df.iloc[:,-1].values)

#knn_model.predict([[95,42,43,20.879744,100.002744,6.502985,50.935536]])



    
    
    
