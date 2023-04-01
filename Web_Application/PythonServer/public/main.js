// // create a new FormData object
// const formData = new FormData();

// // get a reference to the file input element
// const fileInput = document.querySelector('input[type="file"]');

// // add the file to the FormData object
// formData.append('image', fileInput.files[0]);

// // make the fetch request with streaming
// fetch('/upload-image', {
//   method: 'POST',
//   body: formData,
//   headers: {
//     'Content-Type': 'multipart/form-data'
//   },
//   // use the "stream" option to enable streaming
//   // and set the "onUploadProgress" callback to track the upload progress
//   // "onUploadProgress" will be called multiple times during the upload
//   // with the "event" object containing the "loaded" and "total" properties
//   // which can be used to calculate the progress percentage
//   // note that the "stream" option may not be supported by all servers
//   // and may require server-side configuration
//   // consult your server documentation for details
//   stream: true,
//   onUploadProgress: function(event) {
//     const progress = (event.loaded / event.total) * 100;
//     console.log(`Upload progress: ${progress.toFixed(2)}%`);
//   }
// })
// .then(response => {
//   // handle the server response
//   console.log('Server response:', response);
// })
// .catch(error => {
//   // handle the error
//   console.error('Error:', error);
// });