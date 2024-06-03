document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault();
  
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
  
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
  
      try {
        const response = await fetch('https://choice-cheetah-rested.ngrok-free.app/detect_plate/', {
          method: 'POST',
          body: formData
        });
  
        if (response.ok) {
          const data = await response.json();
          document.getElementById('plateNumber').textContent = data.plate;
        } else {
          console.error('Error:', response.statusText);
          const errorText = await response.text();
          console.error('Response Text:', errorText);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  });
  
  document.getElementById('getDataButton').addEventListener('click', async function () {
    try {
      const response = await fetch('https://choice-cheetah-rested.ngrok-free.app/detect_plate/', {
        method: 'GET'
      });
  
      if (response.ok) {
        const data = await response.json();
        document.getElementById('getResponse').textContent = JSON.stringify(data);
      } else {
        console.error('Error:', response.statusText);
        const errorText = await response.text();
        console.error('Response Text:', errorText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });
  