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
                response.text().then(body => {
                    console.log(body)

                    const byteArray = new Uint8Array(body.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
                    const arrayBuffer = new ArrayBuffer(byteArray.length);
                    const bufferView = new Uint8Array(arrayBuffer);
                    bufferView.set(byteArray);

                    // Create a new DataView object to read the JFIF data
                    const jfifDataView = new DataView(arrayBuffer);

                    // Check that the data starts with the JFIF header
                    if (jfifDataView.getUint16(0, false) !== 0xffd8 || jfifDataView.getUint16(2, false) !== 0xffe0 || jfifDataView.getUint8(4) !== 0x4a || jfifDataView.getUint8(5) !== 0x46 || jfifDataView.getUint8(6) !== 0x49 || jfifDataView.getUint8(7) !== 0x46 || jfifDataView.getUint8(8) !== 0x00) {
                    console.error('Input data is not a valid JFIF file');
                    return;
                    }

                    // Extract the JPEG data from the JFIF file
                    const jpegData = body.slice(20);

                    // Save the JPEG data to a new file with the ".jpg" extension
                    const blob = new Blob([jpegData], {type: 'image/jpeg'});
                    const url = URL.createObjectURL(blob);
                    img.src = url

                    // var imgsrc = "data:image/jpg;base64," + btoa(body)
                    // img.src = imgsrc

                    console.log(fileInput.src)
                });
                
                })
                .catch(error => {
                // handle the error
                console.error('Error:', error);
                });
            })            
        }
    });
});