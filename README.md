                                    #+TITLE: One Stop Shop
#+AUTHOR: SriHarsha,Anirudh,Aashish,Sameeranah
#+SETUPFILE: ../../org-templates/level-2.org
#+EXCLUDE_TAGS: boilerplate
#+PROPERTY: session *python*
#+PROPERTY: results output
#+PROPERTY: exports code
#+TAGS: boilerplate(b) notes(n) solution(s)


* Introduction
** Purpose
This Document is an overall description of the project. It throws light on how to setup this in =user interface= and use it.
It also gives us a clear idea about the =database tables= that we maintaned. 

** About Project
We have implemented a =one stop shop= application.This app can be used as as platfor for selling and buying products of different categories.
We used =flask-sqlalchemy= for databases,=python= for backend and =javascript= for frontend

** Requirements to run this application
One has to install all python modules mentioned in the requirements.txt for running this app.

** Steps to run the application

#+NAME: steps
#+BEGIN_SRC
Go to the app directory.Next You have to create database tables for storing information required by our app.This can be done by entering python interpreter.Type python in terminal an press enter.Then in python interpreter execute command =from app import db=,then execute command =db.create_all()=.Now our required database tables are created.
Now execute command =python app.py= in the terminal.
The server is hosted on '127.0.0.1' port = 5000
#+END_SRC

* code structure

Directory structure for our web application
#+NAME: structure
#+BEGIN_SRC
.
├── app.py
├── app.pyc
|
├── Documentation
|
├── requirements.txt
├── static
│   ├── dashboard.css
│   ├── form.css
│   ├── myscripts1.js
│   ├── myscripts3.js
│   ├── myscripts.js
│   ├── script.js
│   ├── signin.css
│   ├── starter-template.css
│   └── style.css
└── templates
    ├── cart.html
    ├── complete.html
    ├── dashboard.html
    ├── dash.html
    ├── dassh.html
    ├── details1.html
    ├── details2.html
    ├── details3.html
    ├── details.html
    ├── history.html
    ├── in1.html
    ├── inde.html
    ├── index.html
    ├── ind.html
    ├── in.html
    ├── lay.html
    ├── login.html
    ├── signup.html
    └── upload.html
#+END_SRC

* Security
  Our web application is CSRF protected.

* Functionalities
 Functionalities of our web application are given below
** =Login=
  A User can have an account through which he can buy or sell products.For buying or Selling products account must be mandatory.A User acn login into his/her account through password and username. 

** =Register=
 A New User can register to the one stop shop by providing username and emailId,and password.

** Non-user view
 If a user is not logged In,they can see various categories of products available for buying,various products available under each category,details of the product like price,name,seller,description,product rating,seller rating,time for delivery,method for delivery etc.
  He/She will not able to buy or sell product if not logged In

** Logged In User View
 If a user is logged In,he/she can see various categories of products available for buying,various products available under each category,details of the product like price,name,seller,description,product rating,seller rating,time for delivery,method for delivery etc which are same above non-user view.
 In addition to above he/she can upload details of the products to be sold by them.one can rate any product,buy any product,rate the seller of the product,comment on the product.

** =selling a product=
  To sell a product using One stop Shop one should be a user of the one stop shop.one can upload image of the product to be sold,details like price,description,time of delivery,method of delivery,no of items available etc.

** =Buying a product= 
  One can add any number of products to the cart and can be able to buy the products or cancel them without buying.

** =Cart=
  One can view cart elements using cart button.Their will options like buy and cancel in the cart

** =History=
  One can view their history of purchages in this view.Their will be a option clear history which wil clear the history of the user.

** =ProductRating=
  User can rate the product in the profile page of the product.One user can rate a particular product only once.

** =SellerRating=
  User can rate a seller only when the user has bought any product sold by that seller.User can rate the seller by going to history page clicking on the product.Now details of the product appear and User can rate the seller.

** =Comments=
 User can comment on the product in the profile page of the product.Comments will be displayed in the profile page of the product along the name of the User who commented.

These are the functionalities of our web application.

This project is done during spring 2017
