
let mediaRecorder;
let audioChunks = [];

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      audioChunks = [];

      mediaRecorder.addEventListener("dataavailable", event => {
        audioChunks.push(event.data);
      });

      mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("audio", audioBlob);

        fetch("/voice", {
          method: "POST",
          body: formData
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("transcriptBox").innerText = `🧍 You: ${data.transcript}`;
          document.getElementById("responseBox").innerText = `🤖 VitalAssist: ${data.response}`;
          document.getElementById("audioPlayer").src = data.audio;
          document.getElementById("audioPlayer").play();
        })
        .catch(error => {
          alert("Voice processing failed. Please try again.");
          console.error("Voice error:", error);
        });
      });
    })
    .catch(err => {
      alert("Microphone access denied.");
      console.error("Mic error:", err);
    });
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}
