var video = document.querySelector("#video");
if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}
var resultb64 = "";
function capture() {
  var canvas = document.getElementById("canvas");
  var video = document.getElementById("video");
  canvas.width = 200;
  canvas.height = 200;
  canvas.getContext("2d").drawImage(video, 0, 0, 200, 200);
  resultb64 = canvas.toDataURL();
  return resultb64;
}

document.getElementById("upload").addEventListener("change", function () {
  var file = this.files[0];
  var reader = new FileReader();
  var canvas = document.getElementById("canvas");

  reader.onloadend = function (e) {
    resultb64 = reader.result;
    var img = new Image();
    img.onload = function () {
      canvas.width = 200;
      canvas.height = 200;
      canvas.getContext("2d").drawImage(img, 0, 0, 200, 200);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
});

document.getElementById("files").addEventListener("submit", async function (e) {
  e.preventDefault();
  var form = document.getElementById("files");
  var send = document.getElementById("photo_data");
  send.value = resultb64;
  var formData = new FormData(form);
  var c = await fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          res = data.photo;
          window.location.href = "/photo?p=" + res;
        });
      } else {
        throw new Error("Something went wrong ...");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
