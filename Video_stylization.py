import os
import numpy as np
import cv2
import tensorflow as tf
import time
from style_transfer import Transfer


FLAGS = tf.compat.v1.flags.FLAGS
#tf.compat.v1.flags.DEFINE_string('gpu_index', '0', 'gpu index, default: 0') #Using GPU
tf.compat.v1.flags.DEFINE_string('checkpoint_dir', './style/africa',
                       'dir to read checkpoint in, default: ./style/africa')
tf.compat.v1.flags.DEFINE_string('in_path', None, 'input video path')
tf.compat.v1.flags.DEFINE_string('out_path', None, 'path to save processeced video to')
#only_check_args error 발생시 아래 활성화
#tf.compat.v1.flags.DEFINE_boolean('only_check_args', True, 'Set to true to validate args and exit.')


#afica / aquarelle / bango / chinese_style / hampson / udnie / wave
#la_muse / rain_princess / the_scream / the_shipwreck_of_the_minotaur

tf.compat.v1.reset_default_graph() 
tf.compat.v1.disable_eager_execution()


resize = cv2.resize
normalize = cv2.normalize
tfv1 = tf.compat.v1

cap = cv2.VideoCapture(FLAGS.in_path)
ret, frame = cap.read()

output_size_1 = int(frame.shape[1]/2)
output_size_0 = int(frame.shape[0]/2)


filename = FLAGS.out_path
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(filename, fourcc, 30, (output_size_1,output_size_0))



sess = tfv1.Session()
        
img_placeholder = tfv1.placeholder(tf.float32, shape=(None, output_size_0, output_size_1, 3))
        
model = Transfer()
pred = model(img_placeholder)
saver = tfv1.train.Saver()
        
ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
saver.restore(sess, ckpt.model_checkpoint_path)
    

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        frame_resize = resize(frame, dsize=(output_size_1,output_size_0), interpolation = cv2.INTER_AREA)
        _pred = sess.run(pred, feed_dict={img_placeholder:[frame_resize]})
        _pred = resize(np.squeeze(_pred, axis=0), dsize=(output_size_1,output_size_0), interpolation = cv2.INTER_LINEAR)
        _pred = normalize(_pred, _pred, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        _pred = cv2.cvtColor(_pred, cv2.COLOR_RGB2BGR)
        
        out.write(_pred)
    else:
        break
