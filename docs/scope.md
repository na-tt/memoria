# Thesis Scope

*"Caracterización experimental del impacto del
particionamiento en nodos ROS 2 sobre el rendimiento
de una cadena de procesamiento de video en una
NVIDIA Jetson Orin Nano"*

*"Experimental Characterization of the Performance Impact of Partitioning a Video Processing Pipeline into ROS 2 Nodes on an NVIDIA Jetson Orin Nano"*

## 1. Research Question Primary Research Question

What is the performance impact of partitioning a computer-vision pipeline into ROS 2 nodes compared with an equivalent single-process Python implementation when executed on an NVIDIA Jetson Orin Nano?

The study is specifically concerned with the performance trade-off associated with introducing ROS 2 communication boundaries into an otherwise equivalent computer-vision application.

## 2. Core Comparison

The thesis will compare two implementations of the same computer-vision application.

### A. Monolithic Single-Process Implementation

The complete pipeline executes within a single Python process.

```
Input
  ↓
Preprocessing
  ↓
Computer Vision / Inference
  ↓
Postprocessing
  ↓
Output
```

### B. Multi-process ROS 2 Implementation

The same processing stages are distributed across multiple ROS 2 nodes using rclpy running as separate processes in the same host communicated via messages.

```
Input Node
    ↓
Processing Node(s)
    ↓
Inference Node
    ↓
Output
```

The underlying computer-vision algorithm, model, input data, hardware, and relevant processing parameters will remain equivalent between implementations.

## 3. Secondary Research Question

The ROS 2 implementation will additionally investigate whether increasing the number of node boundaries affects performance.

How does increasing the degree of partitioning of the computer-vision pipeline into ROS 2 nodes affect latency, throughput, and resource utilization?

The study will use a small number of representative partitioning configurations rather than attempting to characterize every possible ROS 2 architecture.

## 4. Independent Variables
**Primary Independent Variable:** Application architecture

- single-process Python
- Multi-process ROS 2 rclpy

**Secondary Independent Variable:** Degree of ROS 2 partitioning

For example:

2-node pipeline
4-node pipeline

The exact partitioning will be determined based on the final computer-vision pipeline.

## 5. Dependent Variables

The following performance metrics will be measured where practical:

- End-to-end latency
- Processing throughput / frames per second (FPS)
- CPU utilization
- RAM utilization
- GPU utilization
- Optional Metric: Power consumption / performance per watt

Power measurement will only be included if reliable and reproducible measurement can be achieved with the available hardware.

## 6. Controlled Variables

The following should remain constant between experimental configurations wherever possible:

- NVIDIA Jetson Orin Nano hardware
- Operating-system environment
- JetPack/software environment
- ROS 2 distribution
- Python version
- Computer-vision algorithm
- Model and model weights
- Model precision
- Input dataset/video
- Image resolution for each experiment
- Preprocessing operations
- Postprocessing operations
- Hardware acceleration settings
- Measurement duration
- Warm-up procedure
- Experimental methodology

The goal is for application architecture and degree of ROS 2 partitioning to be the primary differences between configurations.

## 7. ROS 2 Configuration

The thesis will use:

- One ROS 2 distribution
- One DDS implementation
- One fixed QoS configuration
- Python and rclpy
- A non-containerized deployment for the primary experiments

These choices are treated as controlled experimental conditions rather than variables under investigation.

## 8. Explicit Exclusions

The following are outside the primary scope of this thesis:

- Comparison of different programming languages
- C++ / rclcpp benchmarking
- ROS 2 composable nodes
- Comparison of different DDS implementations
- Comparison of different ROS 2 middleware configurations
- Systematic comparison of QoS policies
- Zenoh benchmarking
- Docker/containerization benchmarking
- Comparison of different ROS 2 distributions
- Comparison of different Jetson hardware platforms
- Comparison with other robotics middleware
- Comprehensive benchmarking of ROS 2 as a whole
- Evaluation of multiple unrelated computer-vision applications

These topics may be discussed as potential future work.

## 9. Scope Principle

The thesis is not intended to answer:

"What is the fastest possible way to run computer vision with ROS 2?"

Instead, it aims to answer:

"What performance cost is associated with partitioning an equivalent computer-vision application into ROS 2 nodes on an NVIDIA Jetson Orin Nano?"

This distinction defines the boundary of the study.

## 10. Scope Freeze

Once the experimental setup has been established, additional technologies or configurations should not be added to the primary experiment unless they are necessary to answer the research question.

New ideas should instead be recorded in the Future Work document.

The objective is to produce a controlled, reproducible, and sufficiently rigorous undergraduate study rather than a comprehensive evaluation of every ROS 2 performance variable.