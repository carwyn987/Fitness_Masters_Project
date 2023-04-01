import express from 'express'

// Initialise Express
var app = express()
// Render static files
app.use(express.static('public'))

// need to add app.use() - for server

// Port website will run on
app.listen(8080)