# Monolithic 3-Dimensional Network-on-Chip (M3DNoC)

## Description

This repo contains driver code for performing the experiments shown in our EE382C project report.

## Appendices

### Routing algorithm comparison

Here are three plots comparing dimension-order, XY-YX, and minimal-adaptive routing for k = 4 and k = 8 3D meshes under uniform random traffic.

#### dimension-order
![dor](render/avg_lat-uniform-dor.png)

#### XY-YX
![xy_yx](render/avg_lat-uniform-xy_yx.png)

#### minimal-adaptive
![min_adapt](render/avg_lat-uniform-min_adapt.png)

### Traffic power consumption comparison

Here is a plot showing different network components' power consumption across different traffic patterns on the 3D mesh.

![power-consumption](render/power-consumption-of-different-traffic-patterns.png)
