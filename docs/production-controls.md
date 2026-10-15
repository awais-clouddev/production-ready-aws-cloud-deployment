# Production Controls and Accepted Lab Limits

This is an independent, decommissioned portfolio lab.
No production services are being recreated during repository maintenance.

| Control | Historical/repository status | Future live verification |
|---|---|---|
| HTTP ALB routing | Historical routing evidence retained | Verify routes, rewrite and health checks |
| HTTPS and HTTP redirect | Not demonstrated; future improvement | Certificate, redirect and TLS tests |
| Private workloads and data tiers | Documented design; complete exports unavailable | Inspect routes, public-IP settings and permitted/denied paths |
| Application authentication/authorisation | Not demonstrated | Required before real-user data/access |
| Central secrets management | Not historically demonstrated; proposed reference template only | Secret retrieval and least-privilege permissions |
| Valkey encryption at rest | Enabled in historical screenshot | Inspect new environment |
| Valkey encryption in transit | Disabled in historical screenshot | Enable TLS and verify client behavior before production use |
| RDS transport/storage encryption | Complete configuration not established here | Inspect settings and verify encrypted connections |
| Application availability | One task per service | Redundancy, rollout and failure testing |
| Database availability | No database failover demonstration retained | Inspect chosen topology and test recovery/failover |
| Cache availability | One node; Multi-AZ/auto-failover disabled | Replication/failure tests if required |
| Logging | Historical API CloudWatch logs | Verify current delivery, retention and permissions |
| CPU alarm | Historical monitoring-only alarm; no actions | Induce alarm/resolution and test delivery if configured |
| Backup and disaster recovery | Procedures proposed; no AWS restore drill established | Restore into isolated target and validate application data |
| IAM least privilege | Historical full policies unavailable; illustrative policy added | Review actual policies and allowed/denied operations |
| Cost closure | Paid-service deletion reported by author | Account inventory/billing review remains separate |

Network segmentation is not application authentication or encryption.
Multi-AZ subnet placement alone is not application or database high availability.
A persistent database is not a tested backup.

Acceptance for this portfolio means documenting these limits accurately,
not claiming that production controls were implemented offline.
