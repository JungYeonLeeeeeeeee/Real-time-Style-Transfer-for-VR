//Get camera video
const constraints = {
    audio: false,
    video: {
        width: {min: 320, ideal: 640, max: 960},
        height: {min: 360, ideal: 720, max: 1080}
    }
};

navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        document.getElementById("frame_source").srcObject = stream;
        console.log("Got local user video");

    })
    .catch(err => {
        console.log('navigator.getUserMedia error: ', err)
    });
