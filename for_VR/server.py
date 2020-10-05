import style_transfer_main
import os
from PIL import Image
from flask import Flask, request, Response

app = Flask(__name__)

# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST') # Put any other methods you need here
    return response


@app.route('/')
def index():
    return Response('Tensor Flow Style Transfer VR')


@app.route('/transfer')
def transfer():
  return Response(open('./static/transfer.html').read(), mimetype="text/html")


@app.route('/frame', methods=['POST'])
def frame():
  try:
        Frame_file = request.files['frame']  # get the image
        
        frame_object = Image.open(Frame_file).convert('RGB')
        objects = style_transfer_main.start_style_trasnfer(frame_object)
        return objects

  except Exception as e:
        print('POST /image error: %e' % e)
        return e



if __name__ == '__main__':
	# without SSL
    app.run(debug=True, host='0.0.0.0')#'127.0.0.1') #SSL 할 수 있으면 해보기

	# with SSL
    #app.run(debug=True, host='0.0.0.0', ssl_context=('ssl/server.crt', 'ssl/server.key'))
