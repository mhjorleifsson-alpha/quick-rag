# CFIS Explanation Guide

How the System Works - User and Technical Perspectives

**Document Version**: 1.0
**Last Updated**: February 2026

---

## Table of Contents

1. [Campaign Lifecycle](#campaign-lifecycle)
2. [Financial Tracking Explained](#financial-tracking-explained)
3. [Reporting and Compliance](#reporting-and-compliance)
4. [Public Voter Guide](#public-voter-guide)
5. [Behind the Scenes](#behind-the-scenes)

---

## Campaign Lifecycle

### Phase 1: Campaign Registration (Day 1-7)

**What happens**: A candidate announces their campaign.

**In CFIS**:

1. Campaign staff contacts CFB to register
2. CFB enters candidate information:
   - Candidate name
   - Office sought (Mayor, Council member, etc.)
   - Election cycle (2025, 2026, etc.)
   - Campaign committee name
   - Bank account number
3. CFIS generates unique candidate ID
4. System creates filing schedule with due dates

**Why it matters**: CFIS needs to track this candidate's finances from day one.

### Phase 2: Active Campaign (Day 8 - Election Day)

**What happens**: Campaign runs, accepts donations, spends money.

**In CFIS**:

1. Campaign submits financial reports
   - Weekly filings (if required)
   - Disclosure statements
   - Transaction details

2. CFIS tracks:
   - Contributions received (who, how much, when)
   - Expenditures made (what for, to whom)
   - In-kind contributions (donated services, goods)
   - Current cash balance
   - Outstanding debts

3. CFB staff:
   - Validates submitted data
   - Checks for legal violations (donation limits, etc.)
   - Flags issues requiring clarification
   - Publishes data for public view

**Why it matters**: Campaign finance law requires transparency. Voters and regulators need to know where money comes from.

### Phase 3: Public Disclosure (Ongoing During Campaign)

**What happens**: CFIS publishes campaign financial data.

**Public can see**:

- How much each candidate raised
- Top contributors to each campaign
- How much was spent and on what
- Where the money went

**Published via**:

- Voter Guide (voter.ny.gov - before election)
- Campaign Finance website (nyccfb.info)
- Search database (find specific donors)

### Phase 4: Post-Election (After Election Day)

**What happens**: Final financial reconciliation.

**In CFIS**:

1. Final disclosure statements filed
2. Any loans repaid
3. Remaining cash returned or distributed
4. Candidate filed as "inactive"
5. Audit process begins (if selected)

**Why it matters**: Ensures complete transparency about campaign finances.

---

## Financial Tracking Explained

### How Contributions Are Recorded

**Scenario: Candidate receives $500 check from supporter**

**Step 1: Campaign reports it**

- Campaign submits disclosure report
- Lists: Donor name, address, amount, date, occupation
- CFIS scans for problems:
  - Is this a duplicate entry?
  - Is it within legal limits?
  - Is address complete?

**Step 2: CFB verifies**

- Staff reviews report
- Checks math (total + balance = calculations correct)
- Verifies donations meet legal requirements
- Approves or requests correction

**Step 3: CFIS records**

- Stores contribution in database
- Links to candidate account
- Updates running total

**Step 4: Public sees it**

- Appears in voter guide (10 days later typically)
- Searchable in donation database
- Contributors by amount listed

### How Expenditures Are Tracked

**Scenario: Candidate pays $2,000 for campaign mail**

**Step 1: Campaign reports it**

- Lists: Vendor name, address, amount, date, category (mail, phones, ads, etc.)

**Step 2: CFB verifies**

- Is vendor properly identified?
- Is amount within typical range?
- Is it a permitted use (can't buy votes)?

**Step 3: CFIS records**

- Stores in "expenditures" section
- Categorized by type
- Reduces available cash balance

**Step 4: Public sees it**

- In campaign spending totals
- Aggregated by category
- Shows where money went

### In-Kind Contributions

**Scenario: PR firm donates $5,000 worth of advertising**

**Special handling**:

- Not actual money (hence "in-kind")
- Must be valued (fair market value)
- Counts toward donation limits
- Reported same as cash

**CFIS tracks**:

- Fair market value: $5,000
- Donor: PR firm
- Type: Advertising services
- Treated as donation for legal purposes

---

## Reporting and Compliance

### Mandatory Filing Requirements

**Campaign must file**:

| Filing               | Frequency                  | Due Date                   |
| -------------------- | -------------------------- | -------------------------- |
| Disclosure Statement | Daily (if campaign active) | By 11:59 PM                |
| Periodic Report      | Weekly (pre-election)      | Tuesday before week ends   |
| Quarterly Report     | Every 3 months             | 10 days after quarter ends |
| Final Report         | Once per cycle             | 2 weeks after election     |

**CFIS automation**:

- Sends email reminders 5 days before
- Sends urgent reminder 1 day before
- Accepts filings online or by mail
- Validates completeness

### CFIS Compliance Checks

**Automatic validation**:

1. Is required information complete?
2. Does math add up (totals match items)?
3. Are donations within legal limits?
4. Are vendors properly identified?
5. Are dates in correct range?

**CFB staff review** (if automatic check fails):

- Contacts campaign for clarification
- Requests amended report if needed
- Approves revised filing
- Updates public records

### Penalties for Non-Compliance

**Missing filing**: Campaign notified, fine issued
**Incomplete filing**: Campaign given 10 days to correct
**Illegal donation**: Must be returned, penalty assessed
**False information**: Investigation, potential prosecution

---

## Public Voter Guide

### What Is It?

**The Voter Guide** is a website and printed guide showing:

- Who's running for office
- Campaign finance data for each candidate
- Top contributors to each campaign
- How candidate's campaign spent money

### How CFIS Powers It

**Behind the scenes**:

1. Campaign files financial disclosure
2. CFIS validates and stores data
3. System automatically generates:
   - Candidate profile page
   - Financial summary chart
   - Top 10 contributors list
   - Spending breakdown
   - Comparison to other candidates

**Automatic updates**:

- Voter guide refreshed daily
- Latest filings included
- Shows current rankings

### What Voters See

**Example: Voter searches for Candidate Smith**

**Voter Guide shows**:

- How much Smith raised: $500,000
- Top 5 donors (names, amounts)
- Where money came from:
  - Individuals: 70%
  - Business donations: 20%
  - Other: 10%
- How money was spent:
  - Advertising: 45%
  - Staff: 30%
  - Events: 15%
  - Other: 10%
- Comparison to other candidates
  - Smith: $500K
  - Jones: $750K
  - Garcia: $200K

**Why this matters to voters**:

- Helps identify potential conflicts of interest
- Shows who is funding each candidate
- Allows informed voting decisions

---

## Behind the Scenes

### System Architecture (Simplified)

```
User Input
    │
    ├─ Campaign files report (via website)
    ├─ CFB staff verifies (using CFIS tools)
    ├─ Public queries data (via voter guide)
    │
    ▼
CFIS Processing
    ├─ Validate data (automatic checks)
    ├─ Store in database (organized records)
    ├─ Apply business rules (donation limits, etc.)
    ├─ Generate reports (for CFB and public)
    │
    ▼
Database
    ├─ Candidates table (who's running)
    ├─ Transactions table (all money movements)
    ├─ Contributors table (donor information)
    ├─ Audit trail (what changed when)
    │
    ▼
Output
    ├─ CFB internal tools (staff uses for work)
    ├─ Public voter guide (website, PDF)
    ├─ Campaign reports (financial statements)
    ├─ Compliance reports (who's in violation)
```

### Daily Operations

**Morning**:

- CFB staff logs in to CFIS
- Reviews overnight filings
- Checks for errors or violations

**Throughout day**:

- Campaigns file disclosures
- Staff verifies data
- System updates public voter guide
- Public searches and views data

**Evening**:

- System runs nightly batch jobs
- Backups completed
- Reports generated

### Real-World Example: 2025 Mayoral Campaign

**March 1**: Candidate announces

- CFB enters candidate info into CFIS
- System creates filing schedule
- Media notifications sent

**March 15**: Campaign accepts first donation

- Campaign files: "John Doe, $1,000"
- CFIS checks: Donation is legal, address valid
- Data stored in database

**March 20**: Public searches candidate

- Voter accesses voter guide
- CFIS queries database
- Shows: $1,000 raised so far
- Public sees donor list

**April 30**: Campaign hits $100,000 raised

- Media queries CFIS for stats
- System generates report
- Candidate ranked by funds raised

**June 25**: Election day

- Voting concludes
- Campaign must file final report

**July 10**: Final reconciliation

- Campaign files: All money accounted for
- CFIS audits financial records
- Campaign marked as complete
- Audit process begins

---

## Key Concepts Explained

### What is "Campaign Finance"?

The money involved in political campaigns:

- Where it comes from (donors, loans, campaign funds)
- How much is spent
- What it's spent on
- Follows strict legal rules

### Why Transparency?

**The purpose**:

- Voters know who funds each candidate
- Can identify potential conflicts of interest
- Ensures legal compliance
- Maintains public trust

**How CFIS helps**:

- Records every financial transaction
- Makes data public
- Enables enforcement of laws

### What is "Compliance"?

Following the rules:

- Legal donation limits (can't give too much)
- Proper reporting (deadlines, accuracy)
- Prohibited uses (can't buy votes)
- Required disclosures (tell the public)

**CFIS's role**:

- Tracks compliance automatically
- Flags violations for investigation
- Ensures penalties enforced

### What is "Audit Trail"?

A complete record of what changed:

- When data was entered
- Who entered it
- What changed
- When it was changed

**Why it matters**:

- Can track corrections
- Can identify errors or intentional changes
- Supports investigation if fraud suspected

---

## FAQs

### Q: How accurate is the public data?

**A**: Campaigns are responsible for accuracy. CFIS performs automatic checks, and CFB staff reviews filings. However, if campaign provides false information, it may not be caught immediately.

**Public should know**:

- Voter guide shows what campaigns reported
- Doesn't guarantee accuracy (spot-check inconsistencies)
- Public can report suspected violations

### Q: Can I find out who donated to a specific candidate?

**A**: Yes, through the voter guide or campaign finance search. Top donors are published publicly (with some exceptions for certain contributions).

**Privacy note**: Donations above certain amounts are public record in most cases.

### Q: How often is the voter guide updated?

**A**: Daily. New filings are typically included within 24 hours.

### Q: What if I disagree with how campaign classified a donation?

**A**: Report to CFB. Staff will investigate and request correction if needed.

### Q: How long are records kept?

**A**: Permanently archived. Historical data available for past elections.

---

## Conclusion

CFIS is the backbone of campaign finance transparency in NYC. It:

- Records every campaign financial transaction
- Validates legal compliance
- Publishes data to the public
- Enables CFB to enforce rules

**For campaigns**: Efficient filing and reporting
**For the public**: Transparent access to campaign funding data
**For CFB**: Tools to monitor and enforce compliance

The system ensures voters have information they need to make informed decisions.
