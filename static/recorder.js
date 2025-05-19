// static/recorder.js
let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'voice.wav');

        const res = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        document.getElementById("transcriptBox").innerText = data.transcript;
        document.getElementById("responseBox").innerText = data.response;
        document.getElementById("audioPlayer").src = data.audio;
        document.getElementById("audioPlayer").play();
    };

    mediaRecorder.start();
    console.log("🎙️ Recording started...");
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        console.log("🛑 Recording stopped.");
    }
}
