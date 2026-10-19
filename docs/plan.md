# Thesis Proposal and Research Plan

Working Title

*"Caracterización experimental del impacto del particionamiento en nodos ROS 2 sobre el rendimiento de una cadena de procesamiento de video en una NVIDIA Jetson Orin Nano"*

*"Experimental Characterization of the Performance Impact of Partitioning a Video Processing Pipeline into ROS 2 Nodes on an NVIDIA Jetson Orin Nano"*

## 1. Motivation

Modern robotic systems increasingly rely on embedded computing platforms to perform computer-vision and artificial-intelligence workloads close to the source of the sensor data.

Frameworks such as ROS 2 provide modularity and facilitate the integration of independent components through node-based communication. This modularity can be advantageous for the development and maintenance of robotic systems, but communication between nodes may introduce computational and latency overhead.

For resource-constrained embedded platforms such as the NVIDIA Jetson Orin Nano, the practical impact of this overhead is relevant when designing computer-vision systems.

This thesis therefore investigates the performance trade-off between a monolithic single-process implementation and an equivalent ROS 2-based implementation of a computer-vision pipeline.

## 2. Problem Statement

A computer-vision application can be implemented as a single process in which image acquisition, preprocessing, inference, and postprocessing occur sequentially within one program.

Alternatively, these operations can be divided into ROS 2 nodes that communicate using ROS 2 topics.

The latter architecture provides greater modularity but introduces communication boundaries that may involve message handling, serialization, memory transfers, scheduling, and other overhead.

On an embedded platform, these additional costs may affect the achievable throughput and latency of the application.

The magnitude of this effect depends on the workload and architecture, and therefore requires experimental characterization.

## 3. Research Question

*What is the performance impact of partitioning a computer-vision pipeline into ROS 2 rclpy nodes compared with an equivalent single-process Python implementation when executed on an NVIDIA Jetson Orin Nano?*

**Secondary Question**

*How does increasing the degree of partitioning of the computer-vision pipeline into ROS 2 nodes affect latency, throughput, and resource utilization?*

## 4. Objectives
### 4.1 General Objective

Experimentally characterize the performance difference between a monolithic Python computer-vision pipeline and equivalent ROS 2 rclpy implementations on an NVIDIA Jetson Orin Nano.

### 4.2 Specific Objectives

- Develop a representative computer-vision pipeline capable of running on the Jetson Orin Nano.

- Implement the pipeline as a monolithic single-process Python application.

- Implement equivalent processing stages as ROS 2 rclpy nodes.

- Develop multiple ROS 2 configurations with different degrees of pipeline partitioning.

- Establish a reproducible benchmarking methodology.

- Measure end-to-end latency and processing throughput.

- Measure CPU, RAM, and GPU utilization.

- Optionally measure power consumption if reliable measurement is available.

- Compare the results statistically across configurations.

- Determine how the performance impact changes as the ROS 2 pipeline becomes more highly partitioned.

## 5. Hypotheses
### H1 — Latency

The ROS 2 implementations will exhibit greater end-to-end latency than the monolithic implementation due to communication and processing overhead introduced between nodes.

### H2 — Throughput

The monolithic implementation will achieve equal or greater throughput than the ROS 2 implementations under equivalent computational conditions.

### H3 — Resource Utilization

The ROS 2 implementations will require additional CPU and memory resources compared with the monolithic implementation.

### H4 — Partitioning

Increasing the number of ROS 2 communication boundaries will increase communication overhead and therefore increase end-to-end latency.

These hypotheses are predictions rather than expected outcomes that must be confirmed. Results that contradict one or more hypotheses remain valid and should be analyzed.

## 6. System Under Test
### 6.1 Hardware

Primary experimental platform:

NVIDIA Jetson Orin Nano

The exact hardware configuration should be recorded, including:

- Jetson module/model
- RAM capacity
- Storage
- Power mode
- Cooling configuration
- Connected camera/input device
- Operating temperature where relevant

## 7. Computer-Vision Application

A single representative computer-vision workload will be selected.

A suitable example is an object-detection pipeline using a neural-network model capable of running efficiently on the Jetson platform.

The exact model should be selected based on:

- Ability to run reliably on the Jetson Orin Nano
- Reproducibility
- Availability of documented model weights
- Reasonable inference time
- Suitability for real-time or near-real-time processing

The same model and inference configuration will be used in every benchmark.

## 8. Pipeline Architecture
### 8.1 Monolithic Implementation

The baseline implementation will consist of a single Python process.

```
Input
  ↓
Image Acquisition
  ↓
Preprocessing
  ↓
Inference
  ↓
Postprocessing
  ↓
Output
```

All stages execute within one process.

### 8.2 ROS 2 Implementation

The same logical stages will be implemented using ROS 2 rclpy.

A representative configuration could be:
```
Node A
  ↓
Node B
  ↓
Node C
  ↓
Node D
```

The exact mapping of processing stages to nodes should preserve functional equivalence with the monolithic implementation.

## 9. Experimental Configurations

Four configurations are used. All of them execute the same seven operations in
the same order, and each configuration is a merge of contiguous operations, so
that the only difference between them is where information crosses a process
boundary.

| Configuration | Nodes | Node boundaries |
|---|---|---|
| A — Monolithic | 1 process | none |
| B — Minimal partitioning | 2 | after acquisition |
| C — Moderate partitioning | 4 | after acquisition, after conditioning, after detection |
| D — Structural partitioning | 7 | one node per operation |

The seven operations are: acquisition; conditioning (letterbox and colour
conversion); detection (tensor construction, inference and decoding);
non-maximum suppression; coordinate adaptation; domain class filter; and
recording.

The configurations are nested: the boundaries of each one are a subset of the
boundaries of the next, so that moving from one configuration to the next adds
boundaries without reordering the chain or changing the work of any stage.

A, B and C carry the applied comparison against the monolithic baseline. C is
the split that corresponds to the usual way of structuring a perception stack
in ROS 2: a capture node, an image-conditioning node, a detector and a
consumer of its results.

D is a deliberate escalation of the degree of partitioning, not a recommended
deployment. Its three additional boundaries separate operations of trivial
computation and carry messages of the order of tens of KB, so the C→D
increment estimates the fixed cost of a boundary rather than the cost of
transporting bytes, while the B→C increment carries a 1.23 MB message and
estimates the payload-dependent cost. D is reported as what it is.

**Note — open experimentation on the number and placement of partition
points.** The partition points above are fixed for the pilot stage, but the
number of configurations and the exact placement of the node boundaries
remain open to adjustment while the experiments are being run. The reason is
concrete: boundaries that separate trivial operations may produce no
measurable difference in the metrics, in which case the high end of the range
contributes nothing to the characterization and a different placement (for
instance, at points that carry larger payloads) would be more informative.
Any such adjustment must be decided during the pilot phase, recorded in this
document and in `docs/pendientes.md`, and reported as a deviation from the planned
methodology. The matrix must not grow once the final campaign has begun (§17,
phase 5).

## 10. Experimental Matrix

A possible primary experimental matrix is shown below.

| Configuration | Architecture   | Partitioning | Resolution 1 | Resolution 2 | Resolution 3 |
|---------------|----------------|--------------|--------------|--------------|--------------|
| A             | Single process | 1 process    | ✓            | ✓            | ✓            |
| B             | ROS 2          | 2 Nodes      | ✓            | ✓            | ✓            |
| C             | ROS 2          | 4 Nodes      | ✓            | ✓            | ✓            |
| D             | ROS 2          | 7 Nodes      | ✓            | ✓            | ✓            |

Possible resolutions could be:
```
320 × 240
640 × 480
1280 × 720
```
The final resolutions should be selected based on the capabilities of the chosen input and computer-vision model.

This gives:

4 architectures × 3 resolutions = 12 experimental conditions

Each condition should be repeated multiple times or executed for a sufficiently long fixed duration to obtain stable measurements.

## 11. Benchmark Procedure

Each experimental condition should follow the same procedure.

#### 1. Initialize the system
Start the application and monitoring tools.

#### 2. Allow warm-up.

Discard an initial number of frames or a fixed warm-up period to avoid measuring startup behavior.

#### 3. Execute the workload

Run the computer-vision pipeline for a fixed duration or fixed number of frames.

#### 4. Record measurements

Collect:
    - End-to-end latency
    - FPS
    - CPU utilization
    - RAM utilization
    - GPU utilization
    - Optional power consumption

#### 5. Repeat

Repeat the experiment sufficiently to characterize variability.

#### 6. Reset

Return the system to the same baseline state before the next experimental condition.

## 12. Performance Metrics
### 12.1 End-to-End Latency

The time between the input entering the pipeline and the corresponding output being generated.

Report:

- Mean
- Median
- Standard deviation
- Minimum
- Maximum
- P95
- P99 where sufficient samples are available

### 12.2 Throughput

Measured in frames per second.

FPS = processed frames / elapsed time

### 12.3 CPU Utilization

Measure average and, where useful, peak CPU utilization.

### 12.4 Memory Utilization

Measure system RAM utilization.

GPU memory usage may also be recorded if reliable measurement is available.

### 12.5 GPU Utilization

Record GPU utilization to determine whether architectural overhead changes the utilization of the primary compute resource.

### 12.6 Power Consumption

If reliable measurement is available:

- Average power
- Peak power
- Energy per processed frame
- Performance per watt

Power measurements should be treated as an optional extension rather than a requirement that threatens the completion of the thesis.

## 13. Data Analysis

For each experimental condition:

    - Remove startup/warm-up measurements.
    - Calculate descriptive statistics.
    - Compare latency distributions.
    - Compare throughput.
    - Compare CPU, RAM, and GPU utilization.
    - Calculate percentage differences between configurations.
    - Investigate whether increasing node partitioning produces a consistent trend.

Example:

```
ROS overhead (%) = (ROS latency - baseline latency) / baseline latency × 100
```
Where appropriate, statistical tests can be selected after examining the collected data and its distribution.

The objective is not merely to determine which configuration is "faster," but to characterize the performance trade-off introduced by architectural partitioning.

## 14. Reproducibility

The following information should be documented:

- Hardware model
- JetPack version
- Linux distribution
- ROS 2 distribution
- DDS implementation
- Python version
- Package versions
- Model version/weights
- Model configuration
- Input resolution
- ROS 2 QoS configuration
- Power mode
- CPU/GPU configuration
- Ambient/environmental conditions where relevant
- Benchmark duration
- Number of repetitions
- Warm-up procedure

The source code and benchmark configuration should ideally be version-controlled.

## 15. Expected Contribution

The primary contribution of the thesis is an experimental characterization of the performance trade-offs associated with implementing a computer-vision pipeline as a set of ROS 2 nodes rather than as a monolithic process on an embedded NVIDIA platform.

The work may provide practical guidance for developers deciding whether the modularity offered by ROS 2 is accompanied by a significant performance penalty for this type of workload.

The thesis is not intended to establish a universal performance ranking of ROS 2 or computer-vision architectures.

## 16. Thesis Chapter Structure
### Chapter 1 — Introduction
#### 1.1 Motivation and Context

Motivate the need for the thesis by introducing, at a high level:

- Embedded computer vision
- Robotics software architectures
- ROS 2
- NVIDIA Jetson platforms

This section is motivational, not expository: the detailed treatment of
ROS 2, the Jetson platform and the related work belongs to Chapter 2. Its
length should remain a fraction of what a background chapter would require.

#### 1.2 Problem Statement

Explain the potential trade-off between modularity and performance.

#### 1.3 Research Question

Present the primary and secondary research questions.

#### 1.4 Objectives

Present the general and specific objectives.

#### 1.5 Scope and Contributions

Two symmetric subsections: **1.5.1 Scope** — clearly establish what is and is
not evaluated; and **1.5.2 Contributions** — state explicitly what the
contribution of the work is and why it is valuable. Limitations are implied by
the scope definition rather than listed as a separate item; they are discussed
in Chapter 6.

#### 1.6 Thesis Organization

Briefly describe the remaining chapters.

### Chapter 2 — Background and Related Work
#### 2.1 Computer Vision on Embedded Platforms
#### 2.2 NVIDIA Jetson Architecture

Focus only on hardware characteristics relevant to the experiment.

#### 2.3 ROS 2 Architecture

Introduce:

- Nodes
- Topics
- Publishers/subscribers
- Executors
- rclpy

#### 2.4 ROS 2 Communication

Explain the relevant communication mechanisms and DDS at a conceptual level.

#### 2.5 Computer-Vision Workload

Describe the selected algorithm/model.

#### 2.6 Performance Metrics

Define:

- Latency
- Throughput
- CPU utilization
- Memory utilization
- GPU utilization
- Optional power metrics

#### 2.7 Related Work

Review existing:

- ROS 2 benchmarks
- Robotics middleware studies
- Embedded computer-vision benchmarks
- Jetson performance studies
- Studies investigating ROS 2 communication overhead

#### 2.8 Research Gap

Explain what existing work does not answer and how this thesis addresses that gap.

### Chapter 3 — Methodology
#### 3.1 Experimental Platform

Describe the Jetson Orin Nano and experimental environment.

#### 3.2 Software Environment

Document:

- OS
- JetPack
- ROS 2
- Python
- DDS
- Packages

#### 3.3 Computer-Vision Pipeline

Describe the application and processing stages.

#### 3.4 Monolithic Implementation

Describe the baseline architecture.

#### 3.5 ROS 2 Implementation

Describe the node architecture.

#### 3.6 Experimental Configurations

Define each partitioning configuration.

#### 3.7 Benchmarking Procedure

Explain:

- Warm-up
- Run duration
- Number of repetitions
- Monitoring
- Data collection

#### 3.8 Performance Metrics

Define precisely how each metric is measured.

#### 3.9 Data Analysis

Describe statistical and comparative analysis.

#### 3.10 Reproducibility

Document all relevant configuration information.

### Chapter 4 — Results

Present experimental results without excessive interpretation.

Possible sections:

#### 4.1 Throughput
#### 4.2 End-to-End Latency
#### 4.3 CPU Utilization
#### 4.4 Memory Utilization
#### 4.5 GPU Utilization
#### 4.6 Power Consumption
Only if measured.

#### 4.7 Effect of Pipeline Partitioning
Compare the different ROS 2 configurations.

### Chapter 5 — Discussion

Interpret the results.

Questions to address:

- How large was the ROS 2 overhead?
- Did the overhead change with image resolution?
- Did additional node boundaries increase latency?
- Was the overhead computationally significant?
- Which resource was most affected?
- Did the computer-vision workload dominate the total processing time?
- Were the hypotheses supported?
- Are the results consistent with previous research?

Also discuss unexpected findings.

### Chapter 6 — Conclusions and Future Work
#### 6.1 Conclusions

Directly answer the research question.

#### 6.2 Main Findings

Summarize the most important quantitative results.

#### 6.3 Limitations

Discuss limitations such as:

- Single hardware platform
- Single computer-vision workload
- Fixed DDS configuration
- Fixed QoS configuration
- Python implementation

These are scope limitations, not necessarily weaknesses.

#### 6.4 Future Work

Discuss extensions such as:

- Different DDS implementations
- QoS benchmarking
- Zenoh
- Docker
- C++
- Node composition
- Intra-process communication
- Networked ROS 2
- Additional workloads
- Additional hardware

## 17. Suggested Work Sequence

The project should proceed in the following order.

### Phase 1 — Establish the Baseline

Set up the Jetson Orin Nano.

Install and document the software environment.

Implement the single-process Python pipeline.

Verify that it works correctly.

Do not benchmark yet.
### Phase 2 — ROS 2 Implementation

Implement the equivalent ROS 2 pipeline.

Begin with the smallest practical number of nodes.

Verify functional equivalence with the baseline.

Do not add additional middleware or deployment configurations.

### Phase 3 — Benchmark Infrastructure

Develop scripts/tools for:

- Timestamping
- Latency measurement
- FPS measurement
- CPU monitoring
- RAM monitoring
- GPU monitoring
- Data logging

Make the benchmark repeatable before collecting final results.

### Phase 4 — Pilot Experiments

Run a small number of tests to identify:

- Measurement problems
- Unexpected bottlenecks
- Incorrect assumptions
- Configuration errors

The purpose of the pilot is to fix methodology, not generate final results.

### Phase 5 — Final Experiments

Execute the predefined experimental matrix.

Do not add new experimental dimensions simply because they appear interesting during this phase.

Record deviations from the planned methodology, if any.

### Phase 6 — Analysis

- Clean the collected data.
- Calculate descriptive statistics.
- Generate plots.
- Compare configurations.
- Evaluate hypotheses.
- Interpret observed trends.

### Phase 7 — Writing

Write the thesis around the evidence produced by the experiment.

The final thesis should answer:

*What performance impact does ROS 2 node-based partitioning introduce for this computer-vision workload on the Jetson Orin Nano, and how does that impact change with the degree of partitioning?*

## 18. Definition of a Successful Thesis

The thesis is successful if it can:

- Produce functionally equivalent single-process and ROS 2 implementations.
    
- Measure their performance using a reproducible methodology.
    
- Quantify differences in latency, throughput, and resource utilization.
    
- Determine whether increasing ROS 2 partitioning changes those differences.
    
- Explain the observed results using the architecture and relevant literature.
    
- Clearly identify the limitations of the findings.
    
- Provide reproducible evidence supporting its conclusions.

It does not need to determine:

- The fastest DDS.
- The best QoS configuration.
- Whether Docker is faster.
- Whether C++ is faster than Python.
- Whether Zenoh is better than DDS.
- Whether ROS 2 is universally suitable for computer vision.

Those are separate research questions.