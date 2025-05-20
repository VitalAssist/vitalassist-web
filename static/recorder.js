let mediaRecorder;
let audioChunks = [];

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      audioChunks = [];
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      reader.onloadend = () => {
        const base64data = reader.result;
        console.log("Audio Base64:", base64data);
        // Send base64 to backend or handle it
        alert("Audio captured and ready.");
      };
    };

    mediaRecorder.start();
    alert("🎙 Recording started.");
  } catch (err) {
    alert("Voice recording failed: " + err.message);
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
    alert("🛑 Recording stopped.");
  } else {
    alert("No recording is in progress.");
  }
}
