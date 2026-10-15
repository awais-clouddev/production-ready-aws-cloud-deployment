# Historical Evidence and Verification Scope

The deployment was subsequently decommissioned.
This review does not connect to AWS or verify current billing/inventory.
Original screenshots are preserved as historical evidence.

## What the Evidence Supports

| Evidence | Supported observation | Not established by that evidence alone |
|---|---|---|
| Security-group list | Named groups and descriptions existed | Actual ingress/egress rules or denied-path enforcement |
| ALB listener screenshot | HTTP listener, API path rule and URL rewrite | HTTPS, current routing or current availability |
| ECS services screenshot | Two services, one running task each | Cross-AZ task redundancy or demonstrated failover |
| RDS summary screenshot | PostgreSQL instance was available | Complete public-access, encryption, backup or failover configuration |
| Valkey details screenshot | One node; encryption at rest enabled; transit encryption, Multi-AZ and auto-failover disabled | Encrypted client connections or automatic cache failover |
| CloudWatch alarm screenshot | CPU threshold alarm with no actions | Notification delivery or an induced alarm/recovery test |
| API health screenshot | A successful dependency-health response was captured | Database schema readiness, all application operations or restricted network access |

The broader deployment guide records additional author-observed tests.
Those records remain historical reports, not newly repeated tests.
A successful connection does not prove that unauthorised connections are denied.

## Security-Group Interpretation

The source-group/port tables describe the documented intended boundaries.
The retained group-list screenshot is not a rule export.
No current AWS rule inventory or negative connectivity test is available.

Historical troubleshooting used a CloudShell VPC environment.
Its security-group attachment and any temporary administration rules were
not retained. Do not infer an undocumented permanent ingress rule.

## Application and Health Interpretation

The exact historical source commit/image digests are unknown.
Later Docker source improvements have not been deployed to this deleted AWS
environment. Browser health indicators alone are not independent proof that
all dependencies and application functions work.

The historical health-check incident records a change from / to /health.
It does not establish that / must fail in every version of the application.

## Verification Categories

- Historical observation: reported during the original deployment.
- Screenshot-supported: a visible field in preserved historical evidence.
- Offline checked: repository structure, links, JSON and internal consistency.
- Proposed reference: newly authored examples, never claimed as live exports.
- Requires future live verification: AWS permissions, routing, TLS, denied
  network paths, notifications, recovery, load behavior and failover.

These categories must not be substituted for one another.
