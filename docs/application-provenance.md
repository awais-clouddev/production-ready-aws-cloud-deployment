# Application Provenance and Schema Reference

The AWS deployment is historical and was subsequently decommissioned.

## Historical Workload

The deployment used the Help Desk frontend/API and ECR repositories described in the deployment guide. The exact deployed source commit and immutable image digests were not retained in this repository. They are recorded as unknown, rather than reconstructed as facts.

## Current Offline Reference

The current reference source is Docker project commit `8d7345d675262a7042836594c39b57c5fa0fc3b2`:

https://github.com/awais-clouddev/containerized-help-desk-platform/tree/8d7345d675262a7042836594c39b57c5fa0fc3b2

This reference includes later Docker fixes. It does not establish that those fixes were deployed or tested in AWS.

Machine-readable provenance: [application-provenance.json](../reference/application-provenance.json).

## Schema Reference

The versioned [schema](../reference/database/schema.sql) is copied from the pinned reference source. Its SHA-256 is recorded in provenance.

Historical documentation records that a tickets table was created. The original executed SQL was not captured; this file is a current reference, not an authenticated export of that historical database.

## Initialization Procedure for a Future Authorised Deployment

1. Confirm the intended database, schema version and private access path.
2. Back up existing data and inspect existing objects before changes.
3. Use a controlled database session with ON_ERROR_STOP enabled and a transaction to apply a reviewed schema to an empty database.
4. Verify columns, constraints, permissions and ticket create/read/update behavior before opening application traffic.
5. Record the executed migration version and validation evidence.

CREATE TABLE IF NOT EXISTS is not a migration system: it does not repair an existing table with different columns or constraints.

No database connection or schema execution was performed in this offline maintenance work.
