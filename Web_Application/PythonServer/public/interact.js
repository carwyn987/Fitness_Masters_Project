import { sendImgs } from './comm.js'

window.addEventListener('load', function() {
    // Adding event listener to the submit button
    document.getElementById('submit').addEventListener('click', function(event) {
        console.log("submit button clicked")
        event.preventDefault();
        const img = document.getElementById('img');
        
        if (img.files && img.files[0]) {
            img.onload = () => {
                URL.revokeObjectURL(img.src);  // no longer needed, free memory
            }
            // Set up reader and call async read function
            const reader = new FileReader();
            reader.readAsDataURL(img.files[0]);
            // Wait for data to load, and then call blur request and set image
            reader.addEventListener('load', (e) => {
                const img_out = document.getElementById('img_out');
                sendImgs(img_out)
            })            
        }else{
            alert("Missing image 1! Submission cancelled.")
            return
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

