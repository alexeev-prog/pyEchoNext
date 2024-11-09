# pyEchoNext / web frameworks device

---

The most important parts of web frameworks are:

+ Routing handlers:
- Simple: `/index`
- Parameterized: `/article/{article_id}`
+ Request handlers (views, handlers).

Basic requirement: the web framework must be supported by a fast, lightweight and efficient server (eg gunicorn). Python has a WSGI guide for this.

## Web server design in Python

```
REQUEST
CLIENT <--------------> [HTTP (80) or HTTPS (443)] Server
ANSWER

> Application with logic
> Data conversion for a python application <-- Web framework's area of interest (ensuring gunicorn works with it)
> Gunicorn
> Converted data
SERVER -> NGINX
> Data routing
```

When developing a web application in python, we encounter the following problems:

+ Many frameworks (ex. django) do not know how to route response requests.
+ Applications are insecure and may be susceptible to DDoS (Distributed Denial of Service) attacks.
+ No load balancing between multiple servers.
+ NGINX solves the problem of load balancing, but it cannot run and communicate with Python applications.

Therefore, there is a need to use a WSGI server (Web Server Gateway Interface) and a proxy server (such as NGINX).

## WSGI
Python currently boasts a wide range of web application frameworks such as Zope, Quixote, Webware, SkunkWeb, PSO and Twisted Web, just to name a few. This wide variety of options can be a challenge for new Python users, as typically their choice of web framework will limit their choice of web servers to use, and vice versa.

In contrast, although Java has as many web application frameworks available, Java's "servlet" API allows applications written with any Java web application framework to run on any web server that supports the servlet API.

The availability and widespread use of such APIs in web servers for Python—whether those servers are written in Python (e.g., Medusa), built-in Python (e.g., mod_python), or call Python through a gateway protocol (e.g., CGI, FastCGI, and etc.) - will separate framework selection from web server selection, allowing users to choose the pairing that suits them, while freeing up framework and server developers to focus on their preferred area specializations.

Thus, this PEP offers a simple and universal interface between web servers and web applications or frameworks: the Python Web Server Gateway Interface (WSGI).

But the mere existence of the WSGI specification does nothing to address the current state of Python web application servers and frameworks. Authors and maintainers of servers and frameworks must actually implement WSGI for it to have any effect.

However, since no existing server or framework supports WSGI, an author who implements WSGI support will not receive immediate rewards. Thus, WSGI must be easy to implement so that the author's initial investment in the interface can be fairly low.

Thus, ease of implementation on both the server side and the interface framework side is absolutely critical to the usefulness of a WSGI interface and is therefore a primary criterion for any design decisions.

However, it should be noted that ease of implementation for a framework author is not the same as ease of use for a web application author. WSGI provides a completely "no frills" interface for the framework author, because bells and whistles like response objects and cookie handling would simply prevent existing frameworks from solving these problems. Again, the goal of WSGI is to facilitate simple interoperability between existing servers and applications or frameworks, not to create a new web framework.

It should also be noted that this target does not allow WSGI to require anything that is not already available in deployed versions of Python. Therefore, new standard library modules are not proposed or required by this specification, and nothing in WSGI requires a Python version greater than 2.2.2. (However, it would be nice if future versions of Python included support for this interface in the web servers provided by the standard library.)

In addition to being easy to implement for existing and future frameworks and servers, it should also be easy to create request preprocessors, response postprocessors, and other WSGI-based "middleware" components that look like an application to its containing server, while also acting as a server to its contained applications. If middleware can be both simple and reliable, and WSGI is widely available in servers and frameworks, this allows for the possibility of an entirely new type of Python web application framework: consisting of loosely coupled WSGI middleware components. Indeed, existing framework authors may even choose to refactor their frameworks' existing services so that they are exposed in a way that becomes more like the libraries used with WSGI and less like monolithic frameworks. This would then allow application developers to select "best-of-breed" components for a specific functionality, rather than committing to all the pros and cons of a single framework.

Of course, as of this writing, that day is undoubtedly quite far away. At the same time, this is a sufficient short-term goal for WSGI to enable the use of any framework with any server.

Finally, it should be mentioned that the current version of WSGI does not prescribe any specific mechanism for "deploying" an application for use with a web server or server gateway. Currently, this is necessarily determined by the server or gateway implementation. Once enough servers and frameworks have implemented WSGI to provide hands-on experience with various deployment requirements, it may make sense to create another PEP describing

## Integer pyEchoNext
pyEchoNext is a universal tool with the ability to make a monolithic web application, or vice versa, a modular web application. Django was too big and clumsy for us, flask or fastapi was too small. Therefore, we decided to take some features from django and flask/fastapi, combine them and make it all symbiotic. So that you can make a large monolithic project or a small service. And turning a small service into a large application or vice versa required a minimum of effort.

Our goals were also to make all this as clear as possible, developer-friendly, and add the ability to integrate third-party libraries.

As a result, the main characteristics of the project are as follows:

1. Goal: Create a universal multi-faceted web framework in python
2. Tasks:
+ Find the good and bad sides of Flask, FastAPI
+ Find the good and bad sides of Django
+ Compare the capabilities of existing frameworks
+ Selection of the best features
+ Symbiosis of features into one whole
+ Build project code according to SOLID and OOP principles, easily extensible, scalable and complementary.
+ Make the code fast and productive, give freedom to the user and developer
3. Problem: at the moment there are very few universal frameworks that allow you to create both a large monolithic application and a fast small service.
4. Relevance: the web sphere is very popular at the moment, the ability to work with web frameworks, abstractions, and know the structure of sites will help everyone.

---

[Contents](./index.md)
