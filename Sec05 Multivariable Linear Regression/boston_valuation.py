from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np

# Gather Data 

# from sklearn.datasets import load_boston
# boston_dataset = load_boston()
# data = pd.DataFrame(data=boston_dataset.data, columns=boston_dataset.feature_names) 


# Since the import above does not work:
# This is Boston Data
data = pd.read_csv('boston.csv')
log_prices = np.log(data['MEDV'])
features = data.drop(['INDUS','AGE','MEDV'], axis=1)

# Change log_prices shape to match features shape
target = pd.DataFrame({'PRICE':log_prices})

CRIME_IDX = 0
ZN_IDX = 1
CHAS_IDX = 2
RM_IDX = 4
PTRATIO_IDX = 8

ZILLOW_MEDIAN_PRICE = 583.3
SCALE_FACTOR = ZILLOW_MEDIAN_PRICE / np.median(np.e**target)

property_stats = features.mean().values.reshape(1,11) # Changes shape to 1,11 instead of a flat array


# Calculates theta values
regr = LinearRegression().fit(features.values, target.values)

# Calculates predicted or fitted values
fitted_vals = regr.predict(features.values)

# Calculates MSE and RMSE
MSE = mean_squared_error(target, fitted_vals) #Inputs correct target values , predicted values
RMSE = np.sqrt(MSE)

# Create a function which will estimate the log house prices for a specific prices
def get_log_estimate(nr_rooms,
                     students_per_classroom,
                     next_to_river=False,
                     high_confidence=True):
    # Configure property
    property_stats[0][RM_IDX] = nr_rooms
    property_stats[0][PTRATIO_IDX] = students_per_classroom

    if next_to_river:
        property_stats[0][CHAS_IDX] = 1
    else:
        property_stats[0][CHAS_IDX] = 0

    # Make prediction
    log_estimate = regr.predict(property_stats)[0][0] #Needs a single row of features

    # Calc Range
    
    #Wide Range - 2 std dev
    if high_confidence:
        upper_bound = log_estimate + 2*RMSE
        lower_bound = log_estimate - 2*RMSE
        interval = 95
    #Narrow Range - 1 std dev
    else:
        upper_bound = log_estimate + RMSE
        lower_bound = log_estimate - RMSE
        interval = 68

    return log_estimate, upper_bound, lower_bound, interval

def get_dollar_estimate(rm, ptratio, chas=False, large_range=True):
    """ Estimate the price of a property in Boston.  
    
    Keyword arguments:
    rm -- number of rooms in the property
    ptratio -- number of students per teacher in the classrom for the school in the area
    chas -- True if the property is next to the river, False otherwise
    large_range -- True for a 95% prediction interval, False for a 68% interval. 

    """
    if rm < 1 or ptratio < 1:
        print('Tha is unrealistic. Try again')
        return

    log_est, upper, lower, conf = get_log_estimate(rm, ptratio, next_to_river=chas, high_confidence=large_range)

    # Convert to today's dollars
    dollar_est = np.e**log_est * 1000 * SCALE_FACTOR
    dollar_hi = np.e**upper * 1000 * SCALE_FACTOR
    dollar_low = np.e**lower * 1000 * SCALE_FACTOR

    # Round the dollar values to nearest thousand
    rounded_est = np.around(dollar_est, -3)
    rounded_hi = np.around(dollar_hi, -3)
    rounded_low = np.around(dollar_low, -3)

    print(f'The estimated property value is {rounded_est}')
    print(f'At {conf}% confidence the valuation range is')
    print(f'USD {rounded_low} at the lower end to USD {rounded_hi} at the high end.')







