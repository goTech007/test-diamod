# Architecture for 1200 Email Addresses Outreach System

## Overview

This architecture supports 1200 email addresses for outreach campaigns across multiple clients and directions, prioritizing cost efficiency and high fault tolerance.

## Architecture Description

### Core Components

**1. Email Service Layer (SMTP Servers)**
- **Primary**: Multiple SMTP providers (SendGrid, Mailgun, AWS SES) with failover
- **Distribution**: 1200 addresses split across 3-4 providers (~300-400 per provider)
- **Rationale**: Diversification reduces single-point-of-failure risk and provider rate limits

**2. Load Balancer & Router**
- **Service**: Nginx reverse proxy or AWS Application Load Balancer
- **Function**: Distributes email sending requests across SMTP providers
- **Health Checks**: Monitors provider availability and response times

**3. Queue System**
- **Service**: Redis Queue (RQ) or AWS SQS
- **Function**: Asynchronous email queuing with retry logic
- **Benefits**: Prevents overload, enables retry on failures, decouples sending from application

**4. Monitoring & Logging**
- **Services**: Prometheus + Grafana (self-hosted) or CloudWatch
- **Metrics**: Delivery rates, bounce rates, provider health, queue depth
- **Alerts**: Email/SMS notifications for critical failures

**5. Database**
- **Service**: PostgreSQL (self-hosted on VPS) or AWS RDS (small instance)
- **Function**: Stores email addresses, client mappings, campaign data, delivery logs

## Services and Approaches

### Email Providers Strategy
- **SendGrid**: 400 addresses (free tier: 100/day, paid: $15/month for 40k emails)
- **Mailgun**: 400 addresses (free tier: 100/day, paid: $35/month for 50k emails)
- **AWS SES**: 400 addresses (pay-as-you-go: $0.10 per 1000 emails)
- **Backup Provider**: Resend or Postmark for failover

### Infrastructure Approach
- **Compute**: 2x small VPS instances (Hetzner/DigitalOcean: $6-12/month each)
  - Instance 1: Application server + Redis
  - Instance 2: Database + Monitoring stack
- **CDN/DNS**: Cloudflare (free tier) for domain management and DDoS protection
- **Backup**: Automated daily backups to S3-compatible storage (Backblaze B2: ~$0.005/GB)

## Rotation and Monitoring

### Email Address Rotation
- **Algorithm**: Round-robin with weighted distribution based on provider health
- **Implementation**: 
  - Each client/direction mapped to provider pool
  - Rotates addresses within pool to avoid rate limits
  - Tracks daily sending limits per address (e.g., 50-100 emails/day)
- **Smart Routing**: Routes to healthiest provider; auto-switches on failure

### Monitoring System
- **Real-time Dashboards**: 
  - Provider health status (uptime, response time)
  - Queue depth and processing rate
  - Delivery success/failure rates per provider
  - Daily sending volume per address
- **Alerting Rules**:
  - Provider down > 5 minutes → Alert + failover
  - Queue depth > 1000 → Alert
  - Bounce rate > 10% → Alert + pause sending
  - Daily limit reached → Auto-rotate to next provider

## Load Distribution

### Horizontal Distribution
- **By Provider**: 1200 addresses split across 3-4 providers (300-400 each)
- **By Client**: Each client assigned to specific provider pool
- **By Direction**: Different campaigns use different provider sets

### Vertical Distribution (Time-based)
- **Rate Limiting**: Max 50-100 emails per address per day
- **Throttling**: Distributed sending over 24 hours (not burst)
- **Queue Processing**: Processes 10-20 emails/minute per provider

### Failover Mechanism
- **Primary → Secondary**: Automatic switch on provider failure
- **Health Check Interval**: Every 30 seconds
- **Retry Logic**: 3 retries with exponential backoff (1min, 5min, 15min)

## Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Provider Outage** | High | Multi-provider setup with automatic failover; backup provider ready |
| **Rate Limiting** | Medium | Distributed sending, daily limits per address, queue throttling |
| **IP Reputation** | High | Separate IP pools per provider; warm-up process for new addresses |
| **Domain Blacklisting** | High | Multiple domains per client; SPF/DKIM/DMARC configured |
| **Data Loss** | Medium | Daily automated backups; database replication to backup server |
| **Cost Overrun** | Low | Usage monitoring with alerts; hard limits on monthly spend |
| **Single Point of Failure** | High | Redundant VPS instances; database replication; load balancer HA |

### Additional Safeguards
- **Email Warm-up**: Gradual increase in sending volume for new addresses
- **Bounce Handling**: Automatic removal of hard bounces; quarantine for soft bounces
- **Compliance**: GDPR/opt-out handling; unsubscribe links in all emails
- **Security**: API keys stored in environment variables; encrypted database connections

## Cost Estimate

### Monthly Costs

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| **SendGrid** | 40k emails/month | $15 |
| **Mailgun** | 50k emails/month | $35 |
| **AWS SES** | 40k emails/month | $4 |
| **VPS Instances** | 2x 2GB RAM (Hetzner) | $12 |
| **Database** | Included in VPS | $0 |
| **Redis** | Included in VPS | $0 |
| **Monitoring** | Self-hosted (Prometheus/Grafana) | $0 |
| **Backup Storage** | Backblaze B2 (50GB) | $0.25 |
| **Domain/DNS** | Cloudflare (free) | $0 |
| **Total** | | **~$66.25/month** |

### Annual Cost: ~$795/year

### Cost Optimization Notes
- Can reduce to ~$40/month by using more free tiers (100/day per provider = 300/day total)
- AWS SES is most cost-effective for high volume ($0.10 per 1000 emails)
- Self-hosting monitoring/database saves ~$50-100/month vs. managed services
- Scaling: Add providers incrementally as volume grows

## Summary

This architecture achieves high fault tolerance through multi-provider redundancy, automatic failover, and comprehensive monitoring. Cost is minimized by leveraging free tiers, self-hosting non-critical components, and using pay-as-you-go services. The system can handle 1200 email addresses across multiple clients and directions while maintaining 99.9% uptime through intelligent rotation and failover mechanisms.

