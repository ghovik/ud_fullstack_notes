## 1 - Foundation

<iframe width="770" height="433" src="https://www.youtube.com/embed/fDe1k499NNk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### This course will cover

- Authentication systems - design, implementation, and use of third party services.
- Common vulnerabilities while working with passwords and how to avoid these pitfalls.
- Authorization systems - design and implementation for backend and frontend.
- Basic security best practices and key principals to keep in mind.

#### Prerequisite expectations

We expect that you have pre-existing knowledge in the following areas. We've included a few Recap concepts to help refresh your memory for this course.

- Basic frontend or backend implementation (e.g. Javascript/HTML/Python/Flask)
- Network communication (i.e., HTTP)
- Structured Query Language (SQL) using SQLAlchemy
- API Development (REST)

#### This course will *not* cover

- Advanced security principals.
- Penetration testing, red teaming, vulnerability detection.
- "Hacking" and tools and systems to perform nefarious actions.
- DevOps, Deployments, Scaling or maintaining these systems in the cloud



## 2 - Identity and Authentication

#### Authentication in the Digital World

<iframe width="770" height="433" src="https://www.youtube.com/embed/Y1X9yupVhG8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Common Authentication Methods

##### Username and Passwords

<iframe width="770" height="433" src="https://www.youtube.com/embed/Ccm4wie8qlA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Two status codes which are important throughout this course are:

- **401 Unauthorized**

  The client must pass authentication before access to this resource is granted. The server cannot validate the identity of the requested party.

- **403 Forbidden**

  The client does not have permission to access the resource. Unlike 401, the server knows who is making the request, but that requesting party has no authorization to access the resource.

#### Brief Intro to Problems with Passwords

<iframe width="770" height="433" src="https://www.youtube.com/embed/i2PQhJpb_OI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

As we discussed in the video, some issues with passwords are **outside of our control** as developers. Many issues come from user behavior that we cannot directly influence, such as:

- Users forget their passwords
- Users use simple passwords
- Users use common passwords
- Users repeat passwords
- Users share passwords

In contrast, some issues are **within our control** as developers:

- Passwords can be compromised
- Developers can incorrectly check
- Developers can cut corners

### Alternative Authentication Methods

#### Single Sign-On (SSO)

<iframe width="770" height="433" src="https://www.youtube.com/embed/BYSKdCi7hUg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Multi-Factor Authentication

<iframe width="770" height="433" src="https://www.youtube.com/embed/LbbOQBZgRlU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Passwordless

<iframe width="770" height="433" src="https://www.youtube.com/embed/OCSFMzd6SX0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Biometric Authentication

<iframe width="770" height="433" src="https://www.youtube.com/embed/gSm18eliZ1E" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Additional Readings:

- [Oath2](https://oauth.net/2/)
- [Auth0 Identity Providers](https://auth0.com/docs/identityproviders)
- [Google Identity Platform](https://developers.google.com/identity/)
- [Magic Links](https://hackernoon.com/magic-links-d680d410f8f7)
- [iOS Biometrics](https://developer.apple.com/documentation/localauthentication)
- [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_US)
- [Dance Dance Authentication](https://www.youtube.com/watch?v=VgC4b9K-gYU&feature=youtu.be) (Enjoy 😊)

### Third-Party Auth Systems

<iframe width="770" height="433" src="https://www.youtube.com/embed/BBkQ_9SSa88" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Common Auth Services:

- [Auth0](https://auth0.com/) (We'll be using this throughout the course!)
- [AWS Cognito](https://aws.amazon.com/cognito/)
- [Firebase Auth](https://firebase.google.com/docs/auth)
- [Okta](https://www.okta.com/)

### Implementing Auth0

Follow along with the set up at [Auth0.com](https://auth0.com/)!

<iframe width="770" height="433" src="https://www.youtube.com/embed/Mikr9g_JBaE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Using the Auth0 Authorization Code Flow with Hosted Login Pages

<iframe width="770" height="433" src="https://www.youtube.com/embed/_Fb0HKn0U2I" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Alternative Authentication Methods in Auth0

<iframe width="770" height="433" src="https://www.youtube.com/embed/ODZiEI2rJwA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### JSON Web Tokens (JWTs)

<iframe width="770" height="433" src="https://www.youtube.com/embed/6TWWT1W_4D4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### JWT - Data Structure

#### Parts of a JSON Web Token

<iframe width="770" height="433" src="https://www.youtube.com/embed/WRYsLYuvgoc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Including Data in Our JWT Payload

<iframe width="770" height="433" src="https://www.youtube.com/embed/rz7saqU8d8Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### JWT - Validation

#### Validating JWT Authenticity

<iframe width="770" height="433" src="https://www.youtube.com/embed/SoT_ETc35vs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

If the signature strings match, we can trust that the data within the JWT is authentic.

#### Additional Resources:

- [JWT.io](https://jwt.io/introduction/) a useful guide and list of popular JSON Web Token implementations.
- [Base64 Encoding](https://en.wikipedia.org/wiki/Base64)
- [HMAC](https://en.wikipedia.org/wiki/HMAC) keyed-hash message authentication code

### Storing Tokens in Web Browsers

<iframe width="770" height="433" src="https://www.youtube.com/embed/uOBGbP8B1yQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Storing JWTs

<iframe width="770" height="433" src="https://www.youtube.com/embed/WbDEQK3orJ0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```javascript
localStorage.getItem("token");
```

#### Security Considerations of Local Storage

<iframe width="770" height="433" src="https://www.youtube.com/embed/HANOhvWxXTI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### How Cross-Site Scripting Attacks (XSS) are Performed and Mitigated Techniques

<iframe width="770" height="433" src="https://www.youtube.com/embed/dL-Wc0ZEcIQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Sending Tokens with Requests

<iframe width="770" height="433" src="https://www.youtube.com/embed/kbBdD73lYTE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

