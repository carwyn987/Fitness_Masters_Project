import { make_gaussian_blur_request } from './requests.js';

window.addEventListener('load', function() {
    document.querySelector('input[type="file"]').addEventListener('change', function(event) {
        event.preventDefault();
        if (this.files && this.files[0]) {
            var img = document.querySelector('img');
            img.onload = () => {
                URL.revokeObjectURL(img.src);  // no longer needed, free memory
            }
            // Set up reader and call async read function
            const reader = new FileReader();
            reader.readAsDataURL(this.files[0]);
            // Wait for data to load, and then call blur request and set image
            reader.addEventListener('load', (e) => {
                img.src = URL.createObjectURL(this.files[0]); // set src to blob url

                const formData = new FormData();
                const fileInput = document.querySelector('#img');
                formData.append('image', fileInput.files[0]);

                // make the fetch request with streaming
                fetch('/upload-image', {
                    method: 'POST',
                    body: formData,
                    // Set the "onUploadProgress" callback to track the upload progress "onUploadProgress" will be called multiple times during the upload with the "event" object containing the "loaded" and "total" properties
                    stream: true,
                    onUploadProgress: function(event) {
                        const progress = (event.loaded / event.total) * 100;
                        console.log(`Upload progress: ${progress.toFixed(2)}%`);
                    }
                })
                .then(response => {
                    console.log('Server response:', response);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            })            
        }
    });
});