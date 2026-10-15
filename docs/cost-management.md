# Cost Management & Operational Considerations

> **Deployment status:** Historical portfolio deployment, subsequently decommissioned. The author reports that paid AWS services were deleted. Screenshots and successful runtime results describe the earlier deployment, not a currently running environment. Current account inventory and billing have not been independently verified. This maintenance work is offline and does not recreate AWS resources.

## Purpose

This document records the cost-awareness practices used during the AWS deployment and the planned resource-cleanup process for this temporary portfolio environment.

The project was designed as a short-lived engineering lab rather than a permanent production workload, so cloud resources are retained only long enough to complete validation, documentation, and portfolio evidence.

---

## Cost-Control Approach

The following practices were used during the project:

- AWS Free Plan credits were used for temporary project resources.
- The deployment was kept in a single AWS Region: `ap-south-1`.
- ECS service desired count was limited to `1` task per service.
- Small RDS and ElastiCache instance classes were used.
- CloudWatch log retention was limited to one week.
- Unnecessary failed CloudFormation stacks were removed after troubleshooting.
- The temporary AWS deployment was subsequently decommissioned to avoid ongoing infrastructure charges.
- Billing information and payment-card details are not stored in this public repository.

---

## Billing Verification During Deployment

During project validation, the AWS Billing console showed:

- Estimated grand total: `USD 0.00`
- Free Plan: active
- Usage costs: covered by AWS credits

The zero estimated payment did not mean that AWS resources had no underlying usage cost. Running infrastructure still consumed billable AWS services, with credits covering the temporary project usage.

The temporary deployment was subsequently decommissioned. This document does not independently verify the current AWS account billing state.

---

## Main Cost-Sensitive Resources

The primary resources that can generate ongoing cost while the environment is running include:

| Resource | Project Usage |
|---|---|
| AWS Fargate | Runs frontend and API ECS tasks |
| Application Load Balancer | Public application ingress and routing |
| NAT Gateway | Outbound connectivity for private workloads |
| Amazon RDS PostgreSQL | Managed persistent database |
| Amazon ElastiCache for Valkey | Managed cache node |
| Amazon ECR | Container image storage |
| Amazon CloudWatch | Logs, metrics, and alarms |

The VPC and security-group design itself is not the main cost concern; the running compute, load-balancing, NAT, database, cache, storage, and monitoring resources require attention.

---

## Operational Resource Strategy

The AWS environment remained active temporarily after technical validation so that the following work could be completed first:

1. Architecture diagram creation
2. AWS console evidence capture
3. GitHub documentation
4. Recruiter-level repository review
5. Technical walkthrough and interview preparation

Deleting infrastructure before completing these activities would remove useful validation evidence.

---

## Final Cleanup Plan

The author reports that paid services were deleted. The following is a reference cleanup checklist, not an independently verified deletion log.

Reference checks for a future account review include:

1. Stop and remove ECS/Fargate services and running tasks.
2. Delete the Application Load Balancer after application evidence is complete.
3. Remove load-balancer target groups when no longer referenced.
4. Delete the RDS PostgreSQL instance after confirming no project data is required.
5. Delete the ElastiCache Valkey cache.
6. Remove NAT Gateway resources that are no longer required.
7. Review ECR repositories and remove images if the live AWS copies are no longer needed.
8. Review CloudWatch log groups and alarms.
9. Remove remaining project-specific network resources where appropriate.
10. Check AWS Billing and Cost Management for remaining active usage.

---

## Data Retention Before Cleanup

Before deleting managed data resources, the project evidence retained locally and in GitHub includes:

- Architecture diagram
- AWS console screenshots
- Deployment documentation
- Troubleshooting records
- Validation evidence
- Application behavior screenshots

The portfolio does not require the AWS environment to remain permanently online after this evidence has been captured.

---

## Billing Privacy

Billing and payment information is intentionally excluded from repository screenshots and documentation.

No bank-card details, payment-method information, account billing identifiers, or private billing screenshots should be committed to GitHub.

---

## Production Cost Improvements

For a long-lived production environment, cost optimization could include:

- AWS Budgets and cost alerts
- Rightsizing ECS task CPU and memory
- Rightsizing RDS and ElastiCache capacity
- Evaluating NAT Gateway traffic requirements and alternatives
- Log-retention tuning
- Storage lifecycle policies
- Savings Plans where predictable compute usage justifies them
- Cost allocation tags
- Regular AWS Cost Explorer review

> These are future production optimization options and are not presented as features implemented in this temporary portfolio deployment.

---

## Final Cost Verification

The following account-level checks cannot be established from this repository alone. They are not prerequisites for completing this offline documentation review:

- Chargeable temporary resources have been removed.
- ECS/Fargate tasks are no longer running.
- RDS and ElastiCache resources have been removed as planned.
- Load-balancing and NAT resources have been reviewed and cleaned up.
- Remaining AWS resources have been checked for unintended usage.
- The AWS Billing console has been reviewed one final time.

---

## Related Documentation

- [Architecture](architecture.md)
- [Networking](networking.md)
- [Deployment](deployment.md)
- [Validation](validation.md)
