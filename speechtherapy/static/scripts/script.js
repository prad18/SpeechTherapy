// script.js
const recordButton = document.getElementById('recordButton');
const scoreDisplay = document.getElementById('scoreDisplay');
const wordDisplay = document.getElementById('wordDisplay');

let mediaRecorder;
let audioChunks = [];

recordButton.addEventListener('click', async () => {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.addEventListener('dataavailable', (event) => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener('stop', async () => {
      const audioBlob = new Blob(audioChunks);
      const audioFile = new File([audioBlob], 'audio.wav', { type: 'audio/wav' });
      const formData = new FormData();
      const word = wordDisplay.textContent; // Get the word from the wordDisplay element

      formData.append('audio_file', audioFile);
      formData.append('word', word);

      // Add CSRF token to formData
      const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
      formData.append('csrfmiddlewaretoken', csrfToken);

      // Send the FormData object to the server using the POST method to /learn/ URL
      try {
        const response = await fetch('/learn/', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();

        if (response.ok) {
          scoreDisplay.textContent = `Pronunciation correctness: ${data.similarity_score}%`;
        } else {
          scoreDisplay.textContent = `Error: ${data.error}`;
        }
      } catch (error) {
        console.error('Error sending audio data:', error);
        scoreDisplay.textContent = `Error: ${error.message}`;
      }
    });

    mediaRecorder.start();
    console.log('Recording started');
    recordButton.textContent = 'Stop Recording'; // Change button text to indicate recording is ongoing
  } else if (mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    console.log('Recording stopped');
    recordButton.textContent = 'Record'; // Change button text back to original
  }
});
