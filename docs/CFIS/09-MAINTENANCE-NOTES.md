# CFIS Maintenance Notes

Operational Guidelines and Procedures

**Document Version**: 1.0
**Last Updated**: February 2026

---

## Maintenance Strategy Overview

CFIS is in **extended maintenance mode**: focus is stability and compliance, not new feature development. Annual maintenance burden is estimated at 9-13 staff-years for bug fixes, compliance updates, and performance tuning.

---

## Critical Operational Procedures

### Daily Tasks

**Morning (8:00 AM)**:

- Check system availability (test login on all environments)
- Review overnight batch job logs
- Check error log for critical failures
- Verify database backups completed

**Evening (6:00 PM)**:

- Review pending tasks for escalation
- Ensure no critical issues unresolved
- Monitor batch job queue for next run

### Weekly Tasks (Monday)

- Review error log summary
- Check database performance metrics
- Validate integration endpoints (OnBase, CmoService)
- Test disaster recovery procedure (1x per week)

### Monthly Tasks

- Security audit (access logs, privilege changes)
- Capacity planning review
- Backup retention verification
- Update documentation for changes made

### Quarterly Tasks

- Full system backup test (restore to test environment)
- Performance baseline comparison
- Security patch assessment
- Dependency update review (PowerBuilder, .NET, SQL Server)

---

## Backup and Recovery

### Backup Schedule

**Database Backups**:

- Full: Sunday 22:00 (4 hours retention)
- Incremental: Daily 23:00 (7-day retention)
- Transaction log: Every hour (24-hour retention)

**File Backups**:

- Application libraries: Weekly (off-site)
- Configuration files: Daily (encrypted)
- Reports: Monthly archive (long-term)

**Backup Verification**:

- Automated restore test: Monthly
- Manual recovery drill: Quarterly
- Off-site backup verification: Semi-annually

### Recovery Procedures

**Recovery Time Objectives (RTO)**:

- Database: 2 hours
- Application: 1 hour
- Web servers: 30 minutes

**Recovery Point Objectives (RPO)**:

- Database: 1 hour (transaction log backup)
- Files: 4 hours (daily backup)
- Configuration: Same day

### Disaster Recovery Steps

1. **Assess Impact**
   - Determine what was lost
   - Estimate recovery time
   - Activate recovery team

2. **Recover Database**
   - Restore full backup
   - Apply transaction logs to current time
   - Verify data integrity
   - Estimated time: 90 minutes

3. **Recover Application**
   - Restore library files
   - Restore configuration
   - Restart services
   - Estimated time: 60 minutes

4. **Verify System**
   - Run system diagnostics
   - Test core workflows
   - Validate reports
   - Verify integrations

5. **Notify Users**
   - System status message
   - Estimated restoration time
   - Expected functionality limitations

---

## Performance Monitoring

### Key Metrics

**Database Health**:

- CPU usage: <70% normal, <85% peak
- Memory usage: <80% normal
- Disk space: >10% free (alert if <5%)
- Query response time: <1 second (95th percentile)

**Application Health**:

- Error rate: <0.1% of transactions
- Session count: Monitor growth trends
- Memory usage: <2GB per process
- Response time: <2 seconds (95th percentile)

**Integration Health**:

- OnBase availability: >99.5% uptime
- CmoService response: <5 seconds (95th percentile)
- Message queue depth: <100 (normal operation)
- Document upload success: >99%

### Monitoring Tools

**Database**:

- SQL Server Management Studio (native)
- Custom query for daily health check

**Application**:

- Event Viewer (application logs)
- Performance Monitor (CPU, memory)
- Custom error logging tables

**Network**:

- Ping tests to critical endpoints
- Connection monitoring for database
- Bandwidth utilization

### Alerting Thresholds

| Metric          | Warning | Critical | Action                              |
| --------------- | ------- | -------- | ----------------------------------- |
| CPU usage       | 70%     | 85%      | Review load, optimize queries       |
| Memory          | 80%     | 95%      | Restart services, review leaks      |
| Error rate      | 0.5%    | 2%       | Investigate, escalate               |
| Response time   | 3s      | 10s      | Check database, optimize            |
| OnBase downtime | 30m     | 2h       | Page on-call DBA                    |
| Message queue   | 500     | 1000     | Check CmoService, restart if needed |

---

## Common Troubleshooting

### Issue: Database Connection Failed

**Symptoms**:

- "Cannot connect to database" error
- Application unable to start
- Report generation fails

**Diagnosis**:

1. Test network connectivity: `ping dbserver`
2. Check SQL Server service: `sc query MSSQL$SQLEXPRESS`
3. Verify credentials: `sqlcmd -S dbserver -U cfis_user -P ****`
4. Check connection string in pb.ini

**Resolution**:

- Restart SQL Server service if stopped
- Verify firewall allows shared memory protocol
- Check user permissions on database
- Test with different database credentials

**Prevention**:

- Enable SQL Server failover/clustering
- Monitor service health automatically
- Test connections hourly via script

### Issue: Report Generation Times Out

**Symptoms**:

- Reports hang for >30 seconds
- User receives timeout error
- Browser connection closes

**Diagnosis**:

1. Check database query performance: Run EXPLAIN PLAN
2. Check CPU/memory usage during report
3. Check report complexity (number of joins)
4. Test with smaller date range

**Resolution**:

- Add database indexes for report queries
- Break complex reports into smaller queries
- Increase query timeout setting
- Archive old data to improve performance

**Prevention**:

- Monitor report performance weekly
- Implement query optimization reviews
- Set reasonable timeout thresholds

### Issue: OnBase Document Upload Fails

**Symptoms**:

- "Document upload failed" error
- COM object creation error
- OnBase unreachable

**Diagnosis**:

1. Test OnBase service: `ping onbase_server`
2. Verify COM registration: `regsvr32 /n OnBaseUnityUploadApi.dll`
3. Check network connectivity to OnBase
4. Review OnBase service logs

**Resolution**:

- Restart OnBase service if available
- Re-register COM object on client machine
- Check OnBase credentials/permissions
- Verify disk space on OnBase server

**Prevention**:

- Monitor OnBase service availability hourly
- Test document uploads daily
- Implement automatic retry logic

### Issue: Web Server Returns HTTP 500

**Symptoms**:

- "Server error" when accessing voter guides
- ASP.NET application crash
- Event logs show exceptions

**Diagnosis**:

1. Check Windows Event Viewer for details
2. Review IIS application pool status
3. Check database connectivity from web server
4. Review template files for syntax errors

**Resolution**:

- Restart IIS application pool
- Check database connectivity
- Review recent template changes
- Increase application pool timeout

**Prevention**:

- Monitor IIS health automatically
- Deploy templates to test environment first
- Implement automated error logging

---

## Change Management

### Change Request Process

1. **Initiation**
   - Document reason for change
   - Identify impact areas
   - Estimate effort

2. **Planning**
   - Determine test procedure
   - Plan rollback procedure
   - Schedule change window
   - Notify users

3. **Implementation**
   - Follow documented procedure
   - Monitor for errors
   - Log all steps taken

4. **Verification**
   - Test core functionality
   - Validate reports
   - Confirm integrations work
   - Get sign-off from stakeholders

5. **Closure**
   - Document lessons learned
   - Update procedures if needed
   - Close change ticket

### Change Blackout Windows

**No Production Changes**:

- Election day (±3 days)
- Filing deadlines (±2 days)
- Year-end financial close (Dec 20-Jan 10)
- Tax filing season (Feb 1-Apr 30)

---

## Update and Patch Management

### Prioritization Framework

| Update Type          | Priority | Testing          | Schedule   |
| -------------------- | -------- | ---------------- | ---------- |
| Security patches     | CRITICAL | Full suite       | ASAP       |
| Bug fixes            | HIGH     | Core functions   | Next cycle |
| SQL updates          | MEDIUM   | Performance test | Monthly    |
| PowerBuilder updates | LOW      | Compatibility    | Quarterly  |
| Feature requests     | LOW      | UAT required     | Annually   |

### Testing Requirements

**Security Patches**:

- No testing delay (deploy within 24 hours)
- Automated rollback on critical errors
- Monitor for failures post-deployment

**Bug Fixes**:

- Reproduce issue in test environment
- Verify fix resolves issue
- Regression testing on related features
- User acceptance testing (if user-facing)

**Feature Updates**:

- Development testing (unit/integration)
- Quality assurance testing (full suite)
- User acceptance testing (actual users)
- Performance testing (if applicable)

---

## Documentation Updates

### When to Update Procedures

After every change:

- Database schema change → Update data model docs
- Configuration change → Update configuration docs
- API change → Update API documentation
- User-facing change → Update user guides

### Documentation Standards

- Keep procedures up-to-date with actual system
- Include both normal and exception cases
- Provide examples and step-by-step instructions
- Include troubleshooting tips

---

## End-of-Life Planning

### Current Status

- **Technology**: 20+ years old (PowerBuilder 10.5)
- **Vendor Support**: No active vendor support for PB 10.5
- **Security**: Limited patching available
- **Maintenance**: Can continue indefinitely with effort

### Timeline Options

**Option A: Continue as-is**

- Annual maintenance: 9-13 staff-years
- Security risk increases yearly
- Staff expertise becomes rare
- End date: Open-ended

**Option B: Phased modernization (Recommended)**

- Years 1-2: Assessment and planning
- Years 2-4: Phased replacement
- Year 4+: New system in production
- Cost: $300,000-$500,000
- Benefit: Sustainable for next 15-20 years

**Option C: Rapid replacement**

- Year 1: Complete rewrite
- Cost: $500,000-$1,000,000
- Risk: High (complete system replacement)
- Benefit: Fastest time to modern platform

### Recommendation

**Execute Option B (Phased Modernization)**:

- Start: FY 2026 (6-12 month planning phase)
- Pilot: FY 2027 (proof of concept)
- Migration: FY 2028-2029 (phased rollout)
- Completion: FY 2029 (full production operation)

---

## Team Skills and Knowledge

### Required Expertise

- PowerBuilder 10.5 (5-10 remaining developers nationally)
- SQL Server database administration
- Campaign finance domain knowledge
- Document management (OnBase)
- ASP.NET web development

### Knowledge Transfer

- Document key algorithms and business rules
- Cross-train newer staff on critical functions
- Record video tutorials for complex processes
- Maintain runbooks for common tasks

### Risk Mitigation

- Identify single points of knowledge failure
- Plan for key person departure
- Cross-train all critical functions
- Document undocumented features

---

## Cost Estimation

### Annual Maintenance Budget

| Category         | FY 2026   | FY 2027   | FY 2028   |
| ---------------- | --------- | --------- | --------- |
| Staff (9-13 FTE) | $450K     | $450K     | $450K     |
| Infrastructure   | $100K     | $100K     | $100K     |
| Licenses/Support | $50K      | $50K      | $50K      |
| Tools/Utilities  | $25K      | $25K      | $25K      |
| **Total**        | **$625K** | **$625K** | **$625K** |

### Multi-Year Outlook

- Current trajectory: Sustainable through 2028
- Without modernization: Unsustainable after 2030
- Recommended action: Begin modernization planning in 2026

---

## Success Metrics

### Operational Excellence

- System uptime: >99.5%
- Mean time to resolution: <4 hours
- User satisfaction: >85%
- Security incidents: Zero (external attacks)

### Sustainability

- Documentation completeness: >90%
- Knowledge coverage: >80% of critical functions
- Staff expertise: 2+ developers per key area
- Annual budget: Within $±10% variance
