function make_request(){
    const http = new XMLHttpRequest()

    http.open("GET", "http://127.0.0.1:5683/")
    http.send()

    http.onload = () => alert(http.responseText)
}