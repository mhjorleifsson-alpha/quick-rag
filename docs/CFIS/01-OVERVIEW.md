# CFIS System Overview

Campaign Finance Information System (CFIS)

**Document Version**: 1.0
**Last Updated**: February 2026
**System Age**: 25+ years (legacy hybrid system)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Purpose](#system-purpose)
3. [High-Level Architecture](#high-level-architecture)
4. [Technology Stack](#technology-stack)
5. [Component Overview](#component-overview)
6. [Deployment Architecture](#deployment-architecture)
7. [Key Features](#key-features)
8. [System Users](#system-users)

---

## Executive Summary

CFIS is a mission-critical hybrid campaign finance system that has been operational for over 25 years. The system manages campaign finance disclosure, reporting, and public information for the New York City Campaign Finance Board. It combines a legacy PowerBuilder 10.5 desktop application with ASP.NET web components, supporting multiple database versions from SQL Server 2000 through SQL Server 2012.

The system is currently in production supporting election cycles from 2001 through 2010+ with active maintenance and ongoing ballot measure tracking. Despite its age, CFIS continues to process critical campaign finance data, handle public inquiries, and generate regulatory reports.

### Key Statistics

- **PowerBuilder Libraries**: 28 production libraries totaling ~340MB
- **Database Support**: SQL Server 2000, 2003, 2005, 2007, 2008, 2009, 2010, 2012
- **Web Components**: ASP.NET voter guides for multiple candidate types
- **Document Management**: OnBase integration for document storage and retrieval
- **Code Repository**: 7,120+ files in source control (Sybase PowerBuilder format)
- **Template System**: 30+ voter guide templates supporting multiple ballot measure types

---

## System Purpose

CFIS serves as the authoritative campaign finance tracking and reporting system for New York City election campaigns. Core responsibilities include:

### Primary Functions

1. **Campaign Finance Data Collection**: Captures financial contributions, expenditures, and in-kind support
2. **Candidate Management**: Tracks candidate information, committees, and filing requirements
3. **Report Generation**: Produces mandatory campaign finance disclosure documents
4. **Public Query Interface**: Provides voters with searchable campaign finance information
5. **Document Management**: Stores and retrieves campaign finance documents via OnBase
6. **Regulatory Compliance**: Enforces filing deadlines and financial disclosure requirements
7. **Audit Support**: Generates audit trail logs and exception reports

### Regulatory Context

- New York City Campaign Finance Law compliance
- Automated filing deadline enforcement
- Public records management per NY SHIELD Act
- Voter information publication (2001 onward)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CFIS Hybrid System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │  Desktop Application │         │  Web Application     │    │
│  │  (PowerBuilder 10.5) │         │  (ASP.NET)           │    │
│  │                      │         │                      │    │
│  │  • Admin Tools       │         │  • Voter Guides      │    │
│  │  • Data Entry        │         │  • Public Search     │    │
│  │  • Report Generation │         │  • XML Export        │    │
│  │  • Batch Processing  │         │  • Template Engine   │    │
│  └──────────┬───────────┘         └──────────┬───────────┘    │
│             │                               │                  │
│             └───────────────┬────────────────┘                  │
│                             │                                  │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │   OnBase Document Management System                     │  │
│  │   (External Integration)                               │  │
│  │   • Document Storage                                   │  │
│  │   • Audit Letters                                      │  │
│  │   • Correspondence Management                          │  │
│  └──────────────────────────┬──────────────────────────────┘  │
│                             │                                  │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │   SQL Server Database                                  │  │
│  │   (SQL 2000-2012 Support)                              │  │
│  │   • Campaign Finance Data                              │  │
│  │   • Candidate Information                              │  │
│  │   • Transaction Records                                │  │
│  │   • Audit Trail                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Characteristics

- **Hybrid Model**: PowerBuilder desktop + ASP.NET web dual deployment
- **Database Agnostic**: Supports multiple SQL Server versions for backward compatibility
- **Document-Centric**: Heavy integration with OnBase for record management
- **Multi-Tier**: Three-tier architecture (presentation, business logic, data)
- **Legacy Integration**: 25+ years of accumulated data and processes

---

## Technology Stack

### Desktop Application

- **Language**: PowerScript (PowerBuilder scripting language)
- **Framework**: PowerBuilder 10.5
- **Runtime**: Sybase/Appeon PowerBuilder Runtime
- **Database Connectivity**: DB2, Sybase, ODBC via native drivers
- **COM Integration**: OnBaseUnityUploadApi.dll for document management

### Web Application

- **Framework**: ASP.NET (2.0+ implied from structure)
- **Language**: C# (CmoService.cs auto-generated proxy)
- **Rendering Engine**: Template-based HTML (cfis2001 webtemplate directory)
- **Data Binding**: XML-based configuration for dynamic content

### Database

- **Primary**: Microsoft SQL Server (2000-2012 supported)
- **Secondary**: Sybase databases (legacy support)
- **Connection Type**: Shared Memory for local connections
- **Database Names**: db2000, db2001, db2003, db2005, db2005x, db2007, db2007a, db2007b, db2009, db2010, ndb2005x

### External Integration

- **OnBase Document Management**:
  - OnBaseUnityUploadApi.dll for programmatic access
  - Document upload and retrieval
  - Version control and audit trail
- **Web Services**:
  - CmoService SOAP endpoint (Campaign Management Office)
  - Asynchronous messaging capability
  - Letter posting and notification

### Infrastructure

- **Operating System**: Windows (desktop + server)
- **Network Protocol**: HTTP/HTTPS for web, Shared Memory for database
- **Configuration Management**: INI files (pb.ini, asasrv.ini, Schema.ini)
- **Build System**: PowerBuilder project workspace (.pbw files)

---

## Component Overview

### 1. PowerBuilder Libraries (28 Total)

#### Core Infrastructure Libraries

- **Cfisbase.pbl** (356KB): Base structures and data types
- **Cfisutil.pbl** (3.8MB): Utility functions and helpers
- **Cfisfn.pbl** (963KB): Core business functions
- **Cfisstru.pbl** (160KB): Data structure definitions

#### Application Components

- **cfismain.pbl** (4.2MB): Main application entry point
- **cfisapp.pbl** (3.1MB): Application framework and initialization
- **cfisids.pbl** (350KB): ID and reference management
- **cfisdyn.pbl** (564KB): Dynamic object creation and management

#### Business Logic Libraries

- **cfiscand.pbl** (11.7MB): Candidate management
- **cfispmt.pbl** (26.9MB): Payment and financial transaction processing
- **cfisintk.pbl** (44.9MB): Data intake and import functionality (LARGEST)
- **cfiscont.pbl** (2.1MB): Contribution tracking
- **cfisconv.pbl** (3.5MB): Data conversion utilities
- **cfismail.pbl** (1.7MB): Email and messaging

#### Tracking and Reporting Libraries

- **cfisatrk.pbl** (29.0MB): Account tracking
- **cfisdtrk.pbl** (4.9MB): Deposit tracking
- **cfislegtrk.pbl** (1.5MB): Legislative tracking
- **cfistrntrk.pbl** (3.2MB): Transaction tracking
- **cfisvgtrk.pbl** (10.1MB): Voter guide tracking

#### Reporting and UI Libraries

- **cfisrptm.pbl** (39.2MB): Main reporting module (SECOND LARGEST)
- **cfisrptd.pbl** (55.1MB): Detailed reporting module (LARGEST)
- **cfisrptw.pbl** (32.7MB): Web reporting module
- **Cfisform.pbl** (7.8MB): Form components and UI elements
- **Cfissrch.pbl** (4.5MB): Search functionality
- **Cfisdddw.pbl** (1.5MB): Data display windows

#### Administrative Libraries

- **cfisadm.pbl** (2.8MB): Administrator tools and management
- **Cfisuobj.pbl** (194KB): User object definitions
- **cfisids.pbl** (350KB): Integrated development environment services
- **cfiscvsm.pbl** (6.4MB): Content and Version Sync Management

### 2. Web Application Components

#### Template Directory Structure (`cfis2001/webtemplate/`)

**HTML Legacy Templates**:

- candidate.htm: Candidate profile display
- filer.htm: Filer/committee information
- outpen.htm: Outstanding penalties information
- parti.htm: Participant information
- pclist.htm: Participant committee listing
- pre_el.htm: Pre-election information
- ptie.htm: Participant ties
- sumt.htm: Summary information
- dssl.htm: Data supplemental summary

**ASP.NET Template Engine** (30+ ASPX files):

- `gen_cand_TEMPLATE.aspx`: General candidate voter guide generator
- `gen_district_TEMPLATE.aspx`: District-based candidate guides
- `gen_districtX_TEMPLATE.aspx`: Extended district filtering
- `gen_intro_*.aspx`: Introduction pages for different office types
  - Mayor, Comptroller, Public Advocate, City Council, Borough President
- `pri_*.aspx`: Primary election variant templates
- `intro_*.aspx`: Individual office-specific intros

**Template Features**:

- Dynamic content binding from database
- Multi-office support (mayoral, council, PA, comptroller, borough president)
- Primary and general election variants
- No-profile fallback handling
- Alpha-sorted listings

### 3. Web Services

#### CmoService (Campaign Management Office)

**Endpoint**: http://c-accessprod:8007/CAccess/CmoService/

**Methods**:

- `PostMessage()`: Send campaign messages with attachment support
- `PostPaymentLetter()`: Submit payment-related correspondence
- `PostPaymentLetterByPath()`: File-based payment letter posting
- `PostTollingLetter()`: Post tolling letters (compliance notifications)
- `PostInitialDocumentRequest()`: Request initial audit documentation
- `PostDraftAuditReport()`: Submit draft audit reports
- `PostFinalAuditReport()`: Submit final audit reports
- `PostStatementReview()`: Post statement review documents

**Parameters**: Election cycle, candidate ID, creator, title, body, receipt email, attachments, notification flags

**Transport**: SOAP over HTTP (async-capable)

### 4. Database Components

#### Multi-Database Support

- **SQL Server 2000**: Legacy support (db2000)
- **SQL Server 2003**: Extended support (db2003)
- **SQL Server 2005**: Production standard (db2005, db2005x)
- **SQL Server 2007**: Additional instances (db2007, db2007a, db2007b)
- **SQL Server 2008**: Extended support (db2008)
- **SQL Server 2009**: Extended support (db2009)
- **SQL Server 2010**: Current support (db2010)
- **SQL Server 2012**: Current support (db2012)
- **Non-standard**: ndb2005x (potentially replicated instance)

#### Data Schema Coverage

Campaign finance data organized by election cycle and record type:

- Candidate information and status
- Committee relationships
- Financial transactions (receipts, expenditures)
- Payment information
- Contribution tracking
- In-kind contributions
- Bank account information
- Audit trail entries
- Document references

#### Schema Configuration (Schema.ini)

Fixed-length record format supporting legacy integration:

- 72 columns per contributor record
- Campaign-specific data mapping
- Employment information tracking
- Address fields (residential and employment)
- Transaction amounts and dates
- Check number tracking
- Partnership contribution tracking
- Audit and amendment flags

---

## Deployment Architecture

### Desktop Component Deployment

1. **PowerBuilder 10.5 IDE Installation** on developer workstations
2. **Runtime Installation** on user machines (Appeon PowerBuilder Runtime 21.0+)
3. **Application Distribution**: Network-based or local installation
4. **Database Connectivity**: Shared Memory protocol for local network
5. **Library Loading**: Sequential loading of 28 .pbl files in dependency order

### Web Component Deployment

1. **IIS Installation** on web server
2. **ASP.NET Framework** deployment (2.0 or later)
3. **Application Pool** configuration for ASPX processing
4. **Template Files** deployed to cfis2001/webtemplate directory
5. **Configuration Files**: asasrv.ini for web services endpoints

### Document Management Deployment

1. **OnBase Client Installation** on desktop workstations
2. **OnBase API DLL** registration (OnBaseUnityUploadApi.dll)
3. **COM Registration** for PowerBuilder interop
4. **Document Capture** module configuration
5. **Connection Pooling** for upload/download operations

### Database Deployment

1. **SQL Server Instance** configuration
2. **Database Creation** from SQL scripts
3. **Shared Memory** protocol enablement
4. **Backup and Recovery** procedures
5. **Replication** setup (for ndb2005x non-standard instance)

---

## Key Features

### Candidate and Committee Management

- Centralized candidate database with registration
- Committee relationship tracking
- Primary and general election support
- Ballot measure tracking
- Filing status tracking and deadline enforcement

### Financial Transaction Processing

- Receipt recording and categorization
- Expenditure tracking and reporting
- In-kind contribution valuation
- Bank account reconciliation
- Check number tracking
- Payment schedule management

### Public Information System

- Interactive voter guide generation
- Candidate profile pages
- Committee financial summaries
- Searchable transaction database
- PDF report generation
- XML data export

### Audit and Compliance

- Automated filing deadline alerts
- Audit trail logging
- Amendment tracking
- Compliance exception reporting
- Letter management (initial requests, drafts, final reports)

### Document Management

- OnBase integration for document storage
- Automated document capture
- Audit letter lifecycle management
- E-signature support capability
- Document version control

---

## System Users

### Internal Users (CFB Staff)

- **Administrators**: System configuration, user management, database maintenance
- **Data Entry Operators**: Financial transaction entry, candidate data updates
- **Compliance Officers**: Filing deadline management, audit coordination
- **Report Analysts**: Report generation and data validation
- **IT Support**: System maintenance, troubleshooting, backup management

### External Users

- **Candidates and Campaign Committees**: Financial reporting submissions
- **Media and Public**: Voter guide access, financial transaction search
- **Elected Officials**: Public query access to financial data
- **Researchers**: Data export and analysis

### System Operators

- **Batch Processing**: Scheduled tasks for report generation, data cleanup
- **Web Services**: Automated message posting via CmoService endpoints
- **Document Capture**: OnBase integration for automatic document filing

---

## System Lifecycle Status

### Current State (as of February 2026)

- **Active Support**: Yes, ongoing election cycle support through 2010+
- **Maintenance Mode**: Critical patch fixes only, no new features
- **Production**: Primary system for NYC campaign finance data
- **End of Life**: Not yet announced, but 25+ year old system with legacy technology

### Known Constraints

- **Technology Age**: PowerBuilder 10.5 (released 2001-2005 era)
- **Database Age**: SQL Server 2000+ support outdated
- **Architecture**: Hybrid model creates deployment complexity
- **Code Maintenance**: Large codebase (340MB+ libraries) with legacy patterns
- **Test Coverage**: Minimal automated testing (typical of 1990s-2000s systems)

---

## Document Cross-References

For detailed information on specific aspects:

- **Architecture Details**: See 02-ARCHITECTURE.md
- **Dependency Analysis**: See 03-DEPENDENCIES.md
- **Integration Details**: See 04-EXTERNAL-INTEGRATIONS.md
- **API Documentation**: See 05-API-DOCUMENTATION.md
- **Code Analysis**: See 06-CODE-ANALYSIS.md
- **Security Review**: See 07-SECURITY-REVIEW.md
- **Data Flows**: See 09-DATA-FLOWS.md
- **Maintenance**: See 10-MAINTENANCE-NOTES.md
