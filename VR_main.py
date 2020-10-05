import os
import numpy as np
import cv2
import tensorflow as tf
import time
from style_transfer import Transfer


FLAGS = tf.compat.v1.flags.FLAGS
tf.compat.v1.flags.DEFINE_string('checkpoint_dir', './style/africa',
                       'dir to read checkpoint in, default: ./style/africa')


tf.compat.v1.reset_default_graph() 

checkpoint_dir = FLAGS.checkpoint_dir
tf.compat.v1.disable_eager_execution()


resize = cv2.resize
normalize = cv2.normalize
tfv1 = tf.compat.v1 #for tensorflow 2.x if you use tensorflow 1.x then delete this line and replace tfv1 to tf

cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
cap.set(3,640)
cap.set(4,720)


sess = tfv1.Session()
        
img_placeholder = tfv1.placeholder(tf.float32, shape=(None, 360, 320, 3))
        
model = Transfer()
pred = model(img_placeholder)
saver = tfv1.train.Saver()
        
ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
saver.restore(sess, ckpt.model_checkpoint_path)


while(True):
    ret, frame = cap.read()
    start = time.time()
    
    frame_resize = resize(frame, dsize=(320,360), interpolation = cv2.INTER_AREA)
    
    _pred = sess.run(pred, feed_dict={img_placeholder:[frame_resize]})
    

    _pred = resize(np.squeeze(_pred, axis=0), dsize=(640,720), interpolation = cv2.INTER_LINEAR)
    _pred = normalize(_pred, _pred, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    _pred = cv2.cvtColor(_pred, cv2.COLOR_RGB2BGR)
    numpy_horizontal = np.hstack((_pred, _pred))
    

    cv2.imshow('filtered', numpy_horizontal)
    
    print("time :", time.time() - start)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sess.close()
        break
        
cap.release()
cv2.destroyAllWindows()
