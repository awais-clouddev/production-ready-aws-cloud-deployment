# Security Architecture

## Evidence Qualification

See [historical evidence scope](evidence-scope.md) and [production-control status](production-controls.md). Security-group tables record documented intent; the saved group-list screenshot does not establish exact rules or denied-path enforcement. Historical results are not current live checks.

> **Deployment status:** This portfolio deployment has been decommissioned. Screenshots and validation results document the original implementation. Reference configurations are provided for review; the environment is not currently hosted.

## Purpose

This document describes the security controls implemented for the AWS deployment, focusing on network isolation, security-group boundaries, private application workloads, managed data-service protection, and AWS access control.

The security model follows a layered approach in which each application tier accepts traffic only from the tier immediately in front of it.

![Security Groups](../screenshots/02-security-groups.png)

---

## Security Model

The deployed traffic path is:

```text
Internet
   |
   | HTTP 80
   v
Application Load Balancer
   |
   +---- TCP 80 ----> Frontend ECS/Fargate
   |
   +---- TCP 8000 --> API ECS/Fargate
                          |
                  +-------+-------+
                  |               |
             TCP 5432        TCP 6379
                  |               |
                  v               v
           RDS PostgreSQL    ElastiCache Valkey
```

No direct inbound path is provided from the internet to ECS tasks, PostgreSQL, or Valkey.

---

## Application Load Balancer Security Group

Security group:

`project3-alb-sg`

Inbound rule:

- Protocol: TCP
- Port: `80`
- Source: `0.0.0.0/0`

This security group allows public HTTP traffic only to the internet-facing Application Load Balancer.

The ALB is the public entry point for the application.

---

## Frontend Security Group

Security group:

`project3-frontend-sg`

Inbound rule:

- Protocol: TCP
- Port: `80`
- Source: `project3-alb-sg`

The frontend ECS/Fargate workload does not accept arbitrary internet traffic. Only traffic originating from the ALB security group can reach the frontend container.

---

## API Security Group

Security group:

`project3-api-sg`

Inbound rule:

- Protocol: TCP
- Port: `8000`
- Source: `project3-alb-sg`

The FastAPI service can therefore be reached through the Application Load Balancer but is not directly exposed to public clients.

---

## PostgreSQL Security Group

Security group:

`project3-rds-sg`

Inbound rule:

- Protocol: PostgreSQL/TCP
- Port: `5432`
- Source: `project3-api-sg`

Only the API workload can establish PostgreSQL connections to the RDS database.

The RDS database also has public internet access disabled.

![RDS Private Database](../screenshots/09-rds-postgresql-private-database.png)

---

## Valkey Security Group

Security group:

`project3-redis-sg`

Inbound rule:

- Protocol: TCP
- Port: `6379`
- Source: `project3-api-sg`

Only the API workload can communicate with the Redis-compatible Valkey cache.

The cache is deployed in the private data layer and encryption at rest is enabled.

![ElastiCache Valkey](../screenshots/10-elasticache-valkey-cache.png)

---

## Private ECS Workloads

Both ECS services run inside private application subnets:

- `project3-frontend-service`
- `project3-api-service`

Public IP assignment is disabled for both Fargate workloads.

The services are reached through private target IP addresses registered with the Application Load Balancer target groups.

This prevents direct inbound access to application containers from the public internet.

---

## Private Data Layer

PostgreSQL and Valkey are placed behind the API tier rather than exposed as public-facing services.

The intended trust boundaries are:

```text
Internet
   |
   v
ALB
   |
   +----> Frontend
   |
   +----> API
            |
            +----> PostgreSQL
            |
            +----> Valkey
```

The frontend has no direct database or cache access path.

---

## ECR Repository Controls

Amazon ECR repositories used by the deployment were configured with:

- Private repository visibility
- Immutable image tags
- AES-256 encryption

Repositories:

- `project3-helpdesk-frontend`
- `project3-helpdesk-api`

![ECR Repositories](../screenshots/08-ecr-private-repositories.png)

---

## AWS IAM

AWS Identity and Access Management is used for administrative access to AWS resources.

The project was operated using an IAM administrative identity rather than relying on the root account for normal project work.

MFA was configured as an additional account-access control.

IAM operates at the AWS control-plane layer and is separate from the application request path.

---

## Implemented Security Controls

- Dedicated custom VPC
- Public, private application, and private data network tiers
- Public IP disabled for ECS/Fargate workloads
- Internet-facing ALB used as the controlled application entry point
- Frontend accessible only from the ALB security group
- API accessible only from the ALB security group
- PostgreSQL accessible only from the API security group
- Valkey accessible only from the API security group
- RDS public internet access disabled
- Private ECR repositories
- ECR immutable tags
- ECR AES-256 encryption
- Valkey encryption at rest
- IAM-based AWS administrative access
- MFA configured for AWS account security

---

## Production Security Enhancements

For a long-lived production environment, additional hardening would include:

- HTTPS `443` using AWS Certificate Manager
- HTTP-to-HTTPS redirection
- Custom DNS/domain integration
- Encryption in transit for Valkey
- Centralized secrets management
- More restrictive outbound security-group rules where required
- AWS WAF for public application protection where justified
- Expanded CloudWatch security monitoring and notifications
- Automated security configuration through Infrastructure as Code

> These items are listed as production improvements and are not presented as controls implemented in this deployment.

---

## Evidence

- [Security Groups](../screenshots/02-security-groups.png)
- [Application Load Balancer](../screenshots/03-application-load-balancer-overview.png)
- [RDS PostgreSQL](../screenshots/09-rds-postgresql-private-database.png)
- [ElastiCache Valkey](../screenshots/10-elasticache-valkey-cache.png)

---

## Related Documentation

- [Architecture](architecture.md)
- [Networking](networking.md)
- [Deployment](deployment.md)
- [Observability](observability.md)
- [Validation](validation.md)
