from keras import models, layers
from keras import optimizers
import numpy as np

def build_model(train_data):
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(3, activation='sigmoid'))   #标量回归
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    # model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss='mse', metrics=['mae'])
    return model

#k折验证训练
def k_train_data(train_data,train_targets,model):
	k=4
	num_epochs = 1
	all_mae_histories = []
	num_val_samples = len(train_data) // k  #k个分区，每个分区多少数据
	for i in range(k):
		print('processing fold #', i)
		val_data = train_data[i * num_val_samples: (i+1) * num_val_samples]
		val_targets = train_targets[i * num_val_samples: (i+1) * num_val_samples]
		partial_train_data = np.concatenate([train_data[:i * num_val_samples], train_data[(i+1) * num_val_samples:]], axis = 0)
		partial_train_targets = np.concatenate([train_targets[:i * num_val_samples], train_targets[(i+1) * num_val_samples:]], axis = 0)

		model.fit(partial_train_data, partial_train_targets, validation_data=(val_data, val_targets), epochs=num_epochs, batch_size=1)
	return model