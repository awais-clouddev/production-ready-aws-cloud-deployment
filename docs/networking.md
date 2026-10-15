# VPC & Network Architecture

> **Deployment status:** Historical portfolio deployment, subsequently decommissioned. The author reports that paid AWS services were deleted. Screenshots and successful runtime results describe the earlier deployment, not a currently running environment. Current account inventory and billing have not been independently verified. This maintenance work is offline and does not recreate AWS resources.

## Purpose

This document describes the network architecture used by the AWS deployment, including VPC segmentation, subnet roles, internet connectivity, private workload access, and network traffic flow.

The objective was to expose only the load-balancing layer publicly while keeping application workloads, PostgreSQL, and Valkey inside private network tiers.

![VPC Resource Map](../screenshots/01-vpc-resource-map.png)

---

## VPC

The deployment uses a dedicated custom VPC:

- Name: `project3-vpc`
- Region: `ap-south-1` — Asia Pacific (Mumbai)
- Availability Zones used: `ap-south-1a` and `ap-south-1b`

The VPC contains six subnets arranged into three logical network tiers.

---

## Subnet Design

### Public Layer

The public subnet layer contains:

- `project3-public-a`
- `project3-public-b`

These subnets provide the public-facing network layer used by the internet-facing Application Load Balancer.

### Private Application Layer

The private application subnet layer contains:

- `project3-private-app-a`
- `project3-private-app-b`

The frontend and API ECS/Fargate tasks run inside these private application subnets.

Fargate public IP assignment is disabled, preventing direct public access to the containers.

### Private Data Layer

The private data subnet layer contains:

- `project3-private-data-a`
- `project3-private-data-b`

Amazon RDS PostgreSQL and Amazon ElastiCache for Valkey use the private data layer so that the managed data services are not exposed directly to the internet.

---

## Internet Gateway

The VPC uses the Internet Gateway:

`project3-igw`

The Internet Gateway provides internet connectivity for resources that belong to the public network layer, including the Application Load Balancer.

---

## NAT Gateway

The network architecture includes:

`project3-nat-gateway`

The NAT Gateway provides outbound internet access for workloads located in private subnets without making those workloads directly reachable from the public internet.

This is important for private ECS/Fargate tasks that may need outbound access to AWS service endpoints or external package/service endpoints while remaining private.

---

## Application Load Balancer Placement

The internet-facing Application Load Balancer `project3-helpdesk-alb` is associated with the public network layer across Availability Zones.

The ALB acts as the only public application entry point.

Incoming traffic follows this path:

```text
Internet
   |
   v
Internet Gateway
   |
   v
Public Subnets
   |
   v
Application Load Balancer
```

The ALB then forwards traffic into the private application layer.

---

## Private ECS/Fargate Networking

Both ECS services run without public IP addresses:

- `project3-frontend-service`
- `project3-api-service`

The Application Load Balancer reaches these tasks through their private IP addresses and the corresponding target groups.

Validated target examples during deployment included:

- Frontend target on port `80` — Healthy
- API target on port `8000` — Healthy

The containers therefore do not require direct inbound internet exposure.

---

## Private Data Connectivity

The API service communicates privately with two managed data services:

### PostgreSQL

```text
API ECS/Fargate
   |
   | TCP 5432
   v
Amazon RDS PostgreSQL
```

### Valkey

```text
API ECS/Fargate
   |
   | TCP 6379
   v
Amazon ElastiCache for Valkey
```

Security groups restrict both communication paths so that only the API layer can initiate these connections.

---

## Network Traffic Flow

The complete application traffic flow is:

```text
Users
  |
  v
Internet
  |
  v
Internet Gateway
  |
  v
Application Load Balancer
  |
  +---- / --------> Frontend ECS/Fargate
  |                   Private App Subnet
  |
  +---- /api/* ---> API ECS/Fargate
                       Private App Subnet
                              |
                      +-------+-------+
                      |               |
                      v               v
                 PostgreSQL          Valkey
                 Private Data     Private Data
                    Layer            Layer
```

---

## Network Isolation Strategy

The network design follows these principles:

- Only the ALB is directly exposed to public application traffic.
- ECS/Fargate workloads run in private application subnets.
- ECS tasks use private IP addressing.
- Public IP assignment is disabled for application containers.
- PostgreSQL is not directly accessible from the internet.
- Valkey is not directly accessible from the internet.
- Database traffic is restricted to the API layer.
- Cache traffic is restricted to the API layer.
- Public and private workloads are separated into dedicated subnet tiers.
- Resources are distributed across Availability Zones.

---

## Evidence

- [VPC Resource Map](../screenshots/01-vpc-resource-map.png)
- [Security Groups](../screenshots/02-security-groups.png)
- [Application Load Balancer](../screenshots/03-application-load-balancer-overview.png)
- [API Target Health](../screenshots/05-api-target-health.png)
- [Frontend Target Health](../screenshots/06-frontend-target-health.png)

---

## Related Documentation

- [Architecture](architecture.md)
- [Security](security.md)
- [Deployment](deployment.md)
- [Validation](validation.md)

## Historical Availability Boundary

The ECS screenshot shows one running task per service. Two-AZ networking
does not establish redundant application instances or tested failover.

The Valkey screenshot shows one node, Multi-AZ disabled and automatic
failover disabled. Database failover was not demonstrated by the retained
evidence. No current runtime availability is asserted.
