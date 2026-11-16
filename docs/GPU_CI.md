# GPU CI: design only, not executed

This CLI has no GPU functionality. The following is an extension design for a
future GPU workload; no GPU instance was rented and no GPU cost was incurred.
All prices USD, sources retrieved 2026-11-16; capacity is not reserved.

| Option | GPU / deployment | Rate | Eligibility / caveat |
|---|---|---|---|
| GitHub larger Linux GPU runner | Managed GPU runner | $0.052/min = $3.12/h | Organization on Team or Enterprise Cloud; larger runners not free for public repos |
| Runpod Pod | Ephemeral A40, 48 GB | Listed $0.59/h | GPU cloud account, billing and available stock required; selected cloud/region must be confirmed at launch |
| AWS EC2 G4dn | Ephemeral NVIDIA T4 worker | UNVERIFIED ESTIMATE $0.526/h | AWS account, regional GPU quota and capacity; opened instance page did not expose a verifiable numeric quote |

Sources:
- https://docs.github.com/en/billing/reference/actions-runner-pricing
- https://docs.github.com/en/actions/concepts/runners/larger-runners
- https://www.runpod.io/pricing
- https://aws.amazon.com/ec2/instance-types/g4/

## Transparent monthly model

One GPU per job; 30-day month. Successful job minutes include provisioning and
teardown. Failed-attempt fraction p, maximum one retry; expected additional
failed-attempt cost is conservatively budgeted as p times a full job.
Formula: compute hours = (release runs + active nightly runs) * minutes / 60 * (1+p).
Low: (2+10) * 10/60 * 1.05 = 2.10 h.
Base: (4+30) * 20/60 * 1.10 = 12.47 h.
High: (8+30) * 40/60 * 1.25 = 31.67 h.

| Option | Low | Base | High |
|---|---:|---:|---:|
| GitHub compute | $6.55 | $38.90 | $98.80 |
| Runpod compute | $1.24 | $7.36 | $18.68 |
| AWS compute, UNVERIFIED ESTIMATE | $1.10 | $6.56 | $16.66 |

Exclude taxes, storage, transfer, GitHub plan subscription and engineering time.
Allocate another $5/$10/$25 monthly reserve respectively; these are planning
assumptions, not provider prices. GPU types are not performance-equivalent;
measure workload duration before choosing a provider. Base choice: disposable
Runpod A40 if workload fits; managed GitHub if organizational eligibility and
reduced operations work justify the price. AWS integrates IAM/OIDC well but
needs a current regional quote before a spending decision.

## Execution and cost limits

Release GPU job depends on successful CPU tests and verified build, then downloads
that exact artifact. Nightly compares HEAD to last successful GPU-tested SHA;
no new commit means no machine allocation. Never attach untrusted fork code to
a privileged persistent self-hosted runner.

Provision one-use runner from a reviewed image, register it as ephemeral, use
short-lived narrowly scoped credentials where supported and delete it after
one job. Within about 60 seconds run nvidia-smi, framework device detection,
one allocation and a tiny computation; missing GPU fails immediately.
Limit job to 45 minutes and allocation TTL to 60. Release concurrency preserves
the running release; newer nightly work cancels older nightly work. An independent
watchdog terminates idle instances and expired leases even if Actions is offline.
Do not rely only on an in-job cleanup trap: runner crashes can bypass it.

Spot/preemptible mode is optional after verifying provider support and pricing.
Checkpoint long tests; retry interruptions at most once within budget. Alert at
50%, 80%, 100% of a $60 monthly pilot budget and disable new allocations at 100%.
No claim that billing alerts alone enforce a spending cap.
