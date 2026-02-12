# CFIS API Documentation

Complete REST and SOAP API Reference

**Document Version**: 1.0
**Last Updated**: February 2026

---

## Table of Contents

1. [CmoService SOAP API](#cmoservice-soap-api)
2. [PowerBuilder Component APIs](#powerbuilder-component-apis)
3. [Database Stored Procedures](#database-stored-procedures)
4. [Error Codes](#error-codes)
5. [Authentication](#authentication)

---

## CmoService SOAP API

### Service Base URL

```
http://c-accessprod:8007/CAccess/CmoService/
```

### WSDL

```
http://c-accessprod:8007/CAccess/CmoService?wsdl
```

### Authentication

- Integrated Windows Authentication (domain accounts)
- Service account: CFIS_SERVICE@domain.local
- Permissions: Read/Write to Campaign Finance repository

### Methods Reference

#### PostMessage

Posts a generic campaign message.

**Request**:

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <PostMessage xmlns="http://caccess.nyccfb.info/schema/data">
      <electionCycle>2005</electionCycle>
      <candidateID>123</candidateID>
      <creator>CFISADMIN</creator>
      <title>Filing Confirmation</title>
      <body>Your filing has been received.</body>
      <receiptEmail>candidate@example.com</receiptEmail>
      <attachmentData>[base64 encoded PDF]</attachmentData>
      <attachmentName>filing_2005.pdf</attachmentName>
      <notify>true</notify>
    </PostMessage>
  </soap:Body>
</soap:Envelope>
```

**Response**:

```xml
<PostMessageResponse>
  <PostMessageResult>0</PostMessageResult>
  <PostMessageResultSpecified>true</PostMessageResultSpecified>
</PostMessageResponse>
```

**Result Codes**:

- 0: Success
- 1: Invalid election cycle
- 2: Candidate not found
- 3: Invalid attachment
- 4: Email not sent
- 5: System error

#### PostPaymentLetter

Submits payment-related correspondence.

**Parameters**:

- `electionCycle`: Election year
- `candidateID`: Candidate ID
- `letterType`: "Payment", "Receipt", "Reminder"
- `paymentAmount`: Dollar amount
- `dueDate`: Due date (ISO 8601)

#### PostTollingLetter

Sends tolling letter (deadline extension notification).

**Parameters**:

- `electionCycle`: Election year
- `candidateID`: Candidate ID
- `tollingPeriodDays`: Number of days extension
- `reason`: Reason code

#### PostInitialDocumentRequest

Initiates audit document request process.

**Parameters**:

- `electionCycle`: Election year
- `candidateID`: Candidate ID
- `requestDate`: Request creation date
- `dueDate`: Document due date

#### PostDraftAuditReport

Submits draft audit findings.

**Parameters**:

- `electionCycle`: Election year
- `candidateID`: Candidate ID
- `reportContent`: XML audit report
- `responseDeadline`: Days allowed for response

#### PostFinalAuditReport

Posts final audit results.

**Parameters**:

- `electionCycle`: Election year
- `candidateID`: Candidate ID
- `finalReport`: Complete audit report (PDF)
- `penalties`: Penalty recommendations

#### PostStatementReview

Posts statement review findings.

**Parameters**:

- `electionCycle`: Election year
- `candidateID`: Candidate ID
- `statementNumber`: Statement being reviewed
- `findings`: Review findings

---

## PowerBuilder Component APIs

### Candidate Management API

**cfiscand.pbl Functions**:

```powerscript
// Register new candidate
PUBLIC FUNCTION RegisterCandidate(
    ls_name STRING,
    li_office INT,
    li_district INT,
    ls_party STRING
) RETURNS INT
// Returns: candidate_id or error code

// Update candidate status
PUBLIC FUNCTION UpdateCandidateStatus(
    li_candidateID INT,
    ls_status STRING  // "Active", "Withdrawn", "Rejected"
) RETURNS BOOLEAN

// Get candidate by ID
PUBLIC FUNCTION GetCandidate(
    li_candidateID INT,
    rs_candidate REF candidate_str
) RETURNS BOOLEAN

// Search candidates
PUBLIC FUNCTION SearchCandidates(
    ls_name STRING,
    li_election_cycle INT,
    rs_results REF ResultSet
) RETURNS INT
```

### Financial Transaction API

**cfispmt.pbl Functions**:

```powerscript
// Record financial transaction
PUBLIC FUNCTION RecordTransaction(
    li_candidateID INT,
    ls_type STRING,      // "Receipt", "Expenditure", "InKind"
    ld_amount DECIMAL,
    ld_trans_date DATE,
    ls_contributor STRING,
    ls_purpose STRING
) RETURNS INT

// Get transaction totals
PUBLIC FUNCTION GetTransactionTotals(
    li_candidateID INT,
    li_election_cycle INT,
    rs_totals REF totals_str
) RETURNS BOOLEAN

// Reconcile bank account
PUBLIC FUNCTION ReconcileAccount(
    ls_account_number STRING,
    ld_bank_balance DECIMAL,
    ld_book_balance DECIMAL
) RETURNS BOOLEAN
```

### Report Generation API

**cfisrptd.pbl Functions**:

```powerscript
// Generate comprehensive campaign report
PUBLIC FUNCTION GenerateCampaignReport(
    li_candidateID INT,
    li_election_cycle INT,
    ls_format STRING,   // "PDF", "Excel", "XML"
    ls_output_path STRING
) RETURNS BOOLEAN

// Generate financial summary
PUBLIC FUNCTION GenerateFinancialSummary(
    li_candidateID INT,
    ls_summary_type STRING  // "Income", "Expenses", "Both"
) RETURNS summary_str

// Generate audit report
PUBLIC FUNCTION GenerateAuditReport(
    li_candidateID INT,
    li_election_cycle INT,
    rs_findings REF ResultSet
) RETURNS BOOLEAN
```

### Search API

**Cfissrch.pbl Functions**:

```powerscript
// Search transactions
PUBLIC FUNCTION SearchTransactions(
    li_candidateID INT,
    ls_contributor STRING,
    ld_amount_min DECIMAL,
    ld_amount_max DECIMAL,
    ld_date_from DATE,
    ld_date_to DATE,
    rs_results REF ResultSet
) RETURNS INT

// Get search filters
PUBLIC FUNCTION GetSearchFilters(
    rs_filters REF ResultSet
) RETURNS BOOLEAN

// Execute saved search
PUBLIC FUNCTION ExecuteSavedSearch(
    ls_search_name STRING,
    rs_results REF ResultSet
) RETURNS BOOLEAN
```

---

## Database Stored Procedures

### Candidate Management Procedures

```sql
-- Register new candidate
EXEC sp_RegisterCandidate
    @CandidateName NVARCHAR(100),
    @OfficeType INT,
    @DistrictNumber INT,
    @PartyCode NVARCHAR(10),
    @CandidateID INT OUTPUT

-- Update candidate status
EXEC sp_UpdateCandidateStatus
    @CandidateID INT,
    @NewStatus NVARCHAR(20),
    @UpdatedBy NVARCHAR(50)

-- Get candidate information
EXEC sp_GetCandidateInfo
    @CandidateID INT
```

### Financial Procedures

```sql
-- Record transaction
EXEC sp_RecordTransaction
    @CandidateID INT,
    @TransactionType NVARCHAR(20),
    @Amount DECIMAL(12,2),
    @TransactionDate DATE,
    @ContributorName NVARCHAR(100),
    @PurposeCode NVARCHAR(10),
    @TransactionID INT OUTPUT

-- Get transaction totals
EXEC sp_GetTransactionTotals
    @CandidateID INT,
    @ElectionCycle INT

-- Reconcile account
EXEC sp_ReconcileAccount
    @AccountNumber NVARCHAR(20),
    @BankBalance DECIMAL(12,2),
    @BookBalance DECIMAL(12,2)
```

### Reporting Procedures

```sql
-- Generate campaign report
EXEC sp_GenerateCampaignReport
    @CandidateID INT,
    @ElectionCycle INT,
    @ReportFormat NVARCHAR(10)

-- Get financial summary
EXEC sp_GetFinancialSummary
    @CandidateID INT,
    @SummaryType NVARCHAR(20)

-- Generate audit report
EXEC sp_GenerateAuditReport
    @CandidateID INT,
    @ElectionCycle INT
```

---

## Error Codes

### HTTP Error Codes

- 200 OK: Success
- 400 Bad Request: Invalid parameters
- 401 Unauthorized: Authentication failed
- 403 Forbidden: Permission denied
- 404 Not Found: Resource not found
- 500 Internal Server Error: System error
- 503 Service Unavailable: Service down

### SOAP Fault Codes

- soap:Server: Service-side error
- soap:Client: Client-side error
- soap:MustUnderstand: Unsupported header
- soap:VersionMismatch: SOAP version mismatch

### Application Error Codes

| Code     | Message                    | Resolution                         |
| -------- | -------------------------- | ---------------------------------- |
| CFIS_001 | Invalid election cycle     | Check cycle is valid for this year |
| CFIS_002 | Candidate not found        | Verify candidate ID is correct     |
| CFIS_003 | Insufficient permissions   | Contact administrator              |
| CFIS_004 | Database connection failed | Check database availability        |
| CFIS_005 | Invalid transaction        | Verify transaction data            |
| CFIS_006 | OnBase unavailable         | Check OnBase service status        |
| CFIS_007 | Email delivery failed      | Verify email address               |
| CFIS_008 | File format unsupported    | Use supported format (PDF, XLS)    |
| CFIS_009 | Report generation timeout  | Try with smaller date range        |
| CFIS_010 | Audit trail entry failed   | Contact IT support                 |

---

## Authentication

### API Key Authentication (Future)

```
Authorization: Bearer {api_key}
```

### Windows Authentication (Current)

- Use service account credentials
- Enabled for SOAP endpoints
- NTLM or Kerberos authentication

### Token Generation (Future)

```
POST /auth/token
Content-Type: application/json

{
  "username": "cfis_user@domain.local",
  "password": "***"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

### Session Management

- Default session timeout: 30 minutes
- Idle timeout: 15 minutes
- Max concurrent sessions per user: 3

---

## Rate Limiting

### Thresholds (per minute)

- Anonymous: 10 requests
- Authenticated: 100 requests
- Service account: 1000 requests

### Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1645234560
```

---

## Response Format Standards

### Success Response

```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe"
  },
  "timestamp": "2026-02-07T10:30:00Z"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "CFIS_002",
    "message": "Candidate not found",
    "details": "Candidate ID 999 does not exist"
  },
  "timestamp": "2026-02-07T10:30:00Z"
}
```
