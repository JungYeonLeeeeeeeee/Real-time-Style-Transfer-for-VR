# Real-time-Style-Transfer-for-VR in [TensorFlow](https://github.com/tensorflow/tensorflow)
This repository is Tensorflow implementation of Johnson's [Perceptual Losses for Real-Time Style Transfer and Super-Resolution](https://arxiv.org/abs/1603.08155).

<p align="center">
<img src="https://user-images.githubusercontent.com/37034031/42068027-830719f4-7b84-11e8-9e87-088f1e476aab.png" width=800>
</p>
  
<p align="center">
<img src="https://user-images.githubusercontent.com/37034031/42068549-97588fc0-7b87-11e8-8110-93796a42a293.png" width=700>
</p>  

According to prior git, it takes 385ms on a GTX1080Ti to style the MIT Stata Center (1024x680).

It takes 600ms~800ms on a CPU (intel i5 7th) to style our web-cam (1024x720).

## Requirements
- tensorflow  2.1.0 or 1.8.0
- python 3.7  
- numpy 1.14.2
- flask 1.1.2

## Input & Output images / Style checkpoints
You can get inpu and output images in [my google drive](https://drive.google.com/drive/folders/1EI5ACLssZxw6sFah2Plt14tcv7Wckt3h?usp=sharing)

(That files are too large. So I upload that my google_drive. using it)

Download that files and place in the same path as the other files.

## Stylization VR demo
We are preapring a more good demo video. Please wait a little longer.

<p align = 'center'>
  <a href = "https://www.youtube.com/watch?v=NcNE-rb1Q1Q">
    <img src = "https://user-images.githubusercontent.com/44019436/94393586-5ce27800-0196-11eb-9bb6-54aed97e184a.gif">
  </a>
</p>

## Video Stylization
Here we transformed every frame in a video using some style images, then combined the results. [Click to go to the full demo on YouTube!](https://youtu.be/O61LawvhjOc)
<p align = 'center'>
  <a href = 'https://www.youtube.com/watch?v=O61LawvhjOc'>
    <img src = 'https://user-images.githubusercontent.com/44019436/94394865-53a6da80-0199-11eb-863b-28a2680426ad.gif'>
  </a>
</p>


We don't use GPU, so it is really slow to convert full video to style. Thus we makes a short and little styls's demo.
If you want to see more styles and results, then see the privous git, [ChengBinJin](https://github.com/ChengBinJin/Real-time-style-transfer). That's demo is this.
<p align = 'center'>
  <a href = 'https://www.youtube.com/watch?v=HpKMLA19zkg&feature=youtu.be'>
    <img src = 'https://user-images.githubusercontent.com/37034031/42082312-9ffdbffc-7bc2-11e8-9dfe-e505e5b3c528.gif'>
  </a>
</p>

## Image Stylization
A photo of Coffee was applied for various style paintings. Click on the ./output/P folder to see full applied style images.

<p align="center">
<img src=https://user-images.githubusercontent.com/44019436/95039125-e51ecb00-070a-11eb-9f3a-1e34203aa4e2.png>
</p>

## Implementation Details
Implementation uses TensorFlow to train a real-time style transfer network. Same transformation network is used as described in Johnson, except that batch normalization is replaced with Ulyanov's instance normalization, zero padding is replaced by reflected padding to reduce boundary artifacts, and the scaling/offset of the output `tanh` layer is slightly different.  

We follow  [Logan Engstrom](https://github.com/lengstrom/fast-style-transfer) to use a loss function close to the one described in Gatys, using VGG19 instead of VGG16 and typically using "shallower" layers than in Johson's implementation (e.g. `relu1_1` is used rather than `relu1_2`).

VR need real-time response. Thus we try to use interpolation, which reduce original image to half size and recover to original size. It's one of a trick to increase speed (naturally it reduce a little of quality). If your CPU and GPU has great spec, then delete the part of interpolation is more good to your project.



## Documentation
### Stylizing Video
Use `Video_stylization.py` to transfer style into a video. Example usage:
```
python Video_stylization.py --checkpoint_dir style/africa --in_path input/M/0.mp4 --out_path output/output.mp4
```
- `--checkpoint_dir`: dir to read checkpoint in, default: `./checkpoints/africa`  
- `--in_path`: input video path, default: `None`
- `--out_path`: path to save processed video to, default: `None`


### Stylizing Video VR
#### - Using a web-cam
If you using a web-cam in your computer then use `VR_main.py` to transfer. Example usage:
```
python VR_main.py --checkpoint_dir style/africa
```
- `--checkpoint_dir`: dir to read checkpoint in, default: `./checkpoints/africa`  



#### - Using your phone or other device
If you want to using it with your phone or other device, then you need your own web-site or ngrok.

It is more slow then using web-cam. Without doubt, it's speed depended on your Internet condition. (about 2s-7s).

With ngrok, it takes 2sec from google-colab, and 5~6sec from jupyter-notebook.

Go to a path "for_VR", then run `ngrok` first in your terminal.
```
ngrok http 5000
```
then you can see the screen like this
```
Session Status                online
Session Expires               7 hours, 57 minutes
Version                       2.3.35
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://365a81c4b5ff.ngrok.io -> http://localhost:5000
Forwarding                    https://365a81c4b5ff.ngrok.io -> http://localhost:5000 

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00            
```

`https://365a81c4b5ff.ngrok.io` this part is your URL. After that, open the other terminal and run `server.py`. 

```
python server.py
```
Enter your URL+'/transfer'. (For example. `https://365a81c4b5ff.ngrok.io/transfer`)


### Others
We uses already trained and evaluated model. We don't touch anything of [prior git](https://github.com/ChengBinJin/Real-time-style-transfer)

If you want to train more style and evaluated your model, then use to [prior git](https://github.com/ChengBinJin/Real-time-style-transfer)

### Attributions/Thanks
- This project borrowed some code from [Cheng-Bin Jin](https://github.com/ChengBinJin/Real-time-style-transfer), [Logan Engstrom](https://github.com/lengstrom/fast-style-transfer) and Anish's [Neural Style](https://github.com/anishathalye/neural-style/)
- Make a web server got help and borrowed some code [webrtcHacks](from https://webrtchacks.com/webrtc-cv-tensorflow/)
- Some readme formatting was borrowed from [Logan Engstrom](https://github.com/lengstrom/fast-style-transfer)
- The image of the MIT Stata Center at the very beginning of the README was taken by [Juan Paulo](https://juanpaulo.me/)

## License
Copyright (c) 2020 JungYeonLeeeeeeeee and Lee-Jaehu. Contact me for commercial use (or rather any use that is not academic research) (email: snszmsk@naver.com / lghgohafs@naver.com). Free for research use, as long as proper attribution is given and this copyright notice is retained.
