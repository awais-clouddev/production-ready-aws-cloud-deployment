# Troubleshooting & Incident Resolution

> **Deployment status:** Historical portfolio deployment, subsequently decommissioned. The author reports that paid AWS services were deleted. Screenshots and successful runtime results describe the earlier deployment, not a currently running environment. Current account inventory and billing have not been independently verified. This maintenance work is offline and does not recreate AWS resources.

## Purpose

This document records real failures encountered during the AWS deployment, how each problem was diagnosed, and the corrective action taken.

These incidents are included because troubleshooting and recovery are core Cloud/DevOps engineering responsibilities.

---

## Incident 1 — Frontend ECS Service Creation Failed

### Symptom

The first attempt to create `project3-frontend-service` failed during deployment.

### Root Cause

The ECS console deployment attempted to create a security group named `project3-frontend-sg`, but that security group already existed.

The associated CloudFormation deployment entered a failed state because the resource name already existed.

### Resolution

1. Identified the failed CloudFormation stack.
2. Deleted the failed stack.
3. Recreated the ECS service.
4. Selected the existing `project3-frontend-sg` instead of creating a new security group.
5. Verified that the frontend service deployed successfully.

### Result

`project3-frontend-service` reached a stable deployment with `1/1 Tasks running`.

---

## Incident 2 — Incorrect Frontend Subnet Selection

### Symptom

During frontend ECS service networking configuration, a private data subnet was accidentally selected.

### Risk

Application containers should run in the private application tier rather than the private data tier.

### Resolution

The incorrect subnet selection was caught before final deployment and changed to:

- `project3-private-app-a`
- `project3-private-app-b`

### Result

The frontend Fargate task was deployed into the intended private application network layer.

---

## Incident 3 — API ECS Service Creation Failed

### Symptom

The first API ECS service deployment failed.

### Root Cause

The ECS deployment attempted to create `project3-api-sg`, but that security group had already been created.

### Resolution

1. Identified the failed API CloudFormation stack.
2. Deleted the failed stack.
3. Recreated `project3-api-service`.
4. Selected the existing `project3-api-sg`.
5. Continued deployment using the correct private application subnets.

### Result

`project3-api-service` deployed successfully with `1/1 Tasks running`.

---

## Incident 4 — API Target Group Unhealthy

### Symptom

The API ECS task was running, but the Application Load Balancer target group did not become healthy.

### Investigation

The API application exposes its health endpoint at:

`/health`

The target group was initially checking:

`/`

### Root Cause

The Application Load Balancer health check was using the wrong application path.

### Resolution

Changed the `project3-api-tg` health-check path to:

`/health`

### Result

The API target became Healthy on port `8000`.

![API Target Health](../screenshots/05-api-target-health.png)

---

## Incident 5 — `/api/tickets` Returned HTTP 500

### Symptom

The API health endpoint returned successfully and reported both PostgreSQL and the cache as connected, but requesting `/api/tickets` produced an Internal Server Error.

### Investigation

CloudWatch application logs were inspected in:

`/ecs/project3-helpdesk-api`

The logs showed the PostgreSQL error:

```text
psycopg2.errors.UndefinedTable: relation "tickets" does not exist
```

### Root Cause

Network connectivity to RDS was working, but the application database schema had not been initialized. The required `tickets` table did not exist.

### Resolution

Because the RDS database was private, an AWS CloudShell VPC environment was used to access the database privately.

A PostgreSQL session was established to the `helpdesk` database and the required `tickets` table was created.

### Result

After database initialization:

- `/api/tickets` returned successfully
- Ticket creation succeeded
- Ticket persistence was verified
- The frontend displayed the stored ticket

---

## Incident 6 — End-to-End Validation Required

### Situation

Individual infrastructure components were healthy, but component health alone did not prove that the entire application path worked.

### Validation Performed

The deployment was tested across the complete request path:

```text
Browser
   |
   v
Application Load Balancer
   |
   +----> Frontend ECS/Fargate
   |
   +----> API ECS/Fargate
             |
             +----> RDS PostgreSQL
             |
             +----> ElastiCache Valkey
```

Tests included:

- Frontend page load
- API health endpoint
- Ticket creation
- Ticket retrieval
- PostgreSQL persistence
- Dashboard endpoint
- Cached ticket retrieval
- CloudWatch log verification

### Result

The complete application path was successfully validated.

![Application Validation](../screenshots/13-helpdesk-application-validation.png)

![API Health](../screenshots/14-api-health-connectivity.png)

---

## Troubleshooting Approach Used

Across these incidents, the troubleshooting process followed a repeatable pattern:

1. Identify the failing AWS component or application endpoint.
2. Separate infrastructure health from application health.
3. Inspect ECS deployment state, target health, security groups, networking, and CloudWatch logs.
4. Use the most specific error message available.
5. Correct the smallest failing configuration or dependency.
6. Retest the affected component.
7. Perform end-to-end validation after the local issue is resolved.

---

## Engineering Lessons

- A running ECS task does not automatically mean the application is healthy.
- Load-balancer health-check paths must match real application endpoints.
- Security groups should be reused deliberately when they already exist.
- Application workloads and data services should remain in their intended network tiers.
- Successful database connectivity does not guarantee that the application schema exists.
- CloudWatch logs are essential for distinguishing infrastructure failures from application/database failures.
- End-to-end testing is required even when every AWS console resource appears healthy.

---

## Related Documentation

- [Deployment](deployment.md)
- [Observability](observability.md)
- [Validation](validation.md)
- [Security](security.md)
