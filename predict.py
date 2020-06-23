
import combine
import sys 
import cartoon
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import tensorflow as tf
import numpy as np
import os,glob,cv2
from os import walk,path
import sys,argparse
def predict():
	curr_folder = path.dirname(path.realpath(__file__))
# First, pass the path of the image
#	for (dirpath, dirnames, filenames) in walk(curr_folder):
#		for name in filenames:
#			if (name.endswith('jpg')):
#				photo=(dirpath+'/'+name)
	photo='opencv0.jpg'
	image_size=128
	num_channels=3
	images = []
# Reading the image using OpenCV
	image = cv2.imread(photo)
# Resizing the image to our desired size and preprocessing will be done exactly as done during training
	image = cv2.resize(image, (image_size, image_size),0,0, cv2.INTER_LINEAR)
	images.append(image)
	images = np.array(images, dtype=np.uint8)
	images = images.astype('float32')
	images = np.multiply(images, 1.0/255.0) 
 #The input to the network is of shape [None image_size image_size num_channels]. Hence we reshape.
	x_batch = images.reshape(1, image_size,image_size,num_channels)

## Let us restore the saved model 
	sess = tf.Session()
# Step-1: Recreate the network graph. At this step only graph is created.
	saver = tf.train.import_meta_graph('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\created.meta')
# Step-2: Now let's load the weights saved using the restore method.
	saver.restore(sess, tf.train.latest_checkpoint('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV'))

# Accessing the default graph which we have restored
	graph = tf.get_default_graph()

# Now, let's get hold of the op that we can be processed to get the output.
# In the original network y_pred is the tensor that is the prediction of the network
	y_pred = graph.get_tensor_by_name("y_pred:0")

## Let's feed the images to the input placeholders
	x= graph.get_tensor_by_name("x:0") 
	y_true = graph.get_tensor_by_name("y_true:0") 
	y_test_images = np.zeros((1, 3)) 


### Creating the feed_dict that is required to be fed to calculate y_pred 
	feed_dict_testing = {x: x_batch, y_true: y_test_images}
	result=sess.run(y_pred, feed_dict=feed_dict_testing)
# result is of this format [probabiliy_of_rose probability_of_sunflower]
	cartoon.create()
	emo=0
	print(result)
	print('happy', result.item(0))
	print('sad', result.item(1))
	print('surprise', result.item(2))

	if result.item(0)>.5:
		print('happy')
		emo=1
	elif result.item(1)>.5:
		print('sad')
		emo=2
	elif result.item(2)>.5:
		print('surprise')
		emo=3
	print(emo)
	return emo
if __name__ == "__main__":
 	predict()
