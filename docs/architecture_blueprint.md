# Zone Job-Scheduler & Deadlock-Safety Engine Architecture Blueprint
## Task 9: Cloud Architecture Design

### Proposed Architecture

The Zone Job-Scheduler & Deadlock-Safety Engine will use a cloud-based architecture designed to support job scheduling, resource management, deadlock-safety checks, and system monitoring.

The proposed architecture contains the following main components:

1. **User or Client Layer**
   Users or client applications send job requests and system requests to the application.

2. **Application Layer**
   The main application processes job information and performs scheduling operations using algorithms such as FCFS, SJF, SRTF, Round Robin, and Priority Scheduling.

3. **Deadlock-Safety Layer**
   The system performs deadlock-safety checks using Banker's Algorithm before granting resource requests.

4. **Database Layer**
   Job information, resource-allocation information, and system data can be stored in a database for persistence and future processing.

5. **Monitoring Layer**
   System performance, application health, and resource usage can be monitored to detect failures and performance problems.

### High-Level Architecture Flow

User/Client
↓
Application or API Layer
↓
Zone Job Scheduler
↓
Deadlock-Safety Engine
↓
Database and Resource Management
↓
Monitoring and Logging

### Design Rationale

The cloud architecture separates the main functions of the system into different layers. The scheduling component handles job scheduling decisions, while the deadlock-safety component checks whether resource requests can be safely granted.

This separation improves modularity and makes it easier to scale or modify individual components in the future. Monitoring and logging provide visibility into system performance and application behaviour.

The architecture is designed as a blueprint and does not require actual cloud infrastructure to be provisioned.


## Task 10: Kubernetes Deployment Design

### Containerization

The Zone Job-Scheduler & Deadlock-Safety Engine can be packaged into a container using Docker. Containerization provides a consistent environment for running the application and makes deployment easier.

The application can be divided into separate services where required, such as:

* Job Scheduler Service
* Deadlock-Safety Service
* API Service
* Monitoring and Logging Service

### Kubernetes Deployment

Kubernetes can be used to deploy and manage the containerized application.

The main application services can run as Kubernetes Deployments. A Deployment helps manage application replicas and automatically replaces failed containers.

The proposed Kubernetes components are:

1. **Deployment**
   Used to run the application containers.

2. **Pods**
   Each application instance runs inside a Kubernetes Pod.

3. **Service**
   A Kubernetes Service provides communication between application components and allows clients to access the application.

4. **ConfigMap**
   Used to store non-sensitive configuration information.

5. **Secret**
   Used to store sensitive information such as database credentials.

6. **Horizontal Pod Autoscaler**
   Can automatically increase or decrease the number of application replicas based on CPU or other resource usage.

### Scaling Strategy

The Job Scheduler and API components can be scaled independently depending on the workload. If the number of incoming job requests increases, additional application replicas can be created.

For example:

* Normal workload: 2 application replicas
* Higher workload: Automatically scale to additional replicas
* Low workload: Reduce unnecessary replicas to save resources

### Reliability

Kubernetes improves reliability by automatically restarting failed containers. If one Pod fails, Kubernetes can create a replacement Pod.

Multiple replicas can also be used to reduce the impact of a single application failure.

### Design Rationale

Using containers and Kubernetes makes the proposed architecture modular, scalable, and easier to manage. The application can be deployed consistently across different environments, while Kubernetes provides features for scaling and automatic recovery from failures.


## Task 11: Data Storage Design

### Database Selection

The proposed architecture uses a relational database to store persistent system information. A relational database is suitable because the system contains structured information such as jobs, resource allocations, scheduling results, and user or application requests.

### Data to Store

The database can store the following information:

* Job ID
* Zone
* Arrival time
* Burst time
* Priority
* Scheduling results
* Resource allocation information
* Maximum resource requirements
* Available resources
* Banker's Algorithm results
* System and application records

### Proposed Database Tables

The system can use the following logical tables:

1. **Jobs Table**
   Stores information about each job, including job ID, zone, arrival time, burst time, and priority.

2. **Scheduling Results Table**
   Stores scheduling information such as waiting time, turnaround time, completion information, and the algorithm used.

3. **Resource Allocation Table**
   Stores information about allocated resources for each process.

4. **Resource Request Table**
   Stores resource requests and whether they were granted or denied by the deadlock-safety system.

5. **System Logs Table**
   Stores important system events and application information.

### Data Flow

Job requests are received by the application layer and processed by the Job Scheduler.

The scheduler can store job information and scheduling results in the database.

When a process makes a resource request, the Deadlock-Safety Engine checks the request using Banker's Algorithm. The result of the request can then be stored for future analysis and auditing.

### Reliability and Backup

The database should support regular backups to prevent data loss.

A managed cloud database can provide additional reliability features such as automatic backups, replication, and recovery.

### Design Rationale

Using persistent storage allows the system to keep job and resource information even after the application restarts. The stored information can also be used for monitoring, analysis, debugging, and future scheduling decisions.


## Task 12: Networking and Security Design

### Network Architecture

The proposed system uses a layered network architecture to separate public-facing components from internal application and data components.

The network can be divided into the following areas:

1. **Public Access Layer**
   Users or client applications send requests to the system through a secure public entry point.

2. **Application Layer**
   The Job Scheduler, Deadlock-Safety Engine, and API services run inside the application environment.

3. **Database Layer**
   The database is placed in a private network area and is not directly accessible from the public internet.

### Network Communication

The communication flow is:

User or Client
↓
Load Balancer or API Entry Point
↓
Application Services
↓
Job Scheduler and Deadlock-Safety Engine
↓
Database

Only required services should be allowed to communicate with each other.

### Security Measures

The proposed architecture includes the following security measures:

* Use HTTPS for secure communication.
* Restrict database access to authorized application services.
* Store sensitive credentials in Kubernetes Secrets.
* Store non-sensitive configuration in ConfigMaps.
* Use authentication and authorization for system access.
* Apply the principle of least privilege.
* Restrict unnecessary network communication between services.
* Keep application and container images updated.

### Access Control

Different users and services should receive only the permissions required to perform their tasks.

For example:

* Application services can access only the required database resources.
* Database credentials should not be exposed to ordinary users.
* Administrative functions should be restricted to authorized administrators.

### Network Isolation

The database should remain isolated from direct public access.

The application services can communicate with the database through internal networking. This reduces the attack surface and protects sensitive system information.

### Design Rationale

The networking design separates public access, application processing, and data storage into different layers. This improves security by reducing unnecessary exposure of internal components.

Using secure communication, restricted access, network isolation, Secrets, and least-privilege permissions helps protect the proposed Zone Job-Scheduler & Deadlock-Safety Engine.


## Task 13: Monitoring and Reliability Design

### Monitoring

The proposed system should be continuously monitored to track application health, performance, and resource usage.

Important metrics include:

* CPU usage
* Memory usage
* Number of running application instances
* Number of job requests
* Job processing time
* Average waiting time
* Average turnaround time
* Resource utilization
* Failed resource requests
* Application errors

Monitoring these metrics can help identify performance problems and system failures.

### Logging

The application should generate logs for important events, including:

* Job submission
* Scheduling decisions
* Resource requests
* Banker's Algorithm decisions
* Granted or denied requests
* Application errors
* System failures

Centralized logging makes it easier to investigate problems and understand system behaviour.

### Health Checks

Application services should provide health checks.

Kubernetes can use:

* **Liveness checks** to determine whether an application is still running correctly.
* **Readiness checks** to determine whether an application is ready to receive requests.

If a service fails a liveness check, Kubernetes can restart the failed container.

If a service is not ready, traffic should not be sent to it until it becomes ready.

### Reliability

The proposed system improves reliability by using multiple application replicas.

If one application instance fails, another replica can continue processing requests.

Kubernetes Deployments can automatically replace failed Pods.

Database backups and recovery mechanisms should also be used to protect persistent data.

### Fault Handling

The system should detect and respond to:

* Failed application containers
* Failed Pods
* High CPU or memory usage
* Database connection failures
* Unexpected application errors

Alerts can be generated when important failures or performance problems are detected.

### Design Rationale

Monitoring provides visibility into system health and performance, while logging provides detailed information for troubleshooting.

Health checks, multiple replicas, automatic Pod replacement, backups, and failure detection improve the reliability of the proposed Zone Job-Scheduler & Deadlock-Safety Engine.


## Task 14: Cost and Deployment Considerations

### Cost Considerations

The proposed cloud architecture should use resources efficiently to control operational costs.

The main cost factors may include:

* Compute resources for application containers
* Kubernetes cluster resources
* Database storage and processing
* Network usage
* Monitoring and logging services
* Backup and recovery storage

The system can reduce unnecessary costs by using automatic scaling. Additional application instances can be created only when the workload increases and reduced when the workload becomes lower.

### Resource Optimization

The following approaches can help reduce resource usage:

* Use only the number of application replicas required for the current workload.
* Use Horizontal Pod Autoscaling to increase or decrease application replicas.
* Set appropriate CPU and memory requests and limits.
* Remove unused resources.
* Store only necessary logs for an appropriate retention period.
* Use automated backups according to data requirements.

### Deployment Strategy

The application should be deployed using a controlled and repeatable deployment process.

A possible deployment flow is:

Source Code Repository
↓
Build Application Container
↓
Test Application
↓
Deploy to Kubernetes
↓
Run Health Checks
↓
Monitor Application

### Continuous Integration and Deployment

A CI/CD pipeline can automate important deployment steps.

The pipeline can perform:

1. Code validation
2. Automated testing
3. Container image creation
4. Security checks
5. Deployment to the target environment
6. Post-deployment health checks

Automated deployment reduces manual errors and makes the release process more consistent.

### Deployment Environments

Separate environments can be used for different stages:

* **Development** – used for testing new changes.
* **Testing or Staging** – used to test the application before production deployment.
* **Production** – used to run the live application.

This separation reduces the risk of untested changes affecting the production system.

### Design Rationale

The proposed deployment strategy focuses on scalability, reliability, and cost efficiency.

Automatic scaling can reduce unnecessary resource usage, while controlled deployment and testing can reduce the risk of application failures.

Using CI/CD, health checks, monitoring, and separate environments provides a structured approach for deploying and maintaining the Zone Job-Scheduler & Deadlock-Safety Engine.
