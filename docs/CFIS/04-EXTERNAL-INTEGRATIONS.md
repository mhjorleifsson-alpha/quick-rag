# CFIS External Integrations

Complete Integration Details with External Systems

**Document Version**: 1.0
**Last Updated**: February 2026

---

## Table of Contents

1. [Integration Overview](#integration-overview)
2. [OnBase Document Management](#onbase-document-management)
3. [CmoService Web Services](#cmoservice-web-services)
4. [Database Connectivity](#database-connectivity)
5. [Integration Patterns](#integration-patterns)
6. [Error Handling](#error-handling)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting](#troubleshooting)

---

## Integration Overview

CFIS integrates with three major external systems:

```
CFIS Application
    │
    ├─ OnBase (Document Management)
    │  └─ COM-based synchronous integration
    │  └─ Local or network document repository
    │
    ├─ CmoService (Campaign Management Office)
    │  └─ SOAP-based asynchronous integration
    │  └─ Remote web service endpoint
    │
    └─ SQL Server Databases
       └─ Multiple instances for different election cycles
       └─ Shared Memory protocol for local connections
```

### Integration Characteristics

| Aspect              | OnBase           | CmoService       | Database         |
| ------------------- | ---------------- | ---------------- | ---------------- |
| **Protocol**        | COM/DCOM         | SOAP/HTTP        | ODBC             |
| **Sync Model**      | Synchronous      | Asynchronous     | Synchronous      |
| **Deployment**      | Local/Network    | Remote           | Local/Network    |
| **Version Support** | OnBase 2010+     | Dynamic          | SQL 2000-2012    |
| **Failure Mode**    | Blocks operation | Queued for retry | Connection error |

---

## OnBase Document Management

### Connection Architecture

```
PowerBuilder Application
    │
    ├─ OnBaseUnityUploadApi.dll (COM Object)
    │  ├─ ProgID: Hummingbird.OnBase.API.Interop
    │  └─ Supports COM marshalling across processes
    │
    ├─ Local OnBase Client Installation
    │  ├─ OnBase Service (running locally)
    │  └─ Document cache and indexes
    │
    └─ Network OnBase Server
       ├─ Central repository
       └─ Authentication and authorization
```

### API Components

**Primary Interface** (OnBaseUnityUploadApi.dll):

- Version: Typically OnBase 2010+ compatible
- CLSID: Registered in Windows registry
- Threading: Apartment-threaded (STA)
- Registration: Required via regsvr32 or COM registration

### Document Upload Flow

```
PowerBuilder Code
    │
    ├─ Create document object
    │  └─ Set metadata (cycle, candidate, type)
    │
    ├─ Prepare file content
    │  └─ Load file from disk or memory
    │
    ├─ Call OnBase API
    │  ├─ CreateDocument()
    │  ├─ AddContent()
    │  └─ SaveDocument()
    │
    ├─ OnBase Client Process
    │  └─ Validate document
    │
    ├─ Network Transfer (if needed)
    │  └─ Send to OnBase Server
    │
    └─ OnBase Server
       ├─ Store document
       ├─ Index metadata
       ├─ Create audit trail
       └─ Return document ID
```

### Document Types Supported

**Campaign Finance Documents**:

1. **Audit Letters**
   - Initial document request letters
   - Draft audit report responses
   - Final audit report submissions
   - Created by compliance staff
   - Indexed by: Election Cycle, Candidate ID, Document Type

2. **Correspondence**
   - Candidate notifications
   - Committee communications
   - Penalty notices
   - Payment reminders
   - Indexed by: Communication Date, Recipient, Subject

3. **Filed Statements**
   - Campaign finance disclosures
   - Amendments to statements
   - Supporting documentation
   - Indexed by: Filing Date, Statement Number, Cycle

4. **Audit Documentation**
   - Review workpapers
   - Compliance findings
   - Exception reports
   - Indexed by: Audit Period, Finding Type

### Configuration

**Connection Parameters**:

```
OnBase Server Name: [Configured in application]
Repository Name: Campaign Finance
User Credentials: [Integrated Windows Auth or explicit]
Connection Timeout: 30 seconds (default)
Retry Policy: 3 retries on transient failure
```

**Metadata Schema** (custom for CFIS):

```
Election_Cycle: 2001, 2003, 2005, 2007, 2009, 2010, 2012
Candidate_ID: Numeric identifier from CFIS
Document_Type: Letter, Report, Filing, Correspondence
Created_Date: ISO 8601 format
Created_By: Windows username
Department: Campaign Finance Board
```

### Error Handling

**Common OnBase Errors**:
| Error | Cause | Resolution |
|-------|-------|-----------|
| E_FAIL (0x80004005) | Connection failed | Check OnBase service status |
| E_NOINTERFACE | API version mismatch | Update OnBase client |
| E_ACCESSDENIED | Authentication failed | Verify Windows permissions |
| E_INVALIDARG | Bad metadata | Validate document object |

---

## CmoService Web Services

### Service Endpoint

**Primary Endpoint**: http://c-accessprod:8007/CAccess/CmoService/

**Alternative Endpoints**: Configurable via AppSettings

**Service Type**: SOAP 1.1 Web Service
**WSDL Location**: http://c-accessprod:8007/CAccess/CmoService?wsdl

### Service Methods

#### 1. PostMessage()

Posts a generic message with optional attachments

**Signature**:

```csharp
void PostMessage(
    string electionCycle,
    string candidateID,
    string creator,
    string title,
    string body,
    string receiptEmail,
    byte[] attachmentData,
    string attachmentName,
    bool notify,
    out int result,
    out bool resultSpecified
)
```

**Parameters**:

- `electionCycle`: Election year (e.g., "2005")
- `candidateID`: Numeric candidate identifier
- `creator`: User or system creating message
- `title`: Message subject line
- `body`: Message content (plain text or HTML)
- `receiptEmail`: Email for confirmation
- `attachmentData`: Binary file data (base64 encoded in SOAP)
- `attachmentName`: Filename for attachment
- `notify`: Whether to send email notification
- `result`: Return code (0=success)
- `resultSpecified`: Whether result was set

**Example Usage**:

```csharp
CmoService service = new CmoService();
service.PostMessage(
    "2005",
    "123",
    "cfisadmin",
    "Campaign Finance Filing",
    "Your filing has been received and is under review.",
    "candidate@email.com",
    pdfData,
    "filing_2005.pdf",
    true,
    out int resultCode,
    out bool resultSet
);
```

#### 2. PostPaymentLetter()

Submits payment-related correspondence

**Purpose**: Submit payment status letters or payment confirmations
**Async**: Yes, returns immediately and processes in background queue

#### 3. PostPaymentLetterByPath()

Submits payment letter from file path

**Purpose**: File-based letter submission for systems without binary data
**Parameters**: File path, candidate ID, letter type

#### 4. PostTollingLetter()

Posts tolling letters (compliance notifications)

**Purpose**: Send compliance tolling notices (notifications that reset deadline clocks)
**Usage**: Compliance staff notifications of extension periods

#### 5. PostInitialDocumentRequest()

Initiates document request for audit

**Purpose**: Start audit document collection process
**Triggers**: Creates document request workflow
**Notification**: Email sent to candidate/committee

#### 6. PostDraftAuditReport()

Submits draft audit report

**Purpose**: Send draft findings for candidate response
**Process**: Candidate has 30 days to respond to draft findings
**Storage**: Archived in OnBase and database

#### 7. PostFinalAuditReport()

Submits final audit report

**Purpose**: Post final audit results
**Effect**: Closes audit cycle for that election
**Public**: May be published on website

#### 8. PostStatementReview()

Posts statement review documents

**Purpose**: Submit financial statement review results
**Recipient**: Campaign committee and candidate
**Archive**: Stored for public inquiry

### Asynchronous Processing

**Async Pattern** (from CmoService.cs):

```csharp
// Event-based callback
public event PostMessageCompletedEventHandler PostMessageCompleted;

// Start async operation
public void PostMessageAsync(string electionCycle, string candidateID, ...);

// Retrieve result when complete
public void EndPostMessage(IAsyncResult asyncResult, out int result, out bool resultSpecified);

// Handler
private void OnPostMessageCompleted(object sender, PostMessageCompletedEventArgs e)
{
    if (e.Error != null)
    {
        // Handle error
    }
    else if (e.Result.PostMessageResult == 0)
    {
        // Success
    }
}
```

### Configuration

**Connection Settings** (from asasrv.ini):

```ini
[CmoService]
Endpoint=http://c-accessprod:8007/CAccess/CmoService/
Timeout=30000
MaxRetries=3
QueueSize=1000
```

**AppSettings Override** (App.config):

```xml
<appSettings>
    <add key="EndpointURL"
         value="http://c-accessprod:8007/CAccess/CmoService/" />
</appSettings>
```

### Message Queue Semantics

**Delivery Guarantee**: At-least-once
**Ordering**: FIFO per candidate ID
**Timeout**: 5 minutes per message
**Dead Letter Queue**: Failed messages after 5 retries

---

## Database Connectivity

### Connection Strings

**Format** (Shared Memory):

```
DSN=dbXXXX;UID=CFIS_USER;PWD=***
```

**Format** (Named Pipes):

```
Server=DBSERVER\SQLEXPRESS;Database=cfis;Integrated Security=true;
```

### Database Selection Logic

**By Election Cycle**:

| Cycle     | Primary DB | Replica          | Purpose           |
| --------- | ---------- | ---------------- | ----------------- |
| 2000-2003 | db2000     | ndb2000          | Historical        |
| 2005      | db2005     | db2005x          | General + Primary |
| 2007      | db2007     | db2007a, db2007b | Election Year     |
| 2009      | db2009     | -                | Election Year     |
| 2010+     | db2010     | db2012           | Current           |

**Selection Criteria**:

1. Get election cycle from session/parameter
2. Look up in database mapping table
3. Connect to primary or replica based on load
4. Fall back to replica if primary unavailable

### Connection Pooling

**Pool Configuration**:

```
Min Pool Size: 5
Max Pool Size: 100
Connection Timeout: 15 seconds
Idle Timeout: 5 minutes
Max Lifetime: 30 minutes
```

**Pool Reuse**:

- Connections automatically returned to pool
- Tested on checkout for validity
- Stale connections purged periodically

### Multi-Database Transactions

**Pattern for Multi-Cycle Operations**:

```
CFIS Application
    │
    ├─ Connect to db2005 (primary cycle)
    ├─ Begin transaction
    │  ├─ Update candidates table
    │  ├─ Insert transactions
    │  └─ Commit on db2005
    │
    └─ Connect to db2005x (replica)
       └─ Replicate changes (asynchronous)
```

---

## Integration Patterns

### Pattern 1: Document Upload on Report Finalization

```
Report Generation Complete
    │
    ├─ Generate PDF
    │
    ├─ Prepare OnBase metadata
    │  ├─ Election_Cycle = 2005
    │  ├─ Candidate_ID = 123
    │  ├─ Document_Type = "Report"
    │  └─ Created_Date = NOW()
    │
    ├─ Call OnBase API
    │  ├─ CreateDocument()
    │  ├─ SetMetadata()
    │  ├─ AddContent(pdfData)
    │  └─ SaveDocument()
    │
    ├─ OnBase Returns Document ID
    │
    └─ Store Document ID in cfis.document_references table
```

### Pattern 2: Asynchronous Message Posting

```
Compliance Officer: Send Letter
    │
    ├─ Prepare letter content
    │
    ├─ Call CmoService.PostMessageAsync()
    │  ├─ Queue message immediately (returns to user)
    │  └─ Register completion handler
    │
    │ [CmoService Processing in Background]
    │
    ├─ Event Handler Invoked When Complete
    │  ├─ Check result code
    │  ├─ Log to audit trail
    │  ├─ Send confirmation email if needed
    │  └─ Update UI to show completion
    │
    └─ User Sees Status Update
```

### Pattern 3: Multi-Database Candidate Lookup

```
Search for Candidate: "John Smith"
    │
    ├─ Query current cycle database (db2005)
    │  ├─ Search candidates table
    │  └─ Get results: [123, 456]
    │
    ├─ Query prior cycles if requested
    │  ├─ db2003: [789]
    │  ├─ db2001: [012]
    │  └─ Combine results: [123, 456, 789, 012]
    │
    └─ Display unified candidate list to user
```

---

## Error Handling

### OnBase Integration Errors

**Error Handling Strategy**:

```
Call OnBase API
    │
    ├─ Success
    │  └─ Log completion, return document ID
    │
    └─ Failure
       ├─ Catch COM exception
       ├─ Classify error (transient vs permanent)
       ├─ If transient (network timeout)
       │  └─ Retry up to 3 times with exponential backoff
       │  └─ If all retries fail, queue for later retry
       │
       ├─ If permanent (authentication, bad metadata)
       │  └─ Log error details
       │  └─ Display user-friendly error message
       │  └─ Send alert to administrator
       │
       └─ Never silently fail (document loss)
```

**Common Scenarios**:

| Scenario                | Error              | Handling                          |
| ----------------------- | ------------------ | --------------------------------- |
| OnBase service down     | Connection timeout | Retry 3x, queue for later         |
| Bad document object     | E_INVALIDARG       | Validate metadata, log details    |
| Authentication failed   | E_ACCESSDENIED     | Check service account permissions |
| Network latency         | Timeout            | Retry with longer timeout         |
| Document already exists | E_ALREADYEXISTS    | Return existing ID or update      |

### CmoService Integration Errors

**Async Error Handling**:

```csharp
service.PostMessageCompleted += (sender, args) =>
{
    if (args.Error != null)
    {
        // Network or SOAP fault
        LogError("PostMessage failed", args.Error);
        QueueForRetry(message);
    }
    else if (args.Result.PostMessageResult != 0)
    {
        // Application error code
        LogError($"Service returned: {args.Result.PostMessageResult}");
        NotifyAdministrator(args.Result.PostMessageResult);
    }
    else
    {
        // Success
        UpdateAuditTrail("Message posted successfully");
    }
};
```

### Database Connectivity Errors

**Connection Error Strategy**:

```
Database Operation
    │
    ├─ Get connection from pool
    │
    ├─ Execute query
    │
    └─ Error
       ├─ Connection lost mid-operation
       │  └─ Rollback transaction
       │  └─ Return connection to pool (marked invalid)
       │  └─ Retry operation up to 3 times
       │
       ├─ Connection refused
       │  └─ Try alternate database (replica)
       │  └─ Check network connectivity
       │  └─ Notify database administrator
       │
       └─ Timeout
          └─ Kill long-running query
          └─ Log details for investigation
          └─ Return error to user
```

---

## Performance Considerations

### OnBase Integration Performance

**Bottlenecks**:

1. Document upload size (large PDFs)
2. Metadata indexing latency
3. Network latency to OnBase server
4. Local OnBase service responsiveness

**Optimizations**:

```
Document Upload (Large PDF)
    │
    ├─ Compress PDF before upload (40% size reduction typical)
    ├─ Use binary protocol (not text-based encoding)
    ├─ Batch metadata updates (multiple docs together)
    ├─ Implement local caching to avoid re-upload
    └─ Monitor upload performance metrics
```

**Monitoring**:

- Average upload time per document
- Failed uploads (retry count)
- OnBase service availability
- Network latency to OnBase server

### CmoService Integration Performance

**Async Benefits**:

- UI doesn't block during message posting
- Messages queued for reliable delivery
- Multiple messages can be queued in parallel
- Remote processing doesn't impact client

**Monitoring**:

- Message queue depth (should be <100 normally)
- Message processing latency (target <30s)
- Failed message count
- Service endpoint availability

### Database Query Performance

**Query Optimization**:

```sql
-- Poor (full table scan)
SELECT * FROM transactions WHERE Cand_ID = 123

-- Better (uses indexed lookup)
SELECT * FROM transactions
WHERE Election_Cycle = 2005 AND Cand_ID = 123
ORDER BY Trans_Date DESC

-- Best (covered index)
CREATE INDEX idx_cycle_cand_date
ON transactions(Election_Cycle, Cand_ID, Trans_Date DESC)
INCLUDE (Amount, Purpose_CD)
```

---

## Troubleshooting

### OnBase Issues

**Issue**: "OnBase API not available"
**Symptoms**: COM object creation fails
**Resolution**:

1. Verify OnBaseUnityUploadApi.dll is registered: `regsvr32 /s "C:\path\to\OnBaseUnityUploadApi.dll"`
2. Check Windows Event Viewer for COM registration errors
3. Verify OnBase service is running
4. Check network connectivity to OnBase server

**Issue**: "Document upload timeout"
**Symptoms**: Upload hangs for >2 minutes
**Resolution**:

1. Check network bandwidth (not saturated)
2. Check OnBase service CPU/memory
3. Reduce document size or compress
4. Increase timeout setting if needed

### CmoService Issues

**Issue**: "SOAP fault: Server unavailable"
**Symptoms**: All message posting fails
**Resolution**:

1. Verify endpoint URL is correct (check asasrv.ini)
2. Test network connectivity: `ping c-accessprod`
3. Check firewall rules for port 8007
4. Verify DNS resolution for c-accessprod

**Issue**: "Message stuck in queue"
**Symptoms**: Message not processed, appears forever in queue
**Resolution**:

1. Check CmoService background worker status
2. Review CmoService application logs
3. Check if message has parsing error
4. Move to dead letter queue and log for investigation

### Database Issues

**Issue**: "Connection to db2005 refused"
**Symptoms**: Cannot connect to primary database
**Resolution**:

1. Check SQL Server service is running
2. Verify database exists: `SELECT * FROM sys.databases`
3. Check connection string syntax
4. Verify user account has login permissions
5. Check shared memory protocol is enabled

**Issue**: "Query timeout exceeded"
**Symptoms**: Long-running report generation times out
**Resolution**:

1. Identify slow query (enable query profiling)
2. Add indexes for filtering columns
3. Break query into smaller operations
4. Increase query timeout setting
5. Consider archiving old data to improve performance

---

## Monitoring and Maintenance

### Health Checks

**Hourly**:

- Verify OnBase service responds to API calls
- Check CmoService endpoint availability
- Test database connectivity to all instances

**Daily**:

- Review integration error logs
- Check message queue depth
- Verify no stuck operations

**Weekly**:

- Analyze integration performance metrics
- Review failed retry counts
- Plan preventive maintenance if needed

**Monthly**:

- Audit integration security (credentials not exposed)
- Review integration documentation for updates
- Test disaster recovery procedures

### Alert Thresholds

| Metric                        | Warning | Critical |
| ----------------------------- | ------- | -------- |
| OnBase API latency            | >5s     | >30s     |
| CmoService queue depth        | >100    | >500     |
| Database response time        | >1s     | >5s      |
| Failed message count (hourly) | >10     | >100     |
| OnBase uptime                 | <99.5%  | <99%     |
