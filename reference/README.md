# Offline Reference Configuration

These are newly authored reference templates, not exports of deleted AWS resources and not a complete deployment package. Do not submit them to AWS without separately authorised live work and review.

CPU/memory sizing, deployment circuit breaker, grace period, secret injection and IAM examples are reference choices, not claims about historical settings. Secret injection is a proposed improvement; historical central secrets management was not demonstrated.

All angle-bracket placeholders require verified replacements. Historical image digests remain unknown. Select and record future image digests; do not invent historical provenance.

Prerequisites include existing VPC/subnets/routes/security groups, ECS cluster, ECR images, log groups, target groups, ALB listeners, database/schema, cache and correctly reviewed IAM roles. Target groups must use IP targets for awsvpc tasks. API health checks use /health; frontend checks use /.

The API policy is illustrative and scoped to its image repository, log group and one secret. ECR authorization requires Resource '*'. Prepare a separate frontend policy limited to its repository/log group; do not grant it database secret access. Review customer-managed KMS key permissions if applicable. No application task role is included because this reference application does not require AWS API calls.

The API password secret is expected to contain the password as a plain secret string. Other secret formats require a deliberate task-definition change.

Single-task services remain an availability limitation. A rollback circuit breaker is not database recovery or proof of failover. HTTPS, Valkey TLS, replication and other production controls are not implemented by these files.

The network file records documented intent. It is not a security-group export. No IAM, networking or deployment behavior has been live-verified here.
