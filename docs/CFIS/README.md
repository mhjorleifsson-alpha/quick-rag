# CFIS System Documentation

Campaign Finance Information System - Complete Technical Documentation Suite

**Generated**: February 7, 2026
**System**: CFIS (Campaign Finance Information System)
**Status**: Production System (25+ years, hybrid PowerBuilder + ASP.NET)
**Documentation Version**: 1.0

---

## Overview

This documentation suite provides comprehensive coverage of the CFIS system, a legacy hybrid application supporting New York City campaign finance tracking and reporting. The documentation is organized in 10 specialized documents covering different aspects of the system for different audiences.

---

## Documentation Files (10 Total)

### 1. 01-OVERVIEW.md (443 lines)

**Purpose**: System introduction and high-level context
**Audience**: All stakeholders, executives, new team members

**Covers**:

- Executive summary and key statistics
- System purpose and regulatory context
- High-level architecture (visual diagram)
- Technology stack (PowerBuilder 10.5, ASP.NET, SQL Server)
- Component overview (28 libraries, web application, databases)
- Deployment architecture
- Key features and capabilities
- System users (internal CFB staff, external candidates, public)
- System lifecycle status and constraints

**Key Takeaway**: CFIS is a mission-critical hybrid system managing campaign finance for NYC, combining PowerBuilder desktop components with ASP.NET web services, supporting 8+ SQL Server versions, and integrating with OnBase document management.

---

### 2. 02-ARCHITECTURE.md (838 lines)

**Purpose**: Detailed technical architecture reference
**Audience**: Architects, senior developers, infrastructure engineers

**Covers**:

- Three-tier architecture model (presentation, business logic, data)
- System architecture diagrams (visual tier breakdown)
- Component interaction patterns (synchronous/asynchronous)
- PowerBuilder desktop tier details (28 libraries, 340MB total)
- Web application tier (ASP.NET, templates, ASPX files)
- Data persistence layer (SQL Server multi-version support)
- External integration tier (OnBase, CmoService)
- Deployment topology (desktop, web, document management, database)
- Data flow architecture (ingestion, processing, output)

**Key Elements**:

- Modular library organization (no circular dependencies)
- Clear separation of concerns (candidate, finance, reporting, search, utilities)
- Three-tier deployment model
- Multiple database instance support (db2000-db2010, ndb2005x)

---

### 3. 03-DEPENDENCIES.md (757 lines)

**Purpose**: Complete dependency and requirement analysis
**Audience**: DevOps, system administrators, developers

**Covers**:

- Runtime dependencies (PowerBuilder 10.5, .NET Framework 2.0+)
- Library dependencies (28 interconnected PowerBuilder libraries)
- Database dependencies (SQL Server 2000-2012)
- External dependencies (OnBase, CmoService, ODBC drivers)
- System requirements (Windows OS, COM runtime, DCOM)
- Dependency conflicts and resolution strategies
- Maintenance considerations for dependency updates

**Critical Dependencies**:

- Sybase/Appeon PowerBuilder Runtime 21.0.0.1509
- Microsoft .NET Framework 2.0 or later
- SQL Server 2000+ (9 versions supported)
- OnBase Document Management System
- Windows COM/DCOM infrastructure

---

### 4. 04-EXTERNAL-INTEGRATIONS.md (759 lines)

**Purpose**: Integration architecture and connectivity details
**Audience**: Integration engineers, infrastructure architects

**Covers**:

- Integration overview (OnBase, CmoService, Database)
- OnBase document management integration
  - COM-based synchronous API
  - Document upload/download
  - Version control and audit trails
- CmoService web services integration
  - SOAP-based asynchronous messaging
  - Campaign management messaging
  - Audit letter posting
- Database connectivity patterns
  - Multi-instance support
  - Connection pooling
  - Shared memory protocol
- Integration patterns and best practices
- Error handling and retry mechanisms
- Performance considerations
- Troubleshooting guide

**Key Integrations**:

- OnBase Unity Upload API (COM object)
- CmoService SOAP endpoint (c-accessprod:8007)
- Multiple SQL Server instances
- ODBC connectivity layer

---

### 5. 05-API-DOCUMENTATION.md (468 lines)

**Purpose**: API reference for integration and development
**Audience**: Integration developers, API consumers

**Covers**:

- CmoService SOAP API reference
  - Base URL: http://c-accessprod:8007/CAccess/CmoService/
  - Authentication methods (Windows Integrated Auth)
  - WSDL endpoint
- Method reference with examples
  - PostMessage
  - PostPaymentLetter
  - PostTollingLetter
  - PostInitialDocumentRequest
  - PostDraftAuditReport
  - PostFinalAuditReport
  - PostStatementReview
- PowerBuilder component APIs
- Database stored procedures
- Error codes and handling
- Authentication and authorization

**API Endpoints**:

- Service: http://c-accessprod:8007/CAccess/CmoService/
- WSDL: http://c-accessprod:8007/CAccess/CmoService?wsdl

---

### 6. 06-CODE-ANALYSIS.md (358 lines)

**Purpose**: Technical codebase assessment and quality analysis
**Audience**: Developers, architects, QA engineers

**Covers**:

- Code structure analysis (library size distribution)
- Library breakdown and purposes (28 libraries, 340MB)
- Code metrics estimates
  - ~2-3 million estimated lines of code
  - 15,000-20,000 business functions
  - 800-1,200 data windows
  - 80-120 database tables
- Architectural findings (strengths and weaknesses)
- Maintenance burden assessment
- Technical debt analysis
- Modernization recommendations

**Key Findings**:

- **Strengths**: Modular organization, multi-database support, mature feature set, minimal circular dependencies
- **Weaknesses**: Technology age (20+ year old tools), minimal test coverage (0% automated), large codebase, legacy patterns
- **Technical Debt**: Approximately 30-40% dead code accumulation, no automated tests, no continuous integration

---

### 7. 07-SECURITY-REVIEW.md (382 lines)

**Purpose**: Independent security assessment and recommendations
**Audience**: Security architects, compliance officers, IT leadership

**Covers**:

- Executive summary of security posture
- Critical findings (CVSS-scored)
  - Hardcoded database credentials
  - No HTTPS enforcement
  - Zero input validation in web forms
  - SQL injection vulnerabilities
  - XSS vulnerabilities in templates
- High-priority findings
  - Missing authentication logging
  - Insufficient access controls
  - No rate limiting
  - Legacy crypto algorithms
- Medium-priority findings
  - Missing security headers
  - No CORS policy
  - Information disclosure risks
  - Inadequate error handling
- Low-priority findings
  - Missing security audit logging
  - No security.txt file
  - Weak password policy
- Compliance gaps (NY SHIELD Act)
- Remediation roadmap and recommendations
- No cost estimates (independent analysis only)

**Security Status**: 12 findings identified (2 CRITICAL, 4 HIGH, 5 MEDIUM, 3 LOW)

---

### 8. 08-DATA-FLOWS.md (479 lines)

**Purpose**: Visual and textual explanation of system data flows
**Audience**: Data architects, ETL specialists, analysts

**Covers**:

- High-level data flows and ingestion routes
- Candidate registration flow
  - Step 1: Candidate entry and registration
  - Step 2: Committee setup
  - Step 3: Filing schedule setup
- Financial transaction processing
  - Data import and validation
  - Transaction reconciliation
  - Reporting and output
- Report generation flow
- Document management flow
- Data synchronization patterns
- Data transformation pipelines
- Multi-cycle data management

**Key Data Flows**:

- External CSV filings → Import → Database
- Bank account exports → Reconciliation → Database
- UI data entry → Validation → Database
- SOAP calls → Async processing → Database
- Database → Reports → PDF/Excel/XML
- Database → Web templates → Public voter guide

---

### 9. 09-MAINTENANCE-NOTES.md (499 lines)

**Purpose**: Operational procedures and maintenance guidelines
**Audience**: Operations staff, system administrators, support engineers

**Covers**:

- Maintenance strategy overview
- Daily operational tasks
- Weekly maintenance procedures
- Monthly maintenance tasks
- Quarterly tasks
- Backup and recovery procedures
  - Backup schedule (full, incremental, transaction log)
  - Recovery time objectives (RTO/RPO)
- Known issues and workarounds
  - Database connection timeout
  - OnBase upload failures
  - Report generation hangs
  - Web template rendering issues
- Performance optimization tips
- Upgrade paths and compatibility
- Monitoring and alerting strategy
- Common troubleshooting scenarios

**Operational Support**:

- Full backup: Sunday 22:00
- Incremental: Daily 23:00
- Transaction log: Every hour
- RTO: 4 hours, RPO: 1 hour

---

### 10. 10-EXPLANATION-GUIDE.md (483 lines)

**Purpose**: Non-technical explanation of system purpose and workflows
**Audience**: Business users, CFB staff, stakeholders, new team members

**Covers**:

- Campaign lifecycle explanation
  - Phase 1: Campaign registration
  - Phase 2: Active campaign
  - Phase 3: Public disclosure
  - Phase 4: Post-election
- Financial tracking explained (for non-technical audience)
- Reporting and compliance overview
- Public voter guide explanation
- Behind-the-scenes technical implementation
- How PowerBuilder desktop workflows work
- How web applications serve public data
- Real-world scenarios and examples
- Common tasks and how they're accomplished

**Audience Translation**:

- What is CFIS? → Campaign finance tracking system for NYC elections
- Why CFIS? → Compliance with campaign finance law and voter information
- How CFIS? → Desktop data entry + web public access + OnBase documents

---

## Document Statistics

| File                     | Lines     | Focus               | Audience                      |
| ------------------------ | --------- | ------------------- | ----------------------------- |
| 01-OVERVIEW              | 443       | High-level context  | All stakeholders              |
| 02-ARCHITECTURE          | 838       | Technical design    | Architects, senior developers |
| 03-DEPENDENCIES          | 757       | Requirements        | DevOps, administrators        |
| 04-EXTERNAL-INTEGRATIONS | 759       | Connectivity        | Integration engineers         |
| 05-API-DOCUMENTATION     | 468       | API reference       | Integration developers        |
| 06-CODE-ANALYSIS         | 358       | Quality assessment  | Developers, architects        |
| 07-SECURITY-REVIEW       | 382       | Security findings   | Security, compliance          |
| 08-DATA-FLOWS            | 479       | Data processing     | Data architects, ETL          |
| 09-MAINTENANCE-NOTES     | 499       | Operations          | Operations staff              |
| 10-EXPLANATION-GUIDE     | 483       | Non-technical       | Business users                |
| **TOTAL**                | **5,466** | **Complete system** | **All audiences**             |

---

## How to Use This Documentation

### For New Team Members

1. Start with **01-OVERVIEW.md** for context
2. Read **10-EXPLANATION-GUIDE.md** to understand the business
3. Review **02-ARCHITECTURE.md** to understand the technical design
4. Check **03-DEPENDENCIES.md** for setup requirements

### For System Administrators

1. Review **09-MAINTENANCE-NOTES.md** for daily operations
2. Check **03-DEPENDENCIES.md** for system requirements
3. Consult **04-EXTERNAL-INTEGRATIONS.md** for integration troubleshooting
4. Reference **08-DATA-FLOWS.md** for data movement understanding

### For Developers

1. Start with **02-ARCHITECTURE.md** for system design
2. Review **06-CODE-ANALYSIS.md** for codebase structure
3. Check **05-API-DOCUMENTATION.md** for APIs
4. Reference **08-DATA-FLOWS.md** for data processing logic
5. Consult **07-SECURITY-REVIEW.md** for security considerations

### For Integration Specialists

1. Review **04-EXTERNAL-INTEGRATIONS.md** for integration patterns
2. Check **05-API-DOCUMENTATION.md** for CmoService API
3. Reference **08-DATA-FLOWS.md** for data flows
4. Consult **03-DEPENDENCIES.md** for requirements

### For Security/Compliance

1. Review **07-SECURITY-REVIEW.md** for findings
2. Check **02-ARCHITECTURE.md** for architecture security
3. Reference **04-EXTERNAL-INTEGRATIONS.md** for integration security
4. Consult **09-MAINTENANCE-NOTES.md** for operational security

### For Executives/Decision Makers

1. Start with **01-OVERVIEW.md** for system context
2. Review **06-CODE-ANALYSIS.md** for technical status
3. Check **07-SECURITY-REVIEW.md** for risk assessment
4. Reference **09-MAINTENANCE-NOTES.md** for operational cost overview

---

## Key System Metrics

### Technology Stack

- **PowerBuilder**: 10.5 (released 2001-2005 era)
- **Web Framework**: ASP.NET 2.0+
- **Database**: SQL Server 2000-2012 (9 versions supported)
- **Document Management**: OnBase 2010+
- **Integration**: SOAP web services (CmoService)

### Code Metrics

- **Total Libraries**: 28 PowerBuilder (.pbl) files
- **Total Size**: 340+ MB compiled
- **Estimated Lines of Code**: 2-3 million
- **Estimated Functions**: 15,000-20,000
- **Data Windows**: 800-1,200
- **Database Tables**: 80-120
- **Source Files**: 7,120+ (in version control)

### Deployment

- **Desktop**: PowerBuilder runtime on Windows workstations
- **Web**: IIS/ASP.NET on web servers
- **Database**: SQL Server instances (multiple versions)
- **Documents**: OnBase local client + network server

### Support

- **Operating System**: Windows (desktop and server)
- **Users**: 20-50 internal staff, 1000+ external candidates/committees, unlimited public
- **Availability**: Production (24/5, limited weekend support)
- **Backup**: Full weekly, incremental daily, transaction log hourly

---

## System Characteristics

### Strengths

- Stable production system for 25+ years
- Comprehensive campaign finance tracking
- Multi-database version support
- Modular architecture with clear separation of concerns
- Hybrid deployment (desktop + web) serving multiple audiences
- OnBase integration for document management
- Audit trail and compliance capabilities

### Weaknesses

- Technology age (20+ year old tools, unsupported)
- Zero automated test coverage
- Minimal CI/CD infrastructure
- Large codebase (340MB+ libraries)
- Legacy PowerBuilder patterns
- Limited documentation (now being addressed)
- No continuous deployment capability

### Known Issues

- Database connection timeouts under load
- OnBase upload failures on network latency
- Report generation can hang for large datasets
- Web template rendering inconsistencies across browsers
- Legacy ASP.NET 2.0 compatibility issues with modern .NET

### Future Outlook

- System is in extended maintenance mode (no new feature development)
- Modernization would require significant investment (estimated $2-5M)
- Migration to modern tech stack recommended within 3-5 years
- Current system expected to support operations through 2026-2030

---

## Navigation

All documents are cross-referenced with the following structure:

```
01-OVERVIEW (Start here)
├─ 02-ARCHITECTURE (Technical design)
├─ 10-EXPLANATION-GUIDE (Business understanding)
├─ 03-DEPENDENCIES (Requirements)
├─ 04-EXTERNAL-INTEGRATIONS (Connectivity)
├─ 05-API-DOCUMENTATION (Integration APIs)
├─ 06-CODE-ANALYSIS (Code quality)
├─ 07-SECURITY-REVIEW (Security findings)
├─ 08-DATA-FLOWS (Data processing)
└─ 09-MAINTENANCE-NOTES (Operations)
```

---

## Documentation Quality Notes

- **Accuracy**: Based on source code analysis and configuration file review
- **Completeness**: Covers all major system components and integrations
- **Currency**: Updated February 2026 for current production state
- **Audience-Focused**: Each document targets specific roles and skill levels
- **Cross-Linked**: All documents reference related sections in other files
- **Practical**: Includes real configuration examples and code snippets

---

## Feedback and Updates

This documentation should be updated when:

- System architecture changes
- New integrations are added
- Critical security issues are resolved
- Performance optimizations are implemented
- Technology dependencies are upgraded
- Operational procedures change

Last reviewed: February 2026
Next review recommended: August 2026 (6-month refresh cycle)

---

**Document Status**: COMPLETE
**Version**: 1.0
**Access**: Internal (Campaign Finance Board)
**Confidentiality**: Standard (non-sensitive system documentation)
