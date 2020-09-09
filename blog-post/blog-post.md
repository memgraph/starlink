---
title: Low Latency Routing in the *Starlink* Satellite Network
description: 
authors: Team Tolkien
---

# Low Latency Routing in the *Starlink* Satellite Network
## Introduction
Providing worldwide broadband internet is a popular problem **SpaceX** is currently pursuing with their ***Starlink*** project. The plan is to send thousands of satellites into Earth’s orbit which will provide thorough space coverage, as well as low latency transmission. 

Low latency transmission is a key factor when trying to deliver high speed internet access. It doesn’t depend solely on satellite laser performances, but also on the transmission route itself, which is supposed to be as short as possible. In other words, the shorter the path the laser beam needs to travel, the faster the internet connection.

Finding the **shortest path** between locations is a common problem tackled by graph theory, so the ideal approach to the transmission speed problem would be to use graph concepts and algorithms. 

In this tutorial, we will explore how graph analytics and graph theory can be used to model the *Starlink* constellation and optimize transmission paths to ensure high speed internet access anywhere on the planet. 
<br />
<p align="center">
   <img src="https://raw.githubusercontent.com/g-despot/images/699ee65713223a90af3f5b180f331893b2c469be/demo_screenshot.png" alt="" width="800"/>
<p/>
<br />

## What is *Starlink*?

*Starlink* is a satellite constellation being constructed by SpaceX to provide **satellite Internet access**. The constellation will consist of thousands of mass-produced small satellites in low Earth orbit (LEO) (altitudes of 2000 km). The goal of *Starlink* project is to provide satellite internet connectivity to underserved areas of the planet. The project started in 2015 and by this date, 597 satellites have been launched into orbit. By the end of the project, SpaceX wants to build a „shell“ around the Earth consisting of over 4,000 communcation satellites which will use phased array antennas for communication with ground relays in combination with laser communication technology to provide global low-latency high bandwidth coverage. In the first phase, 1,584 satellites will be sent to space at the altitude of 550 km and the second phase adds another 2,825 satellites on three different altitudes to increase density and coverage as far as 70° North/South. 
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/spacex_logo.jpg?raw=true" alt="" width="500"/>
<p/>
<br />

How does *Starlink* work? Each satellite is connected to 4 more satellites – two neighbours are on the same plane, one ahead and one behind. Another two neighbours come from different orbits, one in the front right and the other one behind left forming a good South-West to North-East and North-West to South-East connection.
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/satellite_connection.png?raw=true" alt="" width="500"/>
<p/>
<br />

## Satellites vs Fiber Optics

Compared to optical fiber, transmission speed in space is around 1.47 times higher than in glass optical cables. With the increased transmission speed, free-space laser link speeds could reach rates of 100 Gb/s or even higher. Even though it's hard to predict the network capacity, the most important aspect of transmission is latency. Latency doesn't seem as big of a problem on small distances, but it increases the further we travel through an optic cable. In theory, internet traffic via geostationary satellites has a latency of at least 477 ms. In practice, that number is closer to 600 ms. Being on lower heights, *Starlink* satellites will offer more practical latencies of around 25 to 35 ms. Latency of light travelling through the cable is 49 ms per kilometre, compared to latency of light travelling through vacuum is 33.3 ms per kilometre. Latency between New York and London via fiber optic is around 59 ms, while, in theory, it should be around 40 ms using *Starlink*. 

The exact latency using *Starlink* is still a mystery because there's no publicly available information. We had to make some assumptions on our part to make the simulation more realistic. We also approximate the signal processing time for satellites and ground transceivers, which is fixed and set to 4 ms. For example, a signal travelling from city A to city B via 4 satellites will result in 40 ms of processing time in total. The ground transceivers in both cities will contribute 4 ms of processing time each while the satellites will contribute 8 ms of processing time (4 ms to process the received signal and 4 ms for further transmission processing).
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/starlink_satellite.jpg?raw=true" alt="" width="500"/>
<p/>
<br />

Why is low-latency so important? *Starlink* is designed to support near real-time access to rapidly changing data. Primarily, the system is advertised as a way to connect every human on this planet to the internet. Not only that this system will provide better connection in underdeveloped countries, it will be beneficial to the stock market. Currently, privately owned Hibernia Express cable has the lowest latency between New York and London with latency of 58.95 ms which is 39.4% slower than *Starlink* connection. With millions of dollars being moved in fractions of a second, having lower latency would provide massive advantage in capitalizing price swings. The improvements will be even more pronounced for London to Singapour transmission with rapid gains in speed increase with every kilometre data travels.

How to find low-latency routes? This whole model and dataset can be represented as a graph problem. If we tackle the problem as such, we can use methods from graph theory to calculate and find the path with the lowest latency. 

## Graph Databases in Satellite Networks

So how exactly does graph theory step into this story? Let’s look at the nature of the problem. We have some satellites and lasers that transmit data between them. We could easily model this scenario with some nodes (vertices) and relationships (edges), where the nodes represent the satellites and the relationships represent the laser connections between them. The same notion is applied to cities and radio connections between cities and satellites. The following picture shows one of the relations that we constructed in the *Starlink* simulation.

This simple concept is the basis of graph theory where the main object of interest is a graph, which is nothing more than a structure composed of nodes and relationships. We give these nodes and relationships labels and properties so we can model real life problems with more credibility. Nodes are objects or entities with certain attributes, just like in the classic relational database model, while relationships are connections between nodes that can also hold information such as the nature and gravity of the connection. 
<br />
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/starlink_model.png?raw=true" alt="" width="400"/>
<p/>
<br />

These relationships are what separate the graph database model from the relational database model. They enable flexible data manipulation and are a strong argument against the rigid foreign key assignment that the relational model uses. Here’s the difference: 

If you want to learn more about the advantages of the graph database model, feel free to check out this blog [post]( https://memgraph.com/blog/why-your-business-should-use-a-graph-database). 

Finally, when the graph structure is implemented, as well as all the rules related to orbital mechanics, the *Starlink Network Simulator* gives us a proper view into the intricacies of the project. You can choose pairs of cities and run the simulation to see the shortest transmission path generated between them, as well as the transmission time needed in comparison to the fibre-optic cable.

## Exploring *Starlink* with Cypher Queries

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
Now we can try out something more interesting. Let us return all the satellites that are visible from London. To be more specific, we are returning all the relationships of type `VISIBLE_FROM` that a node with the label `City` and with the property name equal to London has. 
The Cypher query looks like this:
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

If we wanted to return all the relationships a satellite has, we would need to specify if they are of type `VISIBLE_FROM` or `CONNECTED_TO` because the former represents connections between cities and satellites, while the latter represents connections between satellites. We are just going to omit the relationship type in our query so both of these types are returned. 
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

The most important aspect of a satellite network is the transmission time from one point to another. Given that the satellites are in constant movement, their visibility from cities is therefore changing as well. The network needs to be able to calculate the shortest path exceedingly fast and efficiently in real time with these changes in mind. This is where Memgraph comes in handy. 

One way to find such a path would be to run the following Cypher query:

```
   MATCH p=(:City { name: "New York"})
      -[*wShortest (e, n | e.transmission_time) total_transmission_time]-
      (:City { name: "London"})
   RETURN nodes(p) as path, total_transmission_time;
```

The returned path has the smallest possible sum of individual transmission times, i.e. the shortest path for data transmission. This query returns paths that can also include nodes with the label `City` and relationships of type `VISIBLE_FROM` if their use could lower the overall transmission time. 

The same logic could be applied for using ground relay stations that would aid in the transmission process. While this is also an interesting tactic that could be explored, it is not part of our initial problem definition so we will gloss over it for now. 

To fix this problem, we need to add the following query segment: 

```
   WHERE ALL(x IN nodes(p)[1..-1] WHERE (x:Satellite))
```
to ensure that the returned path only contains nodes with the label `Satellite`. 
The final query would look like this:
```
   MATCH p=(:City { name: "New York"})
      -[*wShortest (e, n | e.transmission_time) total_transmission_time]-
      (:City { name: "London"})
   WHERE ALL(x IN nodes(p)[1..-1] WHERE (x:Satellite))
   RETURN nodes(p) as path, total_transmission_time;
```

To get a visual representation of the path in Memgraph Lab, you would need to return the found path and exclude the variable `total_transmission_time`. The query should be:
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

As we have shown in this example, Memgraph DB can be used to solve a complicated problem relatively easily and many other problems can be tackled similarly. Routing packets across mesh networks, supply chain analysis and [optimal route planning](https://memgraph.com/blog/how-to-build-a-route-planning-application-with-breadth-first-search-and-dijkstras-algorithm) are only a few of the numerous examples that are waiting to be explored with this technology. If you want to learn more about how Memgraph can help your business, please visit our website or feel free to contact us directly. 