# Future Work and Potential Extensions

This document contains technically interesting questions and extensions identified during the planning of the thesis.

These topics are intentionally excluded from the primary study in order to preserve a controlled and achievable scope.

## 1. Different DDS Implementations

A natural extension would be to compare different DDS implementations used by ROS 2, such as:

Fast DDS
Cyclone DDS
Other supported DDS implementations

Questions could include:

- How does middleware selection affect latency?
- Does one implementation produce lower communication overhead?
- Does the relative performance of different node partitionings change between DDS implementations?

This would turn part of the study into a ROS 2 middleware benchmarking investigation.

## 2. Zenoh

ROS 2 systems can also be configured to use alternative communication approaches involving Zenoh.

Potential research questions include:

- How does Zenoh compare with DDS for this workload?
- Does Zenoh reduce communication overhead?
- How does its performance change with increasing pipeline partitioning?

This is potentially a substantial study by itself and is therefore outside the current scope.

## 3. QoS Configuration

ROS 2 provides multiple Quality of Service policies.

Potential variables include:

- Reliability
- Durability
- History
- Queue depth
- Best-effort vs. reliable communication

A future study could investigate:

- How does ROS 2 QoS configuration affect computer-vision pipeline latency, throughput, and resource utilization?

For the current thesis, QoS will remain fixed.

## 4. Docker / Containerized Deployment

Many real-world robotics systems are deployed using containers.

A future study could compare:

```
Bare Metal ROS 2
     vs
Docker ROS 2
```

Possible variables could include:

- Containerization overhead
- Host networking vs. other networking configurations
- GPU access
- Shared memory configuration
- IPC configuration
- CPU affinity

Containerization is excluded from the current thesis because it introduces another experimental dimension unrelated to the primary research question.

## 5. ROS 2 Distribution Comparison

The performance of the system could potentially vary between ROS 2 distributions.

A future investigation could compare different distributions under otherwise identical conditions.

This would require controlling for:

- Package versions
- Middleware versions
- Python versions
- System dependencies
- Default configuration changes

This is outside the current scope.

## 6. Python vs. C++

The current study intentionally uses Python for both implementations.

A future investigation could compare:

```
Python / rclpy
     vs.
C++ / rclcpp
```

This could answer a different question:

- How much of the observed performance difference is attributable to ROS 2 architecture, and how much is attributable to language/runtime overhead?

- This would also make it possible to investigate additional ROS 2 mechanisms such as node composition.

## 7. ROS 2 Node Composition

A future study could investigate composable nodes and compare them against ordinary ROS 2 inter-process communication.

Potential configurations could include:

```
Separate Processes
        vs.
Multiple Nodes in One Process
        vs.
Monolithic Application
```

This would be particularly interesting for determining how much of the communication overhead is caused by process boundaries versus ROS 2's node abstraction itself.

## 8. Intra-Process Communication

ROS 2 supports mechanisms intended to reduce communication overhead when nodes operate within the same process.

A future study could compare:
```
Inter-process communication
        vs.
Intra-process communication
```

This could help distinguish:

- Serialization overhead
- Memory-copy overhead
- Process-boundary overhead
- ROS 2 executor overhead

## 9. Message Passing and Memory Copies

A deeper investigation could explicitly profile the movement of image data through the pipeline.

Potential questions include:

- How many memory copies occur?
- How much time is spent serializing images?
- How does image size affect communication cost?
- Does communication overhead become dominant at higher resolutions?

This would provide a more detailed explanation of why ROS 2 performance changes.

## 10. Longer and More Complex Pipelines

The current thesis will investigate a small number of pipeline partitionings.

> Partly addressed by the primary study as of the node-partitioning decision:
> the experimental configurations span 0, 1, 3 and 6 boundaries, and the
> seven-node configuration places one node per operation, which gives a coarse
> reading of how the number of boundaries relates to overhead. What remains
> future work is a finer and systematic variation of the number of stages
> beyond those four configurations, and varying the computational cost of
> individual stages.

A future study could systematically vary the number of stages:
```
2 nodes
3 nodes
4 nodes
5 nodes
6 nodes
...
```

This could potentially establish a relationship between:

Number of communication boundaries → communication overhead

A more sophisticated study could also vary the computational cost of individual stages.

## 11. Networked ROS 2 Nodes

The current study is intended to run on a single Jetson.

A natural extension would be to distribute nodes across multiple computers:

```
Jetson
  ↓
Network
  ↓
Desktop / Edge Computer
```

This would introduce additional variables such as:

- Network latency
- Bandwidth
- Packet loss
- Ethernet vs. Wi-Fi
- DDS discovery
- Network QoS

This would be substantially different from the current single-device experiment.

## 12. Different Computer-Vision Workloads

The current study should use one representative application.

Future research could investigate whether the findings generalize to:

- Object detection
- Image classification
- Semantic segmentation
- Instance segmentation
- Object tracking
- Optical flow
- Depth estimation

Different workloads may have very different computation-to-communication ratios.

## 13. Different Hardware

The same methodology could be applied to:

- Other NVIDIA Jetson platforms
- Desktop GPUs
- CPUs
- Other embedded AI platforms

This could determine whether ROS 2 communication overhead becomes more or less significant as computational resources increase.

## 14. Real-Time Analysis

A deeper investigation could move beyond average performance and examine real-time behavior.

Potential metrics include:

- Worst-case latency
- P95 latency
- P99 latency
- Jitter
- Deadline misses
- Scheduling behavior

This could turn the project toward a more formal real-time-systems analysis.

## 15. Principle for Future Work

These extensions should not be treated as requirements that the current thesis has failed to address.

They represent different research questions that become possible once the basic benchmark has been established.

The current thesis should first establish a reliable baseline.

Future work can then investigate why the observed behavior occurs and how the results change under different middleware, communication, deployment, language, and hardware configurations.