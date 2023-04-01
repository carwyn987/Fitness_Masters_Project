import { make_gaussian_blur_request } from './requests.js';

window.addEventListener('load', function() {
    document.querySelector('input[type="file"]').addEventListener('change', function() {
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
                const data = e.target.result;
                console.log(data)

                var blurred_image = make_gaussian_blur_request(data)
                img.src = URL.createObjectURL(this.files[0]); // set src to blob url
            })            
        }
    });
});