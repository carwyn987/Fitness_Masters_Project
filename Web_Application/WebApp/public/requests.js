function make_request(){
    const http = new XMLHttpRequest()

    http.open("GET", "http://127.0.0.1:5683/")
    http.send()

    http.onload = () => alert(http.responseText)
}

/*
img_data - base64 encoded image
*/
function make_gaussian_blur_request(img_data){
    // https://stackoverflow.com/questions/15001822/sending-large-image-data-over-http-in-node-js

    const param = "image=" + img_data
    const http = new XMLHttpRequest()
    http.open("GET", "http://127.0.0.1:5683/gaussian" + "?" + param)
    http.send()
    http.onload = () => alert(http.responseText)
}

export { make_gaussian_blur_request }