Starlink Demo
===
This demo application simulates and visualizes the Starlink internet constellation. It also demonstrates how **MemgraphDB** can be used to find the shortest routing path in such networks.<br />
To find out more about the subject, read the accompanying [blog post](https://github.com/memgraph/starlink/blob/develop_web/blog-post/blog-post.md).

<br />
<p align="center">
   <img src="https://raw.githubusercontent.com/g-despot/images/699ee65713223a90af3f5b180f331893b2c469be/demo_screenshot.png" alt="" width="800"/>
<p/>
<br />

## Prerequisites

Before you can run the application, you need to have the following tools installed:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

After you installed Docker you need to download the [Memgraph image](https://memgraph.com/download) for Docker and [load it](https://docs.memgraph.com/memgraph/quick-start#docker-installation).<br />
The container with the image should be stopped before attempting to build and run the app.

## Start the app

First, position yourself in the root folder of the project. Build the Docker image and run the application with the following commands:
```
docker-compose build
docker-compose up
```
If everything was successful you can open it in your browser. The app will be listening on: http://localhost:5001/. 

## Project structure

The app is divided into three separate modules:
* **memgraph** - the database where all the positions of satellites and cities are stored and updated. 
* **simulator** - a Python program that utilizes the Skyfield package to calculate satellite positions in orbit. Those positions are then stored in the Memgraph database.
* **web_app** - a client-server app that fetches data from the database and renders it.

## Technologies used

* Python 3.7
* MemgraphDB 2.2.1
* Apache Kafka
* Poetry
* Skyfield
* Flask
* Leaflet
