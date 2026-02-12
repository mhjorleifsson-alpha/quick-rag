# CFIS Dependencies

Complete Application Dependency Analysis

**Document Version**: 1.0
**Last Updated**: February 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Runtime Dependencies](#runtime-dependencies)
3. [Library Dependencies](#library-dependencies)
4. [Database Dependencies](#database-dependencies)
5. [External Dependencies](#external-dependencies)
6. [System Requirements](#system-requirements)
7. [Dependency Conflicts](#dependency-conflicts)
8. [Maintenance Considerations](#maintenance-considerations)

---

## Overview

CFIS has a complex dependency structure spanning:

- **Runtime Environments**: PowerBuilder, .NET Framework, SQL Server
- **System Libraries**: 28 PowerBuilder libraries with interdependencies
- **External Services**: OnBase, CmoService, multiple database servers
- **Framework Requirements**: ASP.NET, COM interop, ODBC drivers

### Dependency Matrix

```
Application Layer
    |
    ├─ PowerBuilder Runtime (v10.5+)
    |  └─ Sybase/Appeon Runtime
    |
    ├─ .NET Framework (2.0+)
    |  └─ System.Web.Services
    |  └─ System.Configuration
    |
    └─ Windows Components
       └─ COM Runtime (DCOM)
       └─ ODBC Driver Manager
```

---

## Runtime Dependencies

### PowerBuilder Runtime

**Version**: PowerBuilder 10.5 or compatible
**Appeon Runtime**: 21.0.0.1509 (from cfis.xml)

**Requirements**:

- Sybase/Appeon PowerBuilder Runtime installed on client machines
- Runtime must be compatible with PowerScript language features used
- Must support library loading from 28 interconnected .pbl files
- Requires database connectivity drivers (DB2, Sybase, ODBC)

**Installation Path**:

```
C:\Program Files (x86)\Sybase\PowerBuilder 10.5
C:\Program Files (x86)\Appeon\Common\PowerBuilder\Runtime 21.0.0.1509
```

**Critical Files**:

- pb.ini: PowerBuilder configuration
- pbrun.exe: Runtime engine
- pbvm.dll: Virtual machine
- Debugger support libraries

### .NET Framework

**Version**: 2.0 or later (implied from ASP.NET version)
**Components**:

- System.Web.Services (SOAP support)
- System.Configuration (AppSettings)
- System.Xml.Serialization (Web service proxies)
- System.Web.Services.Protocols (SOAP protocol)

**Required for**:

- CmoService SOAP proxy (generated from WSDL)
- ASP.NET web application hosting
- XML configuration parsing
- Async/await patterns

**Verification Command**:

```powershell
reg query "HKLM\Software\Microsoft\NET Framework Setup\NDP" /s
```

### Windows Components

**COM Runtime (DCOM)**:

- Enables PowerBuilder-to-OnBase integration
- OnBaseUnityUploadApi.dll registration via COM
- Required for document management operations
- Must be enabled on domain networks

**ODBC Driver Manager**:

- Manages connections to multiple database versions
- Supports legacy database connectivity
- Required for DSN configuration
- Connection pooling support

---

## Library Dependencies

### PowerBuilder Library Dependency Graph

#### Tier 1: Foundation Libraries (No dependencies)

```
Cfisstru.pbl (160KB)
└─ Data type definitions
└─ Structure templates
└─ Enumeration definitions
```

#### Tier 2: Infrastructure Libraries (Depend on Tier 1)

```
Cfisbase.pbl (356KB)
├─ Depends: Cfisstru.pbl
└─ Base object definitions
└─ Global variables
└─ Error handling
```

```
Cfisutil.pbl (3.8MB)
├─ Depends: Cfisbase.pbl
└─ Utility functions
└─ String manipulation
└─ Date/currency conversion
```

```
Cfisuobj.pbl (194KB)
├─ Depends: Cfisbase.pbl
└─ User-defined object (UDO) definitions
└─ Custom control classes
└─ Reusable components
```

#### Tier 3: Core Services (Depend on Tier 2)

```
Cfisfn.pbl (963KB)
├─ Depends: Cfisutil.pbl, Cfisbase.pbl
└─ Core business functions
└─ Data access wrappers
└─ Transaction processing
```

```
cfisdyn.pbl (564KB)
├─ Depends: Cfisbase.pbl
└─ Dynamic object creation
└─ Runtime object instantiation
└─ Reflection-like capabilities
```

```
Cfisconv.pbl (3.5MB)
├─ Depends: Cfisutil.pbl
└─ Data conversion utilities
└─ Format transformation
└─ Import/export preprocessing
```

#### Tier 4: Business Logic (Depend on Tier 3)

```
cfiscand.pbl (11.7MB)
├─ Depends: Cfisfn.pbl, Cfisutil.pbl
└─ Candidate management operations
└─ Committee lifecycle
└─ Filing status tracking
```

```
cfispmt.pbl (26.9MB)
├─ Depends: Cfisfn.pbl, Cfisutil.pbl
└─ Payment processing
└─ Financial transaction operations
└─ Check reconciliation
```

```
cfiscont.pbl (2.1MB)
├─ Depends: Cfisfn.pbl
└─ Contribution tracking
└─ Receipt recording
└─ Contribution categorization
```

```
cfisintk.pbl (44.9MB - LARGEST)
├─ Depends: Cfisconv.pbl, Cfisfn.pbl, Cfisutil.pbl
└─ Data intake processing
└─ File import pipeline
└─ Batch operation coordination
└─ Error recovery
```

```
cfismail.pbl (1.7MB)
├─ Depends: Cfisfn.pbl
└─ Email and messaging
└─ Notification sending
└─ Message composition
```

#### Tier 5: Tracking Modules (Depend on Tier 4)

```
cfisatrk.pbl (29.0MB)
├─ Depends: Cfisfn.pbl
└─ Account tracking
└─ Account reconciliation
└─ Ledger management
```

```
cfisdtrk.pbl (4.9MB)
├─ Depends: Cfisfn.pbl
└─ Deposit tracking
└─ Bank reconciliation
└─ Deposit scheduling
```

```
cfislegtrk.pbl (1.5MB)
├─ Depends: Cfisfn.pbl
└─ Legislative tracking
└─ Official reference data
└─ Ballot measure tracking
```

```
cfistrntrk.pbl (3.2MB)
├─ Depends: Cfisfn.pbl
└─ Transaction tracking
└─ Transaction queries
└─ Query optimization
```

```
cfisvgtrk.pbl (10.1MB)
├─ Depends: Cfisfn.pbl
└─ Voter guide tracking
└─ Public page generation
└─ Template coordination
```

#### Tier 6: Reporting and UI (Depend on Tier 4-5)

```
cfisrptm.pbl (39.2MB)
├─ Depends: Cfisfn.pbl, Cfisutil.pbl
└─ Main reporting module
└─ Report coordination
└─ Report scheduling
```

```
cfisrptd.pbl (55.1MB - LARGEST SINGLE)
├─ Depends: cfisrptm.pbl, Cfisfn.pbl
└─ Detailed reporting
└─ Complex calculations
└─ PDF/Excel generation
```

```
cfisrptw.pbl (32.7MB)
├─ Depends: cfisrptm.pbl
└─ Web reporting interface
└─ HTML output generation
└─ XML data export
```

```
Cfisform.pbl (7.8MB)
├─ Depends: Cfisuobj.pbl, Cfisutil.pbl
└─ Form components
└─ UI controls
└─ Window management
```

```
Cfissrch.pbl (4.5MB)
├─ Depends: Cfisfn.pbl
└─ Search functionality
└─ Query optimization
└─ Result caching
```

```
Cfisdddw.pbl (1.5MB)
├─ Depends: Cfisutil.pbl
└─ Data display windows
└─ DataWindow control customization
└─ Rendering optimization
```

#### Tier 7: Application Framework (Depend on Tier 1-6)

```
cfisapp.pbl (3.1MB)
├─ Depends: All Tier 1-6 libraries
└─ Application framework initialization
└─ Library loading coordination
└─ Configuration management
└─ Global state initialization
```

```
cfisids.pbl (350KB)
├─ Depends: Cfisbase.pbl
└─ ID and reference management
└─ Unique identifier generation
└─ Reference data caching
```

#### Tier 8: Administrative and Special Purpose

```
cfisadm.pbl (2.8MB)
├─ Depends: cfisapp.pbl, Cfisfn.pbl
└─ Administrator tools
└─ System configuration
└─ User management
└─ Batch operations
```

```
cfiscvsm.pbl (6.4MB)
├─ Depends: Cfisfn.pbl
└─ Content and Version Sync Management
└─ Data synchronization
└─ Version control
└─ Replication support
```

### Circular Dependency Analysis

**CRITICAL**: No circular dependencies detected

- Library loading order is strictly hierarchical
- Tier-based structure prevents circular references
- Safe for incremental deployment and testing

---

## Database Dependencies

### SQL Server Version Support

**Supported Versions**:

- SQL Server 2000 (db2000) - Legacy support
- SQL Server 2003 (db2003) - Extended support
- SQL Server 2005 (db2005, db2005x) - Primary production
- SQL Server 2007 (db2007, db2007a, db2007b) - Extended instances
- SQL Server 2008 (db2008) - Extended support
- SQL Server 2009 (db2009) - Extended support
- SQL Server 2010 (db2010) - Current support
- SQL Server 2012 (db2012) - Current support

**Database-Specific Features Used**:

**T-SQL Features (2000+)**:

- Stored procedures
- Triggers
- Views
- Constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE)
- Indexes

**T-SQL Features (2005+)**:

- Common Table Expressions (CTEs)
- XML data type (if used)
- Ranking functions
- Snapshot isolation

**Connection Protocol**:

- Shared Memory (primary, local network)
- Named Pipes (alternative, local network)
- TCP/IP (not typical for internal connections)

**ODBC Drivers Required**:

- ODBC Driver 17 for SQL Server (recommended)
- ODBC Driver 13 for SQL Server (supported)
- SQL Server Native Client (legacy support)
- Driver version must match database version

### Database Schema Dependencies

**Schema Objects**:

```
candidate_master_table
    ├─ Primary Key: Cand_ID
    └─ Foreign Keys:
        ├─ → election_cycle_table
        └─ → office_type_table

committee_table
    ├─ Primary Key: Comm_ID
    ├─ Foreign Key: Cand_ID → candidate_master_table
    └─ Foreign Key: Bank_Acct → bank_accounts_table

financial_transaction_table
    ├─ Composite Key: (Election_Cycle, Cand_ID, Transaction_ID)
    ├─ Foreign Keys:
    │  ├─ → candidate_master_table
    │  ├─ → purpose_codes_table
    │  ├─ → agency_codes_table
    │  └─ → borough_codes_table
    └─ Indexes:
       ├─ (Election_Cycle, Cand_ID, Trans_Date) - for reporting
       ├─ (Trans_Date, Amount) - for range queries
       └─ (Purpose_CD, Amount) - for categorization

contributor_address_table
    ├─ Foreign Key: Transaction_ID → financial_transaction_table
    └─ Indexed on (Cand_ID, Trans_Date) for searches

audit_trail_table
    ├─ Composite Key: (Audit_ID, Table_Name, Record_ID)
    ├─ Indexed on (Changed_Timestamp, Changed_By)
    └─ For compliance and change tracking
```

**Stored Procedure Dependencies**:

- Reporting procedures (call candidate, transaction, committee procedures)
- Data entry procedures (validate, insert, update)
- Audit procedures (log changes, track modifications)
- Maintenance procedures (cleanup, optimization)

---

## External Dependencies

### OnBase Document Management

**Component**: OnBaseUnityUploadApi.dll
**Version**: Compatible with OnBase 2010+
**Interface**: COM object (requires registration)

**Dependency Details**:

```
PowerBuilder Application
    │
    ├─ OnBaseUnityUploadApi.dll (COM Server)
    │  └─ OnBase Client Runtime (local installation)
    │     └─ OnBase Server (network service)
    │        └─ Document Storage (file system or database)
    │
    └─ Configuration
       └─ OnBase connection string
       └─ Document repository settings
       └─ Workflow definition references
```

**Required Methods** (from COM interface):

- Upload: Document submission to repository
- Download: Document retrieval from repository
- Search: Query by metadata
- Delete: Remove document (with audit trail)
- GetMetadata: Extract document properties

**Connection Pooling**:

- Connection string stored in configuration
- Pooling enabled for performance
- Timeout: typically 30 seconds per operation
- Retry logic for transient failures

### CmoService SOAP Integration

**Endpoint**: http://c-accessprod:8007/CAccess/CmoService/
**Protocol**: SOAP over HTTP
**Transport**: Asynchronous capable

**Service Methods** (from CmoService.cs):

1. PostMessage(electionCycle, candidateID, creator, title, body, receiptEmail, attachmentData, attachmentName, notify)
2. PostPaymentLetter(...)
3. PostPaymentLetterByPath(...)
4. PostTollingLetter(...)
5. PostInitialDocumentRequest(...)
6. PostDraftAuditReport(...)
7. PostFinalAuditReport(...)
8. PostStatementReview(...)

**Configuration Override**:

```xml
<!-- AppSettings in App.config -->
<appSettings>
    <add key="EndpointURL" value="http://c-accessprod:8007/CAccess/CmoService/" />
</appSettings>
```

**Async Handling**:

```csharp
// Generated from WSDL
public event PostMessageCompletedEventHandler PostMessageCompleted;
public void PostMessageAsync(string electionCycle, string candidateID, ...);
public void EndPostMessage(IAsyncResult asyncResult, out int result, out bool resultSpecified);
```

**Dependency Chain**:

- .NET Framework with System.Web.Services
- Proxy class auto-generated from WSDL
- Requires network access to http://c-accessprod:8007
- Message queue at remote CmoService endpoint
- Background worker process at CmoService

---

## System Requirements

### Development Environment

**PowerBuilder IDE**:

- PowerBuilder 10.5 (original development)
- PowerBuilder 2019+ (for maintenance and modernization)
- Sybase/Appeon licensing

**Visual Studio** (for ASP.NET components):

- Visual Studio 2005 or later
- .NET Framework 2.0 SDK
- WSDL.exe tool for proxy generation

**Database Tools**:

- SQL Server Management Studio (current version)
- SQL Server Express (local testing)
- Database migration tools for multi-version support

**OnBase** (for integration testing):

- OnBase 2010+ client installation
- OnBase administrative tools
- Document repository access

### Runtime Environment

**Server Requirements**:

- Windows Server 2008 R2 or later
- 8GB RAM minimum (16GB recommended for reporting workloads)
- 500GB disk for database and documents
- SQL Server 2012 or later (Enterprise or Standard)

**Client Requirements**:

- Windows 7 or later
- PowerBuilder 10.5 runtime
- .NET Framework 2.0 or later
- 2GB RAM minimum
- 50MB disk for application

**Network**:

- LAN with Shared Memory support (local connections)
- HTTP/HTTPS for web access
- DNS resolution for database server names
- VPN for remote access

### Third-Party Libraries

**PowerBuilder Standard Libraries**:

- pbstring.pbl (string functions)
- pbarray.pbl (array functions)
- pbupdates.pbl (UI updates)

**ASP.NET Standard**:

- System.Web (web framework)
- System.Web.UI (controls)
- System.Data (database access)

---

## Dependency Conflicts

### Known Conflicts

**SQL Server Version Compatibility**:

- SQL Server 2000: Legacy, removed from Windows Server 2016+
- SQL Server 2003: Custom build (not standard product)
- SQL Server 2005-2008: Extended support ended
- SQL Server 2012: Standard support ends Oct 2022

**Recommendation**: Migrate to SQL Server 2016+ for current support

**PowerBuilder Version Conflicts**:

- PowerBuilder 10.5: 20+ years old, no longer supported
- Appeon Runtime 21.0: Compatible but requires updates
- .NET Framework 2.0: Deprecated, recommend 4.6+

**Recommendation**: Plan modernization to PowerBuilder 2022+

**COM Interop Issues**:

- OnBaseUnityUploadApi.dll: Requires 32-bit or 64-bit architecture consistency
- Registration: May fail on UAC-enabled systems
- Deployment: Manual registration on each machine

**Recommendation**: Automate registration via PowerShell or Group Policy

### Resolution Strategies

**For SQL Server Upgrades**:

1. Run compatibility checker on current SQL Server version
2. Backup all databases before upgrade
3. Test reporting queries on target version
4. Verify stored procedure compatibility
5. Update connection strings

**For PowerBuilder Modernization**:

1. Identify deprecated language features
2. Test in PowerBuilder 2019 IDE (backward compatibility mode)
3. Resolve compilation errors incrementally
4. Update PowerBuilder runtime on all clients
5. Perform regression testing

**For OnBase Migration**:

1. Evaluate OnBase 2023+ versions
2. Plan document repository migration
3. Update API calls for new SDK version
4. Test with new OnBase version in parallel
5. Migrate document metadata

---

## Maintenance Considerations

### Dependency Updates

**Monthly Tasks**:

- Check for SQL Server security patches
- Monitor database connectivity issues
- Review OnBase integration alerts
- Verify backup completion

**Quarterly Tasks**:

- Test database failover procedures
- Update anti-virus exclusions for .pbl files
- Review connection performance metrics
- Plan major version updates

**Annual Tasks**:

- Full environment upgrade testing
- Dependency security assessment
- Capacity planning for data growth
- Archive old election cycle data

### Monitoring and Alerting

**Database Connectivity**:

```sql
-- Monitor failed connections
SELECT *
FROM sys.dm_exec_sessions
WHERE database_id = DB_ID('cfis')
  AND login_time > DATEADD(hour, -1, GETDATE())
```

**COM Interop**:

- Monitor OnBase service availability
- Track failed document uploads
- Alert on COM registration errors
- Log OnBase connection timeouts

**Web Service Connectivity**:

- Monitor CmoService endpoint availability
- Track SOAP request failures
- Alert on network timeouts
- Log authentication failures

### Dependency Documentation

**Maintain Updated Records**:

- Installed version numbers for all components
- License expiration dates
- Upgrade compatibility matrices
- Disaster recovery procedures
- Point of contact for each external service

---

## Summary

CFIS has a **stable but aging dependency structure**:

### Strengths

- Clear hierarchical library organization
- No circular dependencies
- Multiple database version support
- Modular external integrations

### Risks

- End-of-support for PowerBuilder 10.5 (2025+)
- SQL Server 2000-2008 no longer supported
- No native 64-bit version of PowerBuilder 10.5
- OnBase 2010 compatibility uncertain with modern OnBase versions

### Action Items

1. Migrate to SQL Server 2016 or later (within 12 months)
2. Plan PowerBuilder modernization (18-24 month project)
3. Evaluate OnBase API compatibility (6 months)
4. Establish dependency version tracking system (immediate)
5. Create automated testing for dependency compatibility (6 months)
