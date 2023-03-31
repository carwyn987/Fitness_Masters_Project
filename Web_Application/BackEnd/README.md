# RESTFul API Review:

### Source:
 - https://realpython.com/api-integration-in-python/

 REST - Representational State Transfer. A software style that defines a pattern for client and server communcation over network.

 Constraints:
 - Stateless - server will not contain any persistent state between client requests (i.e. one and done).
 - Client-Server - Decoupled nature.
 - Cacheable - Data retreived should be cacheable either by the client or the server.
 - Uniform Interface
 - Layered System
 - Code on Demand (Optional) - Code provided from the server to the client for it to run locally.

What is HTTP?
 - From source https://realpython.com/python-https/#what-is-http 
 - HTTP stands for HyperText Transfer Protocol
 - Basic steps:
   - Browser is told by user to go to a web address
   - A TCP connection is setup between the browser and the server
   - An HTTP request is sent to the server
   - Server handles request
   - Server sends back a response
   - User receives message, parses, and continues
 - HTTP Requests contain:
  - A method - such as GET, POST, ...
  - A path or target - indicates which webpage is being requested to the server
  - A version number of HTTP
  - Headers - connection information
  - The body - other info
 - The response includes similar information, documented at the link below. This includes a status number.
 - https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages 

A few of the main HTTP methods:
 - GET - Retreive a resource
 - POST - Create a resource
 - PUT - Update a resource
 - DELETE - Delete a resource

HTTP Response Codes:
 - 200 - Okay
 - 201 - Created
 - 202 - Accepted, no modification yet
 - 400 - Bad request
 - 415 - Unsupported media type
 - 500 - Server error