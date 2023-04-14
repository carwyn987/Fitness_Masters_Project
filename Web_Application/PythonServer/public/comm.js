import { move } from './progress_bar.js'

function sendImgs(img_out){
    const formData = new FormData();

    // Add image data
    const fileInput = document.querySelector('#img');
    formData.append('image', fileInput.files[0]);

    const fileInput2 = document.querySelector('#img2');
    formData.append('image2', fileInput2.files[0]);

    const fileInput3 = document.querySelector('#t_img1');
    formData.append('t_img1', fileInput3.files[0]);

    const fileInput4 = document.querySelector('#t_img2');
    formData.append('t_img2', fileInput4.files[0]);

    // Ensure all images are there:
    // Note that fileInput or file1 is taken care of in interact.js
    if(fileInput2.value == fileInput2.defaultValue){
        alert("Missing image 2! Submission cancelled.")
        return
    }
    if(fileInput3.value == fileInput3.defaultValue){
        alert("Missing thermal image 1! Submission cancelled.")
        return
    }
    if(fileInput4.value == fileInput4.defaultValue){
        alert("Missing thermal image 2! Submission cancelled.")
        return
    }

    move()

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
        response.text().then(function(body) {
            console.log("BODY: ", body); // this will be a string
            img_out.src = "data:image/png;base64, " + body
            }
        )
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

export { sendImgs }