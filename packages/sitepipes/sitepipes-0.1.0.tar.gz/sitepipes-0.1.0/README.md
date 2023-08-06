# sitepipes

A framework for federated data networks with web components

## Overview

* **Dataset**: Holds a collection of data
* **Model**: Holds a machine learning model
* **Component**: Performs a set of operations on a Dataset or Model

The sitepipes framework performs computations across datasets that may or not be on the same host machine. It revolves around the idea of a site: a host machine (or cluster) that has access to one or more datasets and/or models. Privacy with utility is the name of the game.

The sitepipes framework is designed to be similar to the plumbing in a home. There are "pipes" to move data from Point A to Point B (like water pipes). There are "tanks" for cached data (like water tanks). There are "fittings" to connect two or more pipes (like pipe fittings). And so much more!

The sitepipes framework uses PySyft, which is a wrapper for Torch tensor operations with additional federated learning operations. 

The sitepipes framework contains web components for web frameworks like React and Angular.
