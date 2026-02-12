# CFIS Data Flows

Comprehensive System Data Flows and Processing

**Document Version**: 1.0
**Last Updated**: February 2026

---

## Table of Contents

1. [High-Level Data Flows](#high-level-data-flows)
2. [Candidate Registration Flow](#candidate-registration-flow)
3. [Financial Transaction Processing](#financial-transaction-processing)
4. [Report Generation Flow](#report-generation-flow)
5. [Document Management Flow](#document-management-flow)
6. [Data Synchronization](#data-synchronization)

---

## High-Level Data Flows

### Primary Data Ingestion Routes

```
External Data Sources
    │
    ├─ Campaign Committee Filings (CSV)
    │  └─ cfisintk.pbl: Parse and import
    │
    ├─ Bank Account Exports (Fixed-width)
    │  └─ cfispmt.pbl: Reconcile transactions
    │
    ├─ Manual Data Entry (UI)
    │  └─ PowerBuilder Forms: Validation
    │
    └─ Web Service Calls (SOAP)
       └─ CmoService: Async processing

↓

Database (SQL Server)
    ├─ Candidate data
    ├─ Financial transactions
    ├─ Audit trail
    └─ Document references

↓

Public Interface (Web)
    ├─ Voter Guide (ASPX)
    ├─ Search Interface (HTML)
    └─ Data Export (XML)
```

---

## Candidate Registration Flow

### Step 1: Candidate Entry

```
Campaign Staff/UI
    │
    ├─ Input: Candidate name, office, district
    │
    ├─ cfiscand.pbl:RegisterCandidate()
    │  ├─ Validate inputs
    │  ├─ Check for duplicates
    │  └─ Generate Cand_ID
    │
    └─ Database: INSERT candidates table
       ├─ Cand_ID (PK)
       ├─ Name
       ├─ Office_Type
       ├─ District
       ├─ Election_Cycle
       └─ Registration_Date
```

### Step 2: Committee Setup

```
User Action: "Link Committee"
    │
    ├─ cfiscand.pbl:LinkCommittee()
    │  ├─ Accept committee name
    │  ├─ Verify bank account (if provided)
    │  └─ Generate Comm_ID
    │
    └─ Database: INSERT committees table
       ├─ Comm_ID (PK)
       ├─ Cand_ID (FK)
       ├─ Committee_Name
       └─ Bank_Account_No
```

### Step 3: Filing Schedule Setup

```
Auto-triggered: File filing schedule
    │
    ├─ cfiscand.pbl:SetupFilingSchedule()
    │  ├─ Get election cycle dates
    │  ├─ Calculate due dates per rules
    │  └─ Create filing schedule
    │
    └─ Database: INSERT statements table
       ├─ Statement_No (PK)
       ├─ Cand_ID (FK)
       ├─ Due_Date
       ├─ Report_Type
       └─ Status (Not Filed)
```

### Step 4: Notification

```
Async Event: Filing deadline reached
    │
    ├─ Email: "Filing due in 5 days"
    │  └─ CmoService.PostMessage()
    │
    └─ OnBase: Document created
       ├─ Deadline notice
       ├─ Filed by: System
       └─ Indexed by: Cand_ID
```

---

## Financial Transaction Processing

### Intake Process

```
File: transactions_2005.csv
    │
    ├─ cfisintk.pbl:ProcessFile()
    │  ├─ Read file (CSV/fixed-width)
    │  ├─ Parse each row
    │  ├─ Validate against Schema.ini
    │  ├─ Apply business rules
    │  │  ├─ Check donation limits
    │  │  ├─ Verify contributor address
    │  │  └─ Categorize contribution type
    │  └─ Batch mode processing
    │
    ├─ Database: BEGIN TRANSACTION
    │  ├─ INSERT transactions
    │  │  ├─ Transaction_ID
    │  │  ├─ Cand_ID
    │  │  ├─ Amount
    │  │  ├─ Trans_Date
    │  │  ├─ Trans_Type
    │  │  └─ Purpose_CD
    │  │
    │  ├─ INSERT contributors
    │  │  ├─ Last_Name
    │  │  ├─ First_Name
    │  │  ├─ Address
    │  │  └─ Employment
    │  │
    │  └─ INSERT audit_trail (logged automatically)
    │     ├─ Action: INSERT
    │     ├─ Table: transactions
    │     ├─ Record_ID
    │     ├─ Changed_By: System
    │     └─ Changed_Date: NOW()
    │
    └─ Database: COMMIT if valid, ROLLBACK if errors
```

### Manual Entry Process

```
User: Click "Add Transaction"
    │
    ├─ UI Form: Transaction entry
    │  ├─ Candidate (dropdown)
    │  ├─ Contributor name
    │  ├─ Amount
    │  ├─ Date
    │  └─ Category
    │
    ├─ Client-side validation
    │  ├─ Required fields check
    │  ├─ Amount > 0
    │  └─ Date <= today
    │
    ├─ cfispmt.pbl:RecordTransaction()
    │  ├─ Server-side validation
    │  ├─ Donation limit check
    │  ├─ Duplicate check
    │  └─ Generate Transaction_ID
    │
    └─ Database: INSERT transaction
       ├─ Audit trail updated
       └─ UI: Confirmation message
```

### Transaction Reconciliation

```
Daily Batch Job: 22:00
    │
    ├─ cfispmt.pbl:ReconcileAccounts()
    │  ├─ Get bank statement data
    │  ├─ Query: transactions for day
    │  ├─ Calculate expected balance
    │  ├─ Compare to bank balance
    │  └─ Report discrepancies
    │
    └─ If discrepancies:
       ├─ Email alert to CFO
       ├─ Flag transactions for review
       └─ OnBase: Exception report
```

---

## Report Generation Flow

### Voter Guide Generation

```
User: Click "Generate Voter Guide"
    │
    ├─ UI Dialog:
    │  ├─ Select election cycle
    │  ├─ Select candidate
    │  └─ Choose format (PDF/HTML/XML)
    │
    ├─ cfisrptd.pbl:GenerateVoterGuide()
    │  │
    │  ├─ Query database:
    │  │  ├─ SELECT candidate data
    │  │  ├─ SELECT financial summary
    │  │  │  └─ SUM(amount) BY purpose_cd
    │  │  └─ SELECT contributions (top 10)
    │  │
    │  ├─ Apply formatting rules
    │  │  ├─ Currency formatting
    │  │  ├─ Date formatting
    │  │  └─ Totals calculation
    │  │
    │  └─ Render output
    │     ├─ PDF: Use PDF library
    │     ├─ HTML: Use template
    │     └─ XML: Serialize data
    │
    ├─ File system: Save report
    │  └─ /reports/voter_guide_2005_123.pdf
    │
    ├─ Database: Log generation
    │  └─ INSERT report_log
    │
    └─ UI: Download link to file
```

### Campaign Finance Statement Report

```
User: Submit filing statement
    │
    ├─ UI: Statement form completed
    │
    ├─ cfisrptm.pbl:GenerateStatement()
    │  ├─ Query transactions by category
    │  │  ├─ Contributions received
    │  │  ├─ Expenditures made
    │  │  ├─ In-kind contributions
    │  │  └─ Loans (if any)
    │  │
    │  ├─ Calculate totals
    │  │  ├─ Cash on hand
    │  │  ├─ Debts outstanding
    │  │  └─ Net financial position
    │  │
    │  └─ Validation checks
    │     ├─ Math verification
    │     ├─ Completeness check
    │     └─ Regulatory compliance
    │
    ├─ Database: INSERT statement record
    │  ├─ Statement_No
    │  ├─ Cand_ID
    │  ├─ Filing_Date
    │  └─ Status: Filed
    │
    ├─ OnBase: Store statement
    │  ├─ PDF copy archived
    │  ├─ Indexed by Cand_ID
    │  └─ Audit trail created
    │
    └─ Notification: Email confirmation
       └─ CmoService.PostMessage()
```

---

## Document Management Flow

### Document Upload to OnBase

```
User: "Attach audit letter"
    │
    ├─ File selection dialog
    │  └─ Letter_2005_Candidate_123.pdf
    │
    ├─ Metadata collection
    │  ├─ Election_Cycle: 2005
    │  ├─ Candidate_ID: 123
    │  ├─ Document_Type: Audit Letter
    │  ├─ Created_Date: 2026-02-07
    │  └─ Created_By: staff_user
    │
    ├─ cfisadm.pbl:UploadDocument()
    │  ├─ Validate PDF (file format)
    │  ├─ Create COM object
    │  │  └─ OnBaseUnityUploadApi.CreateDocument()
    │  │
    │  ├─ Set metadata
    │  │  ├─ SetProperty("ElectionCycle", "2005")
    │  │  ├─ SetProperty("CandidateID", "123")
    │  │  └─ SetProperty("DocType", "AuditLtr")
    │  │
    │  ├─ Add file content
    │  │  └─ AddContent(file_binary_data)
    │  │
    │  └─ SaveDocument()
    │     └─ Returns: Document_ID (OnBase)
    │
    ├─ Database: Store reference
    │  └─ INSERT document_references
    │     ├─ Cand_ID
    │     ├─ Onbase_Doc_ID
    │     ├─ Document_Type
    │     └─ Upload_Date
    │
    └─ UI: Success message
       └─ "Document uploaded (ID: 12345)"
```

### Document Retrieval

```
User: "View audit letter"
    │
    ├─ Click document link
    │
    ├─ Query database:
    │  └─ SELECT Onbase_Doc_ID FROM document_references
    │     WHERE Cand_ID = 123
    │
    ├─ cfisadm.pbl:RetrieveDocument()
    │  ├─ Create COM object
    │  ├─ OnBaseUnityUploadApi.GetDocument(doc_id)
    │  ├─ Read binary content
    │  └─ Return to client
    │
    └─ Browser: Display PDF
```

---

## Data Synchronization

### Multi-Database Sync (Periodic)

```
Nightly Batch: 23:00
    │
    ├─ cfiscvsm.pbl:SyncDatabases()
    │  ├─ Connect to db2005 (source)
    │  ├─ Query: Changes since last sync
    │  │
    │  ├─ FOR EACH candidate change:
    │  │  ├─ Replicate to db2005x (replica)
    │  │  ├─ Replicate to archive database
    │  │  └─ Log sync event
    │  │
    │  └─ Verify replication
    │     ├─ Check row counts match
    │     ├─ Validate checksums
    │     └─ Alert if mismatch
    │
    └─ Database: Log replication status
       └─ Last_Sync: NOW()
```

### Web Cache Invalidation

```
Event: Data modified in database
    │
    ├─ Database trigger:
    │  └─ INSERT audit_log (for web cache invalidation)
    │
    ├─ Web application monitors audit log
    │  ├─ Detects change
    │  ├─ Invalidates related cache entries
    │  └─ Next request rebuilds from DB
    │
    └─ Result: Web always shows current data
       (30-second lag maximum)
```

---

## Error Handling and Recovery

### Transaction Rollback on Error

```
Processing file with invalid row:
    │
    ├─ Row 150: Invalid amount field
    │
    ├─ Validation detects error
    │
    ├─ Database: ROLLBACK ALL changes in batch
    │  └─ Partial batch not committed
    │
    ├─ Error logging:
    │  └─ INSERT error_log
    │     ├─ Row_number: 150
    │     ├─ Error: Invalid amount
    │     ├─ Data: [original row]
    │     └─ Action: User corrects and resubmits
    │
    └─ Notification: Email error report
       ├─ "Batch failed at row 150"
       ├─ "Reason: Invalid amount"
       └─ "Resubmit after correction"
```

### Connection Retry Logic

```
Database connection fails
    │
    ├─ cfisfn.pbl:RetryableQuery()
    │  ├─ Attempt 1: Connect → FAIL
    │  ├─ Wait 1 second
    │  ├─ Attempt 2: Connect → FAIL
    │  ├─ Wait 2 seconds
    │  ├─ Attempt 3: Connect → FAIL
    │  ├─ Wait 4 seconds
    │  ├─ Attempt 4: Connect → SUCCESS
    │  │
    │  └─ Execute query
    │     └─ Return results
    │
    └─ Log: "Reconnected after 3 retries (7 seconds)"
```

---

## Performance Characteristics

### Typical Response Times

| Operation          | Data Volume   | Typical Time | Max Time |
| ------------------ | ------------- | ------------ | -------- |
| Candidate lookup   | Single        | 100ms        | 500ms    |
| Transaction search | 1,000         | 500ms        | 2,000ms  |
| Report generation  | 10,000+       | 5,000ms      | 30,000ms |
| Voter guide render | Per candidate | 1,000ms      | 5,000ms  |
| Document upload    | 1-5MB         | 2,000ms      | 10,000ms |
| Batch import       | 1,000 rows    | 3,000ms      | 15,000ms |

### Optimization Opportunities

- Add pagination to large result sets
- Implement result caching for reference data
- Parallelize independent report generation
- Pre-calculate common report views
