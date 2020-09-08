## 1 - Introduction to APIs

#### Course Topics:

- APIs: What, Why, How
- Handling HTTP Requests
- Routing and API Endpoints
- Documentation
- Testing

#### Technologies

- Flask
- Flask-CORS
- SQLAlchemy
- JSONify
- Unittest



### What are APIs?

Some frequently used APIs include:

- [Google Maps API](https://developers.google.com/maps/documentation/)
- [Stripe API](https://stripe.com/docs/api?utm_source=zapier.com&utm_medium=referral&utm_campaign=zapier&utm_source=zapier.com&utm_medium=referral&utm_campaign=zapier)
- [Facebook API](https://developers.facebook.com/docs)
- [Instagram API](https://www.instagram.com/developer/)
- [Spotify API](https://developer.spotify.com/documentation/web-api/)



### How APIs Work

<iframe width="770" height="433" src="https://www.youtube.com/embed/sYZ7QWCbqF4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Internet Protocols (IPs)

Internet Protocol (IP) is the protocol for sending data from one computer to another across the internet.

### RESTful APIs

<iframe width="770" height="433" src="https://www.youtube.com/embed/A8MSvJs02IA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**REST** stands for **Representational State Transfer**.

Here's a short summary of the REST principles:

- **Uniform Interface**: Every rest architecture must have a standardized way of accessing and processing data resources. This include unique resource identifiers (i.e., unique URLs) and self-descriptive messages in the server response that describe how to process the representation (for instance JSON vs XML) of the data resource.
- **Stateless**: Every client request is self-contained in that the server doesn't need to store any application data in order to make subsequent requests
- **Client-Server**: There must be both a client and server in the architecture
- **Cacheable & Layered System**: Caching and layering increases networking efficiency



## HTTP and Flask Basics

### Introduction to HTTP

<iframe width="770" height="433" src="https://www.youtube.com/embed/rtYY2NvDMWE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Features

- **Connectionless:** When a request is sent, the client opens the connection; once a response is received, the client closes the connection. The client and server only maintain a connection during the response and request. Future responses are made on a new connection.
- **Stateless:** There is no dependency between successive requests.
- **Not Sessionless:** Utilizing headers and cookies, sessions can be created to allow each HTTP request to share the same context.
- **Media Independent:** Any type of data can be sent over HTTP as long as both the client and server know how to handle the data format. In our case, we'll use JSON.



#### Elements

- Universal Resource Identifiers (URIs):

  An example URI is

  ```
  http://www.example.com/tasks/term=homework
  ```

- It has certain components:

  - **Scheme:** specifies the protocol used to access the resource, HTTP or HTTPS. In our example `http`.
  - **Host:** specifies the host that holds the resources. In our example `www.example.com`.
  - **Path:** specifies the specific resource being requested. In our example, `/tasks`.
  - **Query:** an optional component, the query string provides information the resource can use for some purpose such as a search parameter. In our example, `/term=homework`.git status

### HTTP Requests

<iframe width="770" height="433" src="https://www.youtube.com/embed/5EUHUzia0bw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### HTTP request methods

<iframe width="770" height="433" src="https://www.youtube.com/embed/zuUwIf90dmU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### HTTP Responses

<iframe width="770" height="433" src="https://www.youtube.com/embed/sfDwGi8CF4Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Creating a basic Flask application