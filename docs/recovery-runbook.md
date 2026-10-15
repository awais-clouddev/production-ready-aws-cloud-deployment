# Recovery Runbook — Future Live Verification Required

This is a proposed procedure, not evidence of a completed AWS recovery drill.
The original deployment was decommissioned. Do not recreate resources during
this offline repository-maintenance task.

## Preparation

Before separately authorised live recovery, establish:

- A verified account/Region and explicit cost approval.
- Actual resource inventory, IAM permissions and network configuration.
- Exact application source and image digests.
- Backup availability, retention, encryption and permissions.
- Business recovery-point and recovery-time objectives.
- An isolated target environment and a rollback/cutover plan.

No particular recovery time or data-loss guarantee has been demonstrated.

## Database Recovery

1. Preserve the original source and available backups.
2. Select a verified snapshot or point-in-time recovery position.
3. Restore into a separate private database; do not overwrite the source.
4. Verify engine compatibility, schema, constraints, data and permissions.
5. Run ticket creation, retrieval, filtering and update tests.
6. Record actual elapsed recovery time and recovered-data timestamp.
7. Stop writes for a planned cutover, update application configuration,
   clear relevant cache data, and verify application behavior.
8. Retain the old environment until rollback is no longer required.

The Docker project's local restore drill is useful application-level evidence,
but it is not an RDS snapshot/PITR recovery test.

## ECS Recovery

Use recorded immutable image digests and reviewed task/service configuration.
Validate private networking, execution-role permissions, secret retrieval,
log delivery, target registration and health checks.

A deployment circuit breaker can roll back an ECS deployment; it does not
restore database data or prove application high availability.

## Cache Recovery

Treat PostgreSQL as authoritative. Rebuild or clear ticket cache entries
after database recovery. Test Redis-compatible client behavior and TLS if
enabled. A single-node historical cache did not demonstrate automatic failover.

## Verification and Evidence

Record exact versions, timestamps, target resources, test commands/results,
failure conditions, rollback results and cleanup. Test alert firing/resolution
and actual delivery separately if notifications are configured.

AWS routing, IAM enforcement, TLS, managed-service recovery and failover
remain unverified live in this repository-maintenance work.
