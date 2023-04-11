window.addEventListener('load', function() {

    // Adding event listener to the submit button
    document.getElementById('submit').addEventListener('click', function(event) {
        console.log("submit button clicked")
        event.preventDefault();
        const img = document.getElementById('img');
        const img_out = document.getElementById('img_out');
        if (img.files && img.files[0]) {
            img.onload = () => {
                URL.revokeObjectURL(img.src);  // no longer needed, free memory
            }
            // Set up reader and call async read function
            const reader = new FileReader();
            reader.readAsDataURL(img.files[0]);
            // Wait for data to load, and then call blur request and set image
            reader.addEventListener('load', (e) => {

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
                    response.text().then(function(body) {
                        console.log("BODY: ", body); // this will be a string
                        img_out.src = "data:image/png;base64, " + body
                      }
                    )
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            })            
        }
    });

    // Adding event listener to img loads
    document.getElementById('img').addEventListener('change', function() {
        document.getElementById('in_img_1').src = URL.createObjectURL(document.getElementById('img').files[0]); 
    })
    document.getElementById('img2').addEventListener('change', function() {
        document.getElementById('in_img_2').src = URL.createObjectURL(document.getElementById('img2').files[0]); 
    })
    document.getElementById('t_img1').addEventListener('change', function() {
        document.getElementById('in_img_3').src = URL.createObjectURL(document.getElementById('t_img1').files[0]); 
    })
    document.getElementById('t_img2').addEventListener('change', function() {
        document.getElementById('in_img_4').src = URL.createObjectURL(document.getElementById('t_img2').files[0]); 
    })
});

