---
title: Using Graph Databases for Low Latency Routing in the Starlink Satellite Network
description: Using Memgraph DB to find optimal routes in satellite networks
authors: Team Tolkien
---

# Using Graph Databases for Low Latency Routing in the Starlink Satellite Network
## Introduction
Providing worldwide broadband internet is a popular problem **SpaceX** is currently pursuing with their **Starlink** project. The plan is to send thousands of satellites into Earth’s orbit which will provide thorough space coverage, as well as low latency transmission. 

Low latency transmission is a key factor when trying to deliver high-speed internet access. It doesn’t depend solely on the data transfer rate, but also on the transmission route itself, which is supposed to be as short as possible. In other words, the shorter the path the data needs to travel, the faster the internet connection.

Finding the shortest path between locations is a common problem tackled by graph theory, so the ideal approach to the transmission routing problem would be to use graph concepts and algorithms. 

In this post, we will explore how graph analytics and graph theory can be used to model the Starlink constellation and optimize transmission paths to ensure high-speed internet access almost anywhere on the planet. You can also visit our [**Starlink Simulator**](http://starlink.memgraph.com/) and see the results for yourself.
<br /><br />
<p align="center">
   <img src="https://raw.githubusercontent.com/g-despot/images/699ee65713223a90af3f5b180f331893b2c469be/demo_screenshot.png" alt="" width="800"/>
<p/>
<br />

## What is *Starlink*?

Starlink is a satellite constellation being built by SpaceX to provide satellite Internet access. The constellation will consist of thousands of mass-produced small satellites in low Earth orbit (LEO) (altitudes below 2000 km). The goal of the Starlink project is to provide satellite internet connectivity to underserved areas of the planet. The project started in 2015 and 597 satellites have been launched into orbit so far. By the end of the project, SpaceX wants to build a “shell“ around the Earth consisting of over 4,000 communication satellites which will use phased array antennas for communication with ground relays in combination with laser communication technology to provide **global low-latency high bandwidth coverage**.<br /><br />
In the first phase, 1,584 satellites will be deployed at an altitude of 550 km and 2,825 satellites will be added in the second phase at three different altitudes to increase density and coverage to as far as 70° North/South. For our simulation, we used 480 satellites in 24 orbital planes at an altitude of around 550 km and an inclination of 70.0°. These parameters make our simulation much more visually understandable but also result in a lack of visible satellites from time to time. In our simulation, each satellite is connected to 4 more satellites. Two of them are in the same orbit while the other two satellites are located in neighbouring orbits.
<br /><br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/satellite_connection.png?raw=true" alt="" width="500"/>
<p/>
<br />

## Satellites vs Fiber Optics

Compared to optical fibre, the transmission speed in space is around **1.47 times higher** than in glass optical cables. With the increased transmission speed, free-space laser link speeds could reach rates of 100 Gb/s or even higher. Even though it's hard to predict the network capacity, the most important aspect of transmission is latency. Latency doesn't seem as big of a problem on small distances, but it increases the further we travel through an optic cable. In theory, internet traffic via geostationary satellites has a latency of at least 477 ms. In practice, that number is closer to 600 ms. Being in lower orbits, Starlink satellites will offer more practical latencies of around 25 to 35 ms. The latency of light travelling through a cable is 49 ms per kilometre, compared to 33.3 ms per kilometre when it’s travelling through a vacuum. For example, the latency between New York and London via fiber optic is around 59 ms, while, in theory, it should be around 40 ms using Starlink.

The exact latency using Starlink is still a mystery because it’s not publicly available information. We had to make some assumptions on our part to make the simulation more realistic. 
We also approximate the signal processing time for satellites and ground transceivers, which are fixed and set to 10 and 12 ms respectively. For example, a signal travelling from city A to city B via 2 satellites will result in 64 ms of processing time in total. The ground transceivers in both cities will contribute 12 ms of processing time each while the satellites will contribute 20 ms of processing time (10 ms to process the received signal and 10 ms for further transmission processing).
<br /><br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/starlink_satellite.jpg?raw=true" alt="" width="500"/>
<p/>
<br />

Why is low-latency so important? Starlink is designed to support near real-time access to rapidly changing data. Primarily, the system is advertised as a way to offer global internet coverage. Not only will this system provide better connections in underdeveloped countries, but it will also target other areas like the financial market. Currently, the privately-owned *Hibernia Express* cable offers the lowest latency transmission between New York and London with up to 58.95 ms which is 39.4% slower than a potential Starlink connection. The benefits of a Starlink connection would be even more pronounced for longer routes like London to Singapour. With millions of dollars being moved in fractions of a second, having lower latencies would provide a massive advantage in capitalizing on these price swings.

How to find low-latency routes? This whole model and dataset can be represented as a **graph problem**. If we tackle the problem as such, we can use methods from **graph theory** to calculate and find the path with the lowest latency.

## Graph Databases in Satellite Networks

So how exactly does graph theory step into this story? Let’s look at the nature of the problem. We have some satellites and lasers that transmit data between them. We could easily model this scenario with nodes (vertices) and relationships (edges), where the nodes represent the satellites and the relationships represent the laser connections between them. The same notion is applied to cities and radio connections between cities and satellites.

This simple concept is the basis of graph theory where the main object of interest is a graph, which is nothing more than a structure composed of nodes and relationships. We give these nodes and relationships labels and properties so we can model real-world problems with more credibility. Nodes are objects or entities with certain attributes, just like in the classic relational database model, while relationships are connections between nodes that can also hold information such as the nature and gravity of the connection. Here’s what our data model looks like:
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/starlink_model.png?raw=true" alt="" width="400"/>
<p/>
<br />

These relationships are what separate the graph database model from the relational database model. They enable flexible data manipulation and are a strong argument against the rigid foreign key assignment that the relational model uses.

If you want to learn more about the advantages of the graph database model, feel free to check out this blog post: [Why Your Business Should Use a Graph Database]( https://memgraph.com/blog/why-your-business-should-use-a-graph-database). 

Finally, when the graph structure is implemented, as well as all the rules related to orbital mechanics, the **Starlink Network Simulator** gives us a proper overview of the project. You can choose pairs of cities and run the simulation to see the shortest transmission path generated between them, as well as the transmission time needed in comparison to the fibre-optic cable.

## Exploring *Starlink* with Cypher Queries

To play around with our dataset just visit [**Memgraph Lab**](https://lab.memgraph.com/) and login with the following credentials:
* **Username:**  userReadonly
* **Password:**  starlinkreadit
* **Host:** 34.248.115.177
* **Port:** 9000<br />

This account only has *read permissions* so don't worry about messing anything up. We are going to show you how to use **openCypher** queries to retrieve interesting results from our data.
Let's start by writing a very simple query that returns all the nodes with the same label. In our example, we are going to return all the nodes with the label `City`.<br />
This is achieved by executing the following query:
```
   MATCH (c:City) RETURN c;
```
The output should be:
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/cities.png?raw=true" alt="" width="600"/>
<p/>
<br />

On the other hand, if you want to return all the nodes with the label `Satellite` you only need to make a small change:
```
   MATCH (s:Satellite) RETURN s;
```
Now we can try out something more interesting. Let's return all the satellites that are visible from *London*. To be more specific, we are returning all the relationships of type `VISIBLE_FROM` that a node with the label `City` and with the property `name` equal to *London* has.<br /> 
The query looks like this:
```
   MATCH (c:City {name: "London"})
   -[r:VISIBLE_FROM]-(n) RETURN c, r, n;
```
The output should be:
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/london_visible_from.png?raw=true" alt="" width="600"/>
<p/>
<br />

If we wanted to return all the relationships a satellite has, we would need to specify if they are of type `VISIBLE_FROM` or `CONNECTED_TO` because the former represents connections between cities and satellites, while the latter only represents connections between satellites. We are just going to omit the relationship type in our query so both of these types are returned.<br /> 
The query looks like this: 
```
   MATCH (s:Satellite {id: "482"})
        -[r]-(n) RETURN s, r, n;
```
The output should be:
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/satellite_id_482.png?raw=true" alt="" width="500"/>
<p/>
<br />

If we wanted to return only relationships of type `CONNECTED_TO`, the query would have been:
```
   MATCH (s:Satellite {id: "482"})
        -[r:CONNECTED_TO]-(n) RETURN s, r, n;
```
The same result can be achieved by specifying the label of the second node instead of the relationship type:
```
   MATCH (s:Satellite {id: "482"})
        -[r]-(n: Satellite) RETURN s, r, n;
```
Both queries have the same output: 
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/satellite_id_482_connected_to.png?raw=true" alt="" width="500"/>
<p/>
<br />

## Using Dijkstra’s Algorithm to Find the Shortest Transmission Path

The most important aspect of a satellite network is the transmission time from one point to another. Given that the satellites are in constant movement, their visibility from cities is therefore changing. The network needs to be able to calculate the shortest path exceedingly fast and efficiently in real-time with these changes in mind. This is where **Memgraph DB** comes in handy. 

One way to find such a path would be to run the following query:

```
   MATCH p=(:City { name: "New York"})
      -[*wShortest (e, n | e.transmission_time) total_transmission_time]-
      (:City { name: "London"})
   RETURN nodes(p) as path, total_transmission_time;
```
The returned path has the smallest possible sum of individual transmission times, i.e. the shortest path for data transmission. This query returns paths that can also include nodes with the label `City` and relationships of type `VISIBLE_FROM` if their use could lower the overall transmission time.<br />
The same logic could be applied for using ground relay stations that would aid in the transmission process. While this is also an interesting tactic that could be explored, it is not part of our initial problem definition so we will gloss over it for now. 

To fix this problem, we need to add the following query segment: 

```
   WHERE ALL(x IN nodes(p)[1..-1] WHERE (x:Satellite))
```
to ensure that the returned path only contains nodes with the label `Satellite`.<br />
The final query would look like this:
```
   MATCH p=(:City { name: "New York"})
      -[*wShortest (e, n | e.transmission_time) total_transmission_time]-
      (:City { name: "London"})
   WHERE ALL(x IN nodes(p)[1..-1] WHERE (x:Satellite))
   RETURN nodes(p) as path, total_transmission_time;
```

To get a visual representation of the path in **Memgraph Lab**, you would need to return the found path and exclude the variable `total_transmission_time`. The query should be:
```
   MATCH p=(:City { name: "New York"})
       -[*wShortest (e, n | e.transmission_time) total_transmission_time]-
       (:City { name: "London"}) 
   WHERE ALL(x IN nodes(p)[1..-1] WHERE (x:Satellite))
   RETURN p;
```
The resulting graph should look like this:
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/london_new_york.png?raw=true" alt="" width="500"/>
<p/>
<br />

## Memgraph and other Real-World Applications

As we have shown in this example, **Memgraph DB** can be used to solve a complicated problem relatively easily and many other problems can be tackled similarly. Routing packets across mesh networks, supply chain analysis and [optimal route planning](https://memgraph.com/blog/how-to-build-a-route-planning-application-with-breadth-first-search-and-dijkstras-algorithm) are only a few of the numerous examples that are waiting to be explored with this technology. You can also try out [**Memgraph Cloud**](https://cloud.memgraph.com/login) for free and see if a graph database would be a good fit for your specific personal or business requirements.<br />
Don't forget to visit the [**Starlink Simulator**](http://starlink.memgraph.com/) if you want to see the satellite network in action or [**Memgraph Lab**](https://lab.memgraph.com/) to play around with the live simulation data.
