#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow import keras as k
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.layers.core import Dense, Dropout
from joblib import dump

#%%
data = pd.read_csv('data.csv')
data.head()
data = data.drop(['filename'],axis=1)

genre_list = data.iloc[:, -1]
convertor = LabelEncoder()
y = convertor.fit_transform(genre_list)
# %%
fit = StandardScaler()
X = fit.fit_transform(np.array(data.iloc[:, :-1], dtype = np.float64))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

# %%
def trainModel(model, epochs, optimizer):
    batch_size = 32
    model.compile(optimizer = optimizer,
                  loss = 'sparse_categorical_crossentropy',
                  metrics = 'accuracy',
    )
    return model.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = epochs,
                    batch_size = batch_size, shuffle = True)

def plotValidate(history):
    print("Validation Accuracy", max(history.history["val_accuracy"]))
    pd.DataFrame(history.history).plot(figsize=(12,6))
    plt.show()

model = k.models.Sequential([

    Dense(512, activation = 'relu', input_shape = (X_train.shape[1],), kernel_initializer=k.initializers.RandomNormal(stddev=0.01)),
    Dropout(0.3),

    Dense(256, activation = 'relu'),
    Dropout(0.3),

    Dense(128, activation = 'relu'),
    Dropout(0.3),

    Dense(64, activation = 'relu'),
    Dropout(0.3),

    Dense(10, activation = 'softmax'),

])
print(model.summary())
model_history = trainModel(model = model, epochs = 500, optimizer='adam')
#%%
plotValidate(model_history)
# %%
model.save('./model/')
dump(fit, './model/std_scaler.bin', compress = True)
