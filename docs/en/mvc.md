# pyEchoNext / MVC Architecture

---

MVC stands for Model-View-Controller, an architectural pattern that divides an application into three logical components: the model, the View, and the controller.

The main idea of the MVC pattern is that each section of code has its own purpose. Part of the code contains application data, the other is responsible for how the user sees it, the latter controls its operation.

+ Model code **Model** stores data and associated logic, and anchors the structure of the application. That is, the programmer will determine the main components of the application using the template.
+ The application's appearance code, **View**, consists of functions that are responsible for the interface and how the user interacts with it. Views are created based on data collected from the model.
+ The controller code, **Controller**, links the model and view. It receives user input, interprets it and informs about the necessary changes. For example, sends commands to update state, such as saving a document.

---

[Contents](./index.md)


