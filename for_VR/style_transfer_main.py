import os
import six.moves.urllib as urllib
import json
import numpy as np
import tensorflow as tf
import cv2

from style_transfer import Transfer

tf.compat.v1.reset_default_graph() 
tf.compat.v1.disable_eager_execution()

#afica / aquarelle / bango / chinese_style / hampson / udnie / wave
#la_muse / rain_princess / the_scream / the_shipwreck_of_the_minotaur
checkpoint_dir = '../style/udnie'

tfv1 = tf.compat.v1
resize = cv2.resize
normalize = cv2.normalize


soft_config = tfv1.ConfigProto(allow_soft_placement=True)
soft_config.gpu_options.allow_growth = True

sess = tfv1.Session(config=soft_config)
#with g.as_default(), g.device('/device:GPU:0'), tfv1.Session(config=soft_config) as sess:

#sess = tfv1.Session()


img_placeholder = tfv1.placeholder(tf.float32, shape=(None, 360, 320, 3))
        
model = Transfer()
pred = model(img_placeholder)
saver = tfv1.train.Saver()
        
ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
saver.restore(sess, ckpt.model_checkpoint_path)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


# Helper code
def load_image_into_numpy_array(frame):
    (im_width, im_height) = frame.size
    return np.array(frame.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def start_style_trasnfer(frame):
    frame_data = load_image_into_numpy_array(frame)

    frame_resize = resize(frame_data, dsize=(320,360), interpolation = cv2.INTER_AREA)

    _pred = sess.run(pred, feed_dict={img_placeholder:[frame_resize]})
    #_pred = resize(np.squeeze(_pred, axis=0), dsize=(640,720), interpolation = cv2.INTER_LINEAR)
    _pred = np.squeeze(_pred, axis=0)
    result = normalize(_pred, _pred, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

  
    outputJson = json.dumps(result, cls=NpEncoder)

    return outputJson