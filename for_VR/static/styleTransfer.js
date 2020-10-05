/*
 * Client side of Tensor Flow Style transfer Web API
 * Written by JungYeonLeeeeeeeee, based on code from webrtcHacks - https://webrtchacks.com
 */

//import "./static/gpu.js";

//Parameters
const s = document.getElementById('styleTransfer');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const mirror = s.getAttribute("data-mirror") || false; //mirror the boundary boxes
const apiServer = s.getAttribute("data-apiServer") || window.location.origin + '/frame'; //the full TensorFlow Object Detection API server url

//Video element selector
v = document.getElementById(sourceVideo);

//for starting events
let isPlaying = false,
    gotMetadata = false;

//Canvas setup

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d", { alpha: false });

//create a canvas for drawing object boundaries
let drawCanvas = document.createElement('canvas');
document.body.appendChild(drawCanvas);
let drawCtx = drawCanvas.getContext("2d", { alpha: false });
//const offscreen = drawCanvas.transferControlToOffscreen();


function clearCanvas() {
  //clear the previous drawings
  drawCtx.clearRect(0, 0, window.innerWidth, window.innerHeight);
  drawCtx.beginPath();

}

//Add file blob to a form and post
function postFile(file) {

    //Set options as form data
    let formdata = new FormData();
    formdata.append('frame', file);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiServer, true);
    xhr.onload = function () {
        if (this.status === 200) {
            let objects = JSON.parse(this.response); 

            clearCanvas();
            
            var r,g,b;
            var oc = document.createElement('canvas'),
                octx = oc.getContext('2d', { alpha: false });
            

            for (var i = 0; i < objects.length; i++) {

              for (var j = 0; j < objects[0].length; j++) {
                
                r = objects[i][j][0];
                g = objects[i][j][1];
                b = objects[i][j][2];
                octx.fillStyle = "rgba(" + r + "," + g + "," + b + ", 1)";
                octx.fillRect(j, i, 1, 1);
              }
            }
            drawCtx.translate(window.innerWidth/40, 0);
            drawCtx.drawImage(oc, 0, 0, oc.width*(39/40), oc.height, 0, 0, window.innerWidth, window.innerHeight);
            drawCtx.translate(window.innerWidth/2, 0);
            drawCtx.drawImage(oc, oc.width*(3/40), 0, oc.width, oc.height, 0, 0, window.innerWidth, window.innerHeight);
            drawCtx.translate(-window.innerWidth*21/40, 0);        

            //Save and send the next image
            imageCtx.drawImage(v, 0, 0, 640, 720);
            imageCanvas.toBlob(postFile, 'frame/jpeg');
        }
        else {
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}


//Start style tansfer
function startStyleTransfer() {

    console.log("starting style transfer");

    //Set canvas sizes base don input video
    drawCanvas.width = window.innerWidth;
    drawCanvas.height =  window.innerHeight;

    imageCanvas.width = 640;
    imageCanvas.height = 720;
    
    //Save and send the first image
    imageCtx.drawImage(v, 0, 0, 640, 720);
    imageCanvas.toBlob(postFile, 'frame/jpeg');

}

//Starting events

//check if metadata is ready - we need the video size
v.onloadedmetadata = () => {
    console.log("video metadata ready");
    gotMetadata = true;
    if (isPlaying)
        startStyleTransfer();
};

//see if the video has started playing
v.onplaying = () => {
    console.log("video playing");
    isPlaying = true;
    if (gotMetadata) {
        startStyleTransfer();
    }
};