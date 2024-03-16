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
      console.log('Recording stopped');

      const audioBlob = new Blob(audioChunks);
      const audioFile = new File([audioBlob], 'audio.wav', { type: 'audio/wav' });
      const formData = new FormData();
      console.log('Word displayed:', wordDisplay.textContent);
      const word = wordDisplay.textContent; // Get the word from the wordDisplay element
      const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

      formData.append('audio_file', audioFile);
      formData.append('word', word);
      formData.append('csrfmiddlewaretoken', csrfToken);

      // Print formData to check if it contains the correct data
      console.log('FormData:', formData);

      try {
        const response = await fetch('/learn/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Print data to check if it contains the correct information
        console.log('Response data:', data);

        // Update the scoreDisplay element with the correctness percentage
        scoreDisplay.textContent = `Pronunciation correctness: ${data.similarity_score}%`;

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
