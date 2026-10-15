# AWS Deployment Workflow

> **Deployment status:** Historical portfolio deployment, subsequently decommissioned. The author reports that paid AWS services were deleted. Screenshots and successful runtime results describe the earlier deployment, not a currently running environment. Current account inventory and billing have not been independently verified. This maintenance work is offline and does not recreate AWS resources.

## Purpose

This document records the end-to-end deployment workflow used to move the containerized Help Desk workload from the local Docker environment into AWS.

The workflow focuses on infrastructure preparation, container delivery, networking, ECS/Fargate deployment, managed data services, load balancing, application initialization, and operational validation.

---

## Deployment Sequence

The deployment was completed in the following order:

1. Prepared the AWS account, IAM access, MFA, Region, and cost controls.
2. Prepared the frontend and API container images.
3. Stored both images in private Amazon ECR repositories.
4. Built the custom VPC and subnet architecture.
5. Created service-specific security groups.
6. Provisioned Amazon RDS PostgreSQL.
7. Provisioned Amazon ElastiCache for Valkey.
8. Created the ECS cluster.
9. Created frontend and API ECS task definitions.
10. Created the Application Load Balancer and target groups.
11. Configured HTTP listener routing and API URL rewriting.
12. Created the frontend and API ECS/Fargate services.
13. Verified running tasks and healthy load-balancer targets.
14. Initialized the PostgreSQL application schema.
15. Performed full browser and API validation.
16. Configured and verified CloudWatch logging and monitoring.
17. Performed security and reliability validation.

---

## 1. Container Image Delivery

The application workload originated from the previous Docker-based Help Desk platform.

Two deployment images were used:

- Frontend container — Nginx serving the web interface
- API container — Python, FastAPI, and Uvicorn

Private ECR repositories were prepared:

- `project3-helpdesk-frontend`
- `project3-helpdesk-api`

The repositories use immutable image tags and AES-256 encryption.

![ECR Repositories](../screenshots/08-ecr-private-repositories.png)

---

## 2. Network Foundation

A custom VPC named `project3-vpc` was created in `ap-south-1`.

The network was separated into:

- Public subnets
- Private application subnets
- Private data subnets

An Internet Gateway provides public connectivity to the public tier, while a NAT Gateway provides outbound connectivity for private workloads.

![VPC Resource Map](../screenshots/01-vpc-resource-map.png)

---

## 3. Security Groups

Dedicated security groups were created before deploying the application services:

- `project3-alb-sg`
- `project3-frontend-sg`
- `project3-api-sg`
- `project3-rds-sg`
- `project3-redis-sg`

The rules enforce the traffic chain:

```text
Internet -> ALB -> Frontend/API -> PostgreSQL/Valkey
```

![Security Groups](../screenshots/02-security-groups.png)

---

## 4. Managed Data Services

### PostgreSQL

Amazon RDS was provisioned as:

- Identifier: `project3-helpdesk-rds`
- Engine: PostgreSQL
- Database: `helpdesk`
- Port: `5432`
- Public internet access: disabled

### Valkey Cache

Amazon ElastiCache was provisioned as:

- Cache name: `project3-redis`
- Engine: Valkey
- Version: `9.1.0`
- Node type: `cache.t4g.micro`
- Port: `6379`

Both services were placed behind the API security boundary.

---

## 5. ECS Cluster & Task Definitions

The ECS cluster was created as:

`project3-helpdesk-cluster`

Two task definitions were prepared:

- `project3-helpdesk-frontend-task:1`
- `project3-helpdesk-api-task:1`

The frontend exposes container port `80`.

The API exposes container port `8000`.

AWS Fargate was selected so that the containers could run without managing EC2 container hosts.

---

## 6. Application Load Balancer

The internet-facing load balancer was created as:

`project3-helpdesk-alb`

Target groups:

- `project3-frontend-tg`
- `project3-api-tg`

Listener:

- Protocol: HTTP
- Port: `80`

Routing:

- Default `/` traffic -> frontend target group
- `/api/*` traffic -> API target group

API URL transformation:

```text
^/api/(.*)$ -> /$1
```

The API target-group health check was configured to use:

`/health`

![ALB Listener Routing](../screenshots/04-alb-listener-path-routing.png)

---

## 7. ECS/Fargate Services

Two ECS services were deployed:

### Frontend

- Service: `project3-frontend-service`
- Launch type: Fargate
- Desired tasks: `1`
- Public IP: disabled
- Target group: `project3-frontend-tg`

### API

- Service: `project3-api-service`
- Launch type: Fargate
- Desired tasks: `1`
- Public IP: disabled
- Target group: `project3-api-tg`

Both services eventually reached:

`1/1 Tasks running`

![ECS Cluster Services](../screenshots/07-ecs-cluster-services.png)

---

## 8. Target Health Validation

The load balancer registered private ECS task IP addresses as targets.

Validation confirmed:

- Frontend target on port `80` — Healthy
- API target on port `8000` — Healthy

![API Target Health](../screenshots/05-api-target-health.png)

![Frontend Target Health](../screenshots/06-frontend-target-health.png)

---

## 9. Database Initialization

The API health endpoint confirmed network connectivity to PostgreSQL and Valkey, but the ticket endpoint initially returned HTTP `500`.

CloudWatch logs revealed:

`relation "tickets" does not exist`

Because RDS was private, an AWS CloudShell VPC environment was used to connect to PostgreSQL.

The required `tickets` table was created in the `helpdesk` database.

After initialization, the ticket endpoint returned successfully and the application was able to persist ticket records.

---

## 10. End-to-End Application Validation

The final deployment was tested through the public ALB.

Validation included:

- Frontend rendering
- API routing
- Health endpoint
- PostgreSQL connectivity
- Valkey connectivity
- Ticket creation
- Ticket persistence
- Dashboard response
- Cached ticket retrieval

![Application Validation](../screenshots/13-helpdesk-application-validation.png)

![API Health](../screenshots/14-api-health-connectivity.png)

---

## 11. Observability

Amazon CloudWatch was used for runtime visibility.

Implemented items:

- API log group: `/ecs/project3-helpdesk-api`
- Runtime application logs
- ECS CPU metric monitoring
- Alarm: `project3-api-high-cpu-alarm`
- Threshold: CPU greater than `80%`

![CloudWatch Logs](../screenshots/11-cloudwatch-api-logs.png)

![CloudWatch CPU Alarm](../screenshots/12-cloudwatch-api-cpu-alarm.png)

---

## 12. Final Deployment State

At the end of deployment validation:

- ECS cluster: Active
- ECS services: 2 active
- Running tasks: 2
- Frontend target: Healthy
- API target: Healthy
- RDS PostgreSQL: Available
- Valkey cache: Available
- API health: Healthy
- Database connectivity: Connected
- Cache connectivity: Connected
- CloudWatch logs: Verified
- CPU alarm: Configured

The AWS environment remained running temporarily for evidence capture. The author subsequently reported deleting the paid services. The state listed above is historical, not current.

---

## Related Documentation

- [Architecture](architecture.md)
- [Networking](networking.md)
- [Security](security.md)
- [Observability](observability.md)
- [Troubleshooting](troubleshooting.md)
- [Validation](validation.md)

## Application Version and Schema Reference

See [application provenance and schema](application-provenance.md). The historical deployed image/source versions are unknown. The pinned current Docker reference must not be presented as a newly verified AWS deployment.
