import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor

crop_recomendation_df = pd.read_csv('data/crop_recommendation.csv')
rainfall_levels_df = pd.read_csv('data/rainfall_levels.csv')
agriculture_price_df = pd.read_csv('data/agriculture_price.csv')

# N, P, K, pH

tmp_crop_recs_df = pd.get_dummies(crop_recomendation_df)[['temperature', 'humidity', 'label_apple',
       'label_banana', 'label_coconut', 'label_cotton', 'label_grapes',
       'label_jute', 'label_maize', 'label_mango', 'label_orange',
       'label_papaya', 'label_pomegranate', 'label_rice', 'N', 'P', 'K', 'ph']]

models = {
    'N': DecisionTreeRegressor().fit(tmp_crop_recs_df.iloc[:, :-4].values, tmp_crop_recs_df.iloc[:, -4].values),
    'P': DecisionTreeRegressor().fit(tmp_crop_recs_df.iloc[:, :-4].values, tmp_crop_recs_df.iloc[:, -3].values),
    'K': DecisionTreeRegressor().fit(tmp_crop_recs_df.iloc[:, :-4].values, tmp_crop_recs_df.iloc[:, -2].values),
    'pH': DecisionTreeRegressor().fit(tmp_crop_recs_df.iloc[:, :-4].values, tmp_crop_recs_df.iloc[:, -1].values)
}

def toBinary(prop):
    return 1 if prop else 0
    
def getOneHotEncodedVector(crop):
    return [toBinary('apple' == crop),
       toBinary('banana' == crop), toBinary('coconut' == crop), toBinary('cotton' == crop), toBinary('grapes' == crop),
       toBinary('jute' == crop), toBinary('maize' == crop), toBinary('mango' == crop), toBinary('orange' == crop),
       toBinary('papaya' == crop), toBinary('pomegranate' == crop), toBinary('rice' == crop)]

# [temperature, humidity] + getOneHotEncodedVector(crop)
# models['N'].predict([tmp_crop_recs_df.iloc[0, :-4].values])[0]

# Rainfall Levels

# months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
def getRainfallLevelValues(state, month):
    return [tuple(i) for i in rainfall_levels_df[rainfall_levels_df['state'] == state][[month, 'YEAR']].values]

# State based Price of Items

def getStateBasedItemPrices(state):
    return [tuple(i) for i in agriculture_price_df[agriculture_price_df['state'] == state][['label', 'modal_price']].values]

# Crop Recommendation based on Soil

crop_recommender_model = KNeighborsClassifier().fit(crop_recomendation_df.iloc[:, :-1].values, crop_recomendation_df.iloc[:, -1].values)

# [N, P, K, temperature, humidity, ph]
# crop_recommender_model.predict([crop_recomendation_df.iloc[0, :-1].values])[0]