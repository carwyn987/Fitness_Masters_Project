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
                // const data = e.target.result;
                // console.log(data)
                // var blurred_image = make_gaussian_blur_request(data)
                img.src = URL.createObjectURL(this.files[0]); // set src to blob url

                //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                // create a new FormData object
                const formData = new FormData();

                // get a reference to the file input element
                // const fileInput = document.querySelector('input[type="file"]');
                const fileInput = document.querySelector('#img');

                // add the file to the FormData object
                formData.append('image', fileInput.files[0]);

                // make the fetch request with streaming
                fetch('/upload-image', {
                method: 'POST',
                body: formData,
                // headers: {
                //     'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryLq85t7aGlb6IzEMP'
                // }, # This is similar to problems many people have when coming from less useful HTTP libraries. However, the documentation is very clear about how to post multipart files. Otherwise, all we could reasonably do is have a general note that says "Please stop providing your own headers, requests can do it by itself". https://github.com/psf/requests/issues/1997
                // use the "stream" option to enable streaming
                // and set the "onUploadProgress" callback to track the upload progress
                // "onUploadProgress" will be called multiple times during the upload
                // with the "event" object containing the "loaded" and "total" properties
                // which can be used to calculate the progress percentage
                // note that the "stream" option may not be supported by all servers
                // and may require server-side configuration
                // consult your server documentation for details
                stream: true,
                onUploadProgress: function(event) {
                    const progress = (event.loaded / event.total) * 100;
                    console.log(`Upload progress: ${progress.toFixed(2)}%`);
                }
                })
                .then(response => {
                // handle the server response
                console.log('Server response:', response);
                })
                .catch(error => {
                // handle the error
                console.error('Error:', error);
                });
                // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            })            
        }
    });
});