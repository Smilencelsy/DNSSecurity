#coding=utf-8
import numpy as np
import tensorflow as tf 
testset=[]
saver = tf.train.import_meta_graph('models/nn_model.ckpt.meta')

#计算前向传播结果
def inference(input_tensor, avg_class, weights1, biases1, weights2, biases2, weights3, biases3):
    if avg_class == None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biases1)
        layer2 = tf.nn.relu(tf.matmul(layer1, weights2) + biases2)
        return tf.matmul(layer2, weights3) + biases3

    else:  
        layer1 = tf.nn.relu(tf.matmul(input_tensor, avg_class.average(weights1)) + avg_class.average(biases1))
        layer2 = tf.nn.relu(tf.matmul(layer1, avg_class.average(weights2)) + avg_class.average(biases2))
        return tf.matmul(layer2, avg_class.average(weights3)) + avg_class.average(biases3)


import pickle
def evaluate(t):
	with tf.Session() as sess:
		tf.global_variables_initializer().run()
		#读取TensorFlow模型
		saver.restore(sess,'models/nn_model.ckpt')
		#从模型中读取权重
		weights1=tf.get_default_graph().get_tensor_by_name("Variable/read:0")
		biases1=tf.get_default_graph().get_tensor_by_name("Variable_1/read:0")
		weights2=tf.get_default_graph().get_tensor_by_name("Variable_2/read:0")
		biases2=tf.get_default_graph().get_tensor_by_name("Variable_3/read:0")
		weights3=tf.get_default_graph().get_tensor_by_name("Variable_4/read:0")
		biases3=tf.get_default_graph().get_tensor_by_name("Variable_5/read:0")
		testset=np.array([t])

		testset=np.array(testset,dtype='float32')
		#计算前向传播结果
		average_y =  sess.run(inference(testset, None,weights1, biases1, weights2, biases2, weights3, biases3))
		argmax = sess.run(tf.argmax(average_y, 1))
		return argmax[0]