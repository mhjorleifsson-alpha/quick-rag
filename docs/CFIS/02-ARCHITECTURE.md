# CFIS System Architecture

Detailed Technical Architecture

**Document Version**: 1.0
**Last Updated**: February 2026

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Three-Tier Architecture Model](#three-tier-architecture-model)
3. [Component Interaction Patterns](#component-interaction-patterns)
4. [PowerBuilder Desktop Tier](#powerbuilder-desktop-tier)
5. [Web Application Tier](#web-application-tier)
6. [Data Persistence Layer](#data-persistence-layer)
7. [External Integration Tier](#external-integration-tier)
8. [Deployment Topology](#deployment-topology)
9. [Data Flow Architecture](#data-flow-architecture)

---

## System Architecture Overview

CFIS implements a hybrid three-tier architecture combining:

1. **Presentation Tier**: PowerBuilder desktop application + ASP.NET web
2. **Business Logic Tier**: PowerBuilder libraries + C# web services
3. **Data Tier**: SQL Server with multiple version support

### Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    PRESENTATION TIER                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────┐      ┌──────────────────────────┐   │
│  │  PowerBuilder Client │      │  ASP.NET Web            │   │
│  │  (Desktop Users)     │      │  (Public/Voters)        │   │
│  │                      │      │                         │   │
│  │  • Forms & Windows   │      │  • ASPX Pages           │   │
│  │  • Data Entry UI     │      │  • Template Engine      │   │
│  │  • Reports Viewer    │      │  • XML Endpoints        │   │
│  │  • Admin Tools       │      │  • Search Interface     │   │
│  └──────────┬───────────┘      └──────────┬──────────────┘   │
│             │                             │                   │
└─────────────┼─────────────────────────────┼───────────────────┘
              │                             │
┌─────────────▼─────────────────────────────▼───────────────────┐
│                   BUSINESS LOGIC TIER                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        PowerBuilder Application Logic                │   │
│  │                                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │  Candidate  │  │  Finance    │  │  Report    │  │   │
│  │  │  Management │  │  Processing │  │  Generation│  │   │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  │                                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │  Search &   │  │  Audit      │  │  Document  │  │   │
│  │  │  Query      │  │  Functions  │  │  Management│  │   │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  └──────────┬──────────────────────────────────────────┘   │
│             │                                                │
│  ┌──────────▼──────────────────────────────────────────┐   │
│  │  Web Services Layer (CmoService SOAP)               │   │
│  │  • Message Posting                                  │   │
│  │  • Async Processing                                 │   │
│  │  • External Integration                             │   │
│  └──────────┬──────────────────────────────────────────┘   │
│             │                                                │
└─────────────┼────────────────────────────────────────────────┘
              │
┌─────────────▼────────────────────────────────────────────────┐
│                    DATA TIER                                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     SQL Server Database Engine                       │   │
│  │     (SQL 2000-2012 Support)                          │   │
│  │                                                      │   │
│  │  ┌─────────────┐  ┌────────────┐  ┌────────────┐   │   │
│  │  │ Campaign    │  │ Candidate  │  │ Transaction│   │   │
│  │  │ Data        │  │ Data       │  │ Records    │   │   │
│  │  └─────────────┘  └────────────┘  └────────────┘   │   │
│  │                                                      │   │
│  │  ┌─────────────┐  ┌────────────┐  ┌────────────┐   │   │
│  │  │ Committee   │  │ Audit      │  │ User Access│   │   │
│  │  │ Information │  │ Trail      │  │ Logs       │   │   │
│  │  └─────────────┘  └────────────┘  └────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     OnBase Document Management                       │   │
│  │     (External Integration)                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Three-Tier Architecture Model

### Tier 1: Presentation Tier

**Purpose**: User interface and user experience

**Components**:

- PowerBuilder desktop application (28 libraries, 340MB+)
- ASP.NET web application (IIS-hosted)
- Web template engine (30+ ASPX files)
- Legacy HTML templates (cfis2001 directory)

**Responsibilities**:

- Render user interfaces
- Accept user input
- Validate user interactions
- Display data and reports
- Route user actions to business logic

**Technologies**:

- PowerScript (desktop)
- ASP.NET (web)
- HTML/CSS (templates)
- Windows Forms (UI controls)

### Tier 2: Business Logic Tier

**Purpose**: Core application functionality and business rules

**Components**:

- PowerBuilder application objects
- User-defined objects (UDOs)
- Business function libraries
- Data validation logic
- Report generation engine
- Web service handlers

**Responsibilities**:

- Enforce business rules
- Process transactions
- Calculate derived values
- Coordinate multi-step operations
- Handle data transformations
- Generate reports and exports

**Technologies**:

- PowerScript functions
- Stored procedures (database)
- SOAP web services
- COM objects (OnBase integration)

**Key Libraries**:

- Cfisfn.pbl: Core business functions
- cfiscand.pbl: Candidate operations
- cfispmt.pbl: Payment processing
- cfisintk.pbl: Data intake
- cfisrptd.pbl: Detailed reporting
- Cfisutil.pbl: Utility functions

### Tier 3: Data Tier

**Purpose**: Persistent data storage and retrieval

**Components**:

- SQL Server database instances (2000-2012)
- Database schema (campaign finance tables)
- Stored procedures
- OnBase document storage
- Audit trail logs
- Configuration data

**Responsibilities**:

- Store and retrieve data
- Enforce data integrity
- Execute complex queries
- Maintain transaction consistency
- Provide backup and recovery
- Store and manage documents

**Technologies**:

- Microsoft SQL Server (RDBMS)
- T-SQL (stored procedures and functions)
- OnBase API (document management)
- ODBC/ADO connections

---

## Component Interaction Patterns

### Pattern 1: Client-Server (PowerBuilder Desktop)

```
User Input
   │
   ▼
PowerBuilder Form (UI)
   │
   ▼
PowerBuilder Script (event handler)
   │
   ▼
Business Logic Function (Cfis*.pbl)
   │
   ▼
Database Query/Stored Procedure
   │
   ▼
SQL Server Database
   │
   ▼
Result Set
   │
   ▼
PowerBuilder DataWindow (data display)
   │
   ▼
User Display
```

### Pattern 2: Web Request Processing (ASP.NET)

```
HTTP Request (Browser)
   │
   ▼
IIS / ASP.NET Handler
   │
   ▼
ASPX Template (gen_cand_TEMPLATE.aspx)
   │
   ▼
Template Engine (XML binding)
   │
   ▼
Database Query
   │
   ▼
SQL Server Database
   │
   ▼
Result Set
   │
   ▼
Template Rendering
   │
   ▼
HTML Response
   │
   ▼
Browser Rendering
```

### Pattern 3: Asynchronous Web Service (SOAP)

```
External System Request
   │
   ▼
CmoService SOAP Endpoint
   │
   ▼
CmoService.cs Proxy
   │
   ▼
Message Queue / Async Handler
   │
   ▼
PowerBuilder Business Logic
   │
   ▼
Database Update
   │
   ▼
OnBase Document Upload
   │
   ▼
Async Callback
   │
   ▼
SOAP Response (async)
```

### Pattern 4: Document Management (OnBase)

```
PowerBuilder Application
   │
   ▼
OnBaseUnityUploadApi.dll (COM Interface)
   │
   ▼
OnBase Client Library
   │
   ▼
OnBase Server
   │
   ▼
Document Storage
   │
   ▼
Audit Trail
```

---

## PowerBuilder Desktop Tier

### Application Structure

**Library Dependency Chain** (partial, showing major dependencies):

```
cfismain.pbl (entry point)
   │
   ├─ cfisapp.pbl (framework)
   │  ├─ Cfisbase.pbl (structures)
   │  ├─ Cfisutil.pbl (utilities)
   │  └─ Cfisstru.pbl (data types)
   │
   ├─ cfiscand.pbl (candidates)
   │  └─ Cfisfn.pbl (functions)
   │
   ├─ cfispmt.pbl (payments)
   │  └─ Cfisfn.pbl
   │
   ├─ cfisintk.pbl (intake)
   │  └─ Cfisconv.pbl (conversion)
   │
   ├─ cfisrptd.pbl (reports - detailed)
   │  └─ cfisrptm.pbl (reports - main)
   │     └─ Cfisform.pbl (forms)
   │
   └─ cfisadm.pbl (admin)
      └─ Cfisuobj.pbl (user objects)
```

### Key Components

#### 1. Application Initialization (cfismain.pbl)

- Application startup logic
- Library loading
- Database connection pooling
- Configuration loading from pb.ini
- User authentication
- Main application window creation

#### 2. Candidate Management (cfiscand.pbl - 11.7MB)

- Candidate registration
- Committee relationships
- Ballot position tracking
- Filing status management
- Office type classification
- Primary/general election switching

#### 3. Financial Processing (cfispmt.pbl - 26.9MB)

- Payment recording
- Transaction entry
- Check number management
- Amount validation and tracking
- Payment schedule maintenance
- Bank account reconciliation

#### 4. Data Intake (cfisintk.pbl - 44.9MB - LARGEST)

- File import processing
- CSV/fixed-width parsing
- Data validation
- Contribution record loading
- In-kind contribution handling
- Batch processing coordination
- Error logging and recovery

#### 5. Reporting Engine (cfisrptd.pbl - 55.1MB - LARGEST SINGLE)

- Complex multi-table joins
- Campaign finance calculations
- Report formatting and pagination
- PDF generation
- Excel export
- XML output
- Performance optimization for large datasets

#### 6. Search and Query (Cfissrch.pbl - 4.5MB)

- Full-text search capability
- Transaction lookup
- Candidate filtering
- Committee search
- Query result caching
- Performance optimization

#### 7. Utilities and Base (Cfisutil.pbl, Cfisbase.pbl)

- String manipulation
- Date formatting
- Currency conversion
- Data type utilities
- Error handling
- Logging infrastructure

### Database Connectivity

**Connection Strategy**:

```powerscript
// Typical connection in pb.ini
[db2005]
Link=Shared Memory

// PowerBuilder connection establishment
SQLCA.AutoCommit = false
SQLCA.DBParm = "ConnectString='DSN=db2005;UID=CFIS;PWD=***'"
connect using SQLCA
```

**Supported Connections**:

- db2000 (SQL Server 2000, legacy)
- db2001, db2003 (historical)
- db2005, db2005x (production primary)
- db2007, db2007a, db2007b (election years)
- db2008, db2009, db2010, db2012 (recent versions)
- ndb2005x (replicated/special purpose)

---

## Web Application Tier

### ASP.NET Architecture

**Component Stack**:

```
Browser Request
   │
   ▼
IIS (Internet Information Services)
   │
   ▼
ASP.NET Runtime (.NET Framework 2.0+)
   │
   ▼
ASPX Parser
   │
   ▼
HTML Template Processing (cfis2001/webtemplate/)
   │
   ▼
XML Configuration Binding
   │
   ▼
Database Access Layer
   │
   ▼
SQL Server Query
```

### Template System (30+ Templates)

**General Election Templates**:

- `gen_cand_TEMPLATE.aspx`: Candidate profile pages
- `gen_intro_mayor_TEMPLATE.aspx`: Mayoral election intro
- `gen_intro_comptroller_TEMPLATE.aspx`: Comptroller intro
- `gen_intro_pa_TEMPLATE.aspx`: Public advocate intro
- `gen_intro_citycouncil_TEMPLATE.aspx`: City council intro
- `gen_intro_bp_TEMPLATE.aspx`: Borough president intro
- `gen_district_TEMPLATE.aspx`: District-based filtering
- `gen_no_profile_TEMPLATE.aspx`: Fallback for candidates without profiles

**Primary Election Templates**:

- `pri_cand_TEMPLATE.aspx`: Primary candidate pages
- `pri_byalpha_TEMPLATE.aspx`: Alphabetical candidate lists
- `pri_district_TEMPLATE.aspx`: District filtering
- `pri_no_profile_TEMPLATE.aspx`: Primary fallback

**Introduction Templates**:

- `intro_mayor_TEMPLATE.aspx`
- `intro_comptroller_TEMPLATE.aspx`
- `intro_pa_TEMPLATE.aspx`
- `intro_citycouncil_TEMPLATE.aspx`
- `intro_bp_TEMPLATE.aspx`

**Legacy HTML Templates** (cfis2001/webtemplate/\*.htm):

- candidate.htm: Static candidate reference
- filer.htm: Committee/filer information
- parti.htm: Participant data
- pclist.htm: Participant committee list
- pre_el.htm: Pre-election reference

### Web Service Layer (CmoService)

**Service Endpoint Configuration**:

```xml
<!-- cfis.xml -->
<?xml version="1.0" encoding="utf-8" ?>
<Application>
    <RuntimePath>C:\Program Files (x86)\Appeon\Common\PowerBuilder\Runtime 21.0.0.1509</RuntimePath>
</Application>
```

**CmoService Methods**:

1. PostMessage(): Generic message posting with optional attachments
2. PostPaymentLetter(): Payment-related correspondence
3. PostPaymentLetterByPath(): File-based letter submission
4. PostTollingLetter(): Compliance notification (tolling letters)
5. PostInitialDocumentRequest(): Audit initiation request
6. PostDraftAuditReport(): Draft report submission
7. PostFinalAuditReport(): Final audit report submission
8. PostStatementReview(): Statement review document posting

**Service URL**:

- Configured: http://c-accessprod:8007/CAccess/CmoService/
- Override via AppSettings: EndpointURL configuration

**Protocol**: SOAP over HTTP with async callback capability

---

## Data Persistence Layer

### Database Schema Architecture

**Primary Tables** (implicit from Schema.ini configuration):

#### Candidate Tables

- candidates (Cand_ID, Comm_ID, name, office type, election cycle)
- committees (Comm_ID, committee name, type, status)
- ballot_positions (Cand_ID, office, district, line number)

#### Financial Tables

- transactions (transaction ID, Cand_ID, amount, type, date)
- contributors (Last_Name, First_Name, address, employment)
- payments (payment ID, Cand_ID, amount, check number, date)
- in_kind (ID, Cand_ID, amount, description, date)

#### Reference Tables

- election_cycles (election year, cycle type, start/end dates)
- bank_accounts (account ID, bank, balance)
- purpose_codes (Purpose_CD, description)
- agency_codes (Agency_CD, agency name)
- borough_codes (Boro_CD, borough name)

#### Audit Tables

- audit_trail (user ID, action, timestamp, record ID, before/after values)
- statements (Statement_No, Cand_ID, filing date, status)
- amendments (Amendment_Type, reference information)
- reference_notes (Reference_No, note text)

### Query Patterns

**Contribution Search** (from Schema.ini):

```
SELECT
    Last_Name, First_Name, MI,
    Street_No, Street_Name, Apt_No, City, State_CD, Zip_CD,
    Emp_Last_Name, Emp_First_Name, Emp_Street_Name, Emp_City,
    C_CD, Agency_CD, Occupation,
    Trans_Date, Trans_Type, Amount,
    Check_No, Purpose_CD, Explain,
    Exempt_Ind, Election_Cycle, Cand_ID
FROM campaign_finance_table
WHERE Election_Cycle = @cycle AND Cand_ID = @candidate
ORDER BY Trans_Date DESC, Amount DESC
```

**Reporting Joins** (typical):

```
SELECT
    c.Cand_ID, c.Name, c.Office, c.District,
    SUM(t.Amount) as Total_Raised,
    COUNT(*) as Transaction_Count,
    MAX(t.Trans_Date) as Last_Update
FROM candidates c
LEFT JOIN transactions t ON c.Cand_ID = t.Cand_ID
WHERE c.Election_Cycle = @cycle
GROUP BY c.Cand_ID, c.Name, c.Office, c.District
```

### Multi-Database Strategy

**Database Selection Logic**:

```
Election Cycle 2000-2003  → db2000, db2001, db2003
Election Cycle 2005      → db2005, db2005x
Election Cycle 2007      → db2007, db2007a, db2007b
Election Cycle 2009      → db2009
Election Cycle 2010+     → db2010, db2012
Replicated/Special       → ndb2005x
```

**Connection Pooling**:

- Shared Memory protocol for local network performance
- Connection string: `DSN=dbXXXX;UID=CFIS;PWD=***`
- Auto-commit disabled for transaction control
- Connection reuse for performance optimization

---

## External Integration Tier

### OnBase Document Management

**Integration Points**:

```
PowerBuilder Desktop
   │
   ├─ OnBaseUnityUploadApi.dll (COM Interop)
   │  └─ Document Upload/Download
   │
   └─ OnBase Client Runtime
      └─ Document Indexing & Retrieval
```

**Document Types**:

- Audit letters (initial, draft, final)
- Correspondence (candidate, committee)
- Filed statements and amendments
- Payment documentation
- Compliance notices
- Statement review documents

**Lifecycle Management**:

1. Document creation in PowerBuilder
2. Optional file attachment
3. Upload to OnBase via COM API
4. Indexing by election cycle, candidate, cycle type
5. Audit trail maintenance
6. Retrieval for compliance review

### CmoService Integration

**Connection Model**:

```
PowerBuilder → CmoService SOAP Client → External CmoService →
  Message Queue → PowerBuilder Background Worker
```

**Message Flow**:

1. PowerBuilder application prepares message data
2. Serializes to SOAP request
3. Posts to http://c-accessprod:8007/CAccess/CmoService/
4. CmoService queues message asynchronously
5. Background processor handles message
6. Async callback returns result

**Configuration**:

```
[EndpointURL]
Default: http://c-accessprod:8007/CAccess/CmoService/
Override: App.config AppSettings["EndpointURL"]
```

---

## Deployment Topology

### Single-Tier Deployment (Small Organizations)

```
┌─────────────────────────────┐
│  Windows Server             │
├─────────────────────────────┤
│  PowerBuilder Runtime       │
│  ASP.NET Runtime            │
│  SQL Server (Local)         │
│  OnBase Client              │
└─────────────────────────────┘
```

### Two-Tier Deployment (Medium Organizations)

```
┌─────────────────────────┐         ┌─────────────────────────┐
│  Application Server     │         │  Database Server        │
├─────────────────────────┤         ├─────────────────────────┤
│  PowerBuilder Runtime   │         │  SQL Server Instance    │
│  ASP.NET Runtime        │────────▶│  Multiple Databases     │
│  OnBase Client          │         │  Replication (optional) │
│  IIS                    │         │  Backup/Recovery        │
└─────────────────────────┘         └─────────────────────────┘
```

### Three-Tier Deployment (Large Organizations)

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Web Server   │   │ App Server   │   │ Database     │
├──────────────┤   ├──────────────┤   ├──────────────┤
│ IIS/ASP.NET  │   │ PowerBuilder │   │ SQL Server   │
│ ASPX Pages   │   │ Windows Svc  │   │ db2005,db21  │
│ Templates    │   │ CmoService   │   │ db2007,db210 │
└──────┬───────┘   └──────┬───────┘   └──────▲───────┘
       │                  │                   │
       └──────────────────┼───────────────────┘
                  HTTPS/HTTP
```

### Network Architecture

**Typical Network Configuration**:

```
Users (Desktop/Browser)
   │
   ├─ Shared Memory (Local Network)
   │  └─ PowerBuilder Desktop ←→ Database Server
   │
   └─ HTTP/HTTPS (Internet)
      └─ ASP.NET Web ←→ Web Server ←→ Database Server
```

**Firewalls and Security Zones**:

- Desktop users on corporate network: Direct shared memory access
- Web users on Internet: IIS reverse proxy, firewalled database
- Internal APIs: CmoService endpoints restricted to trusted sources

---

## Data Flow Architecture

### Election Cycle Entry Flow

```
1. Candidate Registration (Desktop)
   ├─ Input: Candidate name, office, district
   ├─ Validation: Unique candidate per cycle/office
   ├─ Store: candidates table
   └─ OnBase: Link to candidate record

2. Committee Setup (Desktop)
   ├─ Input: Committee name, bank account
   ├─ Association: Link to candidate
   ├─ Store: committees table
   └─ Audit Trail: Creation log

3. Finance Reporting Setup (Desktop/Web)
   ├─ Template: Statement schedules
   ├─ Validation: Required fields
   ├─ Store: statement_templates table
   └─ Notify: Filing deadline alerts
```

### Financial Transaction Processing

```
1. Transaction Entry
   ├─ Source: Manual entry, file import, external API
   ├─ Validation: Contributor address, amount ranges
   ├─ Categorization: Receipt/expenditure/in-kind
   └─ Store: transactions table

2. Reconciliation (Batch)
   ├─ Match: Transactions to source documents
   ├─ Validate: Bank account totals
   ├─ Resolve: Discrepancies
   └─ Update: transaction status

3. Reporting
   ├─ Calculate: Totals by category
   ├─ Format: Per regulatory requirements
   ├─ Audit: Verify calculations
   └─ Publish: Public reporting
```

### Public Query Processing

```
1. Web Request (Voter Guide)
   ├─ URL: /cfis2001/gen_cand_TEMPLATE.aspx?cycle=2005&id=123
   ├─ Parse: Template binding
   └─ Route: cfis2001/gen_cand_TEMPLATE.aspx

2. Template Rendering
   ├─ Read: XML configuration
   ├─ Query: Candidate data, transactions
   ├─ Transform: Candidate profile HTML
   └─ Bind: Campaign finance summary

3. Response
   ├─ Generate: Static HTML
   ├─ Cache: Optional browser cache
   └─ Deliver: HTTP response
```

---

## Summary

The CFIS architecture is a mature three-tier system balancing:

- **Flexibility**: Support for multiple database versions
- **Integration**: External document and web service connectivity
- **Performance**: Large dataset handling through optimized queries
- **Legacy Compatibility**: 25+ year support for historical data
- **Scalability**: Multi-database distribution by election cycle

The hybrid PowerBuilder-ASP.NET model reflects the system's evolution from desktop-only to web-enabled deployment while maintaining backward compatibility with legacy processes.
