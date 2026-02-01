# PromptShield - Claude Code Build Prompts
## Step-by-Step Implementation Guide

---

## How to Use This Guide

1. Initialize your project directory and place `CLAUDE.md` in the root
2. Run `claude` in your terminal to start Claude Code
3. Execute each prompt in sequence, waiting for completion before moving to the next
4. Review and test after each major phase

---

## Phase 1: Project Initialization

### Prompt 1.1: Create Project Structure

```
Create a new React + TypeScript + Vite project for PromptShield with the following:

1. Initialize with: npm create vite@latest promptshield -- --template react-ts
2. Install dependencies:
   - Tailwind CSS with configuration for dark theme
   - @supabase/supabase-js
   - react-router-dom
   - @tanstack/react-query
   - lucide-react for icons
   - clsx and tailwind-merge for class utilities
   - zod for validation
   - date-fns for date formatting

3. Set up the folder structure as defined in CLAUDE.md
4. Configure Tailwind with the color variables from CLAUDE.md design system
5. Create a basic App.tsx with react-router setup
6. Add the Google Fonts imports for Space Grotesk, Inter, and JetBrains Mono
7. Create index.css with the CSS variables and base dark theme styles

Make sure TypeScript strict mode is enabled and ESLint is configured.
```

### Prompt 1.2: Set Up Supabase

```
Set up Supabase integration:

1. Create src/lib/supabase/client.ts with the Supabase client initialization
2. Create src/types/database.ts with TypeScript types for all tables defined in CLAUDE.md
3. Create src/lib/supabase/auth.ts with helper functions:
   - signUp(email, password)
   - signIn(email, password)
   - signInWithGoogle()
   - signOut()
   - resetPassword(email)
   - getCurrentUser()

4. Create src/context/AuthContext.tsx with:
   - AuthProvider component
   - useAuth hook
   - User state management
   - Session persistence

5. Create supabase/migrations/001_initial_schema.sql with all table definitions from CLAUDE.md
6. Create supabase/migrations/002_rls_policies.sql with all RLS policies

Include proper TypeScript types throughout and error handling.
```

---

## Phase 2: Core Security Scanning Engine

### Prompt 2.1: Implement Security Rules - Prompt Injection

```
Create the prompt injection detection module at src/lib/security/rules/promptInjection.ts:

Define a SecurityRule interface:
interface SecurityRule {
    id: string;
    name: string;
    category: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    pattern: RegExp;
    description: string;
    recommendation: string;
    owaspRef?: string;
    cveRef?: string;
}

Implement these prompt injection detection rules:

CRITICAL severity:
- "ignore (all )?(previous|prior|above) instructions" pattern
- "disregard (all )?(previous|prior|above)" pattern  
- "system:\s*you are" - system override attempts
- "jailbreak" keyword
- "DAN mode" or "DAN:" patterns
- "forget everything" pattern
- "new instructions:" prefix
- "you are now" with role change

HIGH severity:
- "[system]" tag injection
- "act as if you" patterns
- "pretend to be" patterns
- "your new role is" patterns
- "bypass" with "safety|filter|restriction"
- "developer mode" patterns

MEDIUM severity:
- "roleplay as" patterns
- "imagine you are" patterns
- "from now on" with behavior change
- "override" with "settings|behavior|rules"

Also implement POSITIVE checks (things that SHOULD be present):
- Has explicit rejection instructions for override attempts
- Has role anchoring/persistence instruction
- Has instruction to maintain identity
- Handles unicode/encoding edge cases mention

Export a function: checkPromptInjection(prompt: string): SecurityFinding[]

Each finding should include: id, ruleId, category, severity, title, description, evidence (the matched text), recommendation, and references.
```

### Prompt 2.2: Implement Security Rules - Credential Exposure

```
Create src/lib/security/rules/credentialExposure.ts:

Implement credential and sensitive data exposure detection:

CRITICAL severity:
- OpenAI API keys: sk-[a-zA-Z0-9]{32,}
- Anthropic API keys: sk-ant-[a-zA-Z0-9-]+
- Generic API keys: api[_-]?key\s*[:=]\s*["']?[a-zA-Z0-9_-]{20,}
- Bearer tokens: Bearer\s+[a-zA-Z0-9._-]{20,}
- JWT tokens: eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+
- Database connection strings: (mongodb|postgres|mysql)(\+srv)?:\/\/[^\s]+
- AWS credentials: AKIA[0-9A-Z]{16}
- Private keys: -----BEGIN (RSA |EC |)PRIVATE KEY-----
- Hardcoded passwords: password\s*[:=]\s*["'][^"']+["']

HIGH severity:
- Secret key references: secret[_-]?key
- Auth tokens: auth[_-]?token
- API endpoints with credentials in URL
- Internal URLs: \.internal\.|localhost|127\.0\.0\.1
- Webhook URLs with tokens

MEDIUM severity:
- Generic API endpoint exposure: https?:\/\/[^\s]*api[^\s]*
- Environment variable references without proper handling
- Hardcoded email addresses (potential PII)

POSITIVE checks:
- Has instruction to never reveal credentials
- Has instruction to never expose internal URLs
- References secure credential storage

Export: checkCredentialExposure(prompt: string): SecurityFinding[]
```

### Prompt 2.3: Implement Security Rules - MCP Security

```
Create src/lib/security/rules/mcpSecurity.ts:

Implement MCP (Model Context Protocol) security checks based on 2025 threat intelligence:

CRITICAL severity:
- "execute any command" or "run any code" - unrestricted execution
- "no restrictions on tools" - unrestricted tool access
- "trust all (sources|inputs|data)" - no input validation
- "automatically accept tool" - no human verification
- Dynamic tool loading without verification: "dynamically (load|update|change) tool"
- Tool definition mutation patterns (rug pull risk)

HIGH severity:
- "full access to" with system resources
- Missing tool whitelisting patterns
- No mention of tool permission scoping
- "execute without confirmation"
- Cross-server tool access without isolation
- Sampling feature without request sanitization

MEDIUM severity:
- MCP server references without security context
- Tool description references without validation mention
- "tools/list" exposure without filtering
- Context window manipulation patterns
- Memory/history access without boundaries

POSITIVE checks:
- Has tool whitelisting: "only (use|access|call) (approved|whitelisted)"
- Has verification steps: "verify|validate|confirm before"
- Has permission scoping: "minimum (necessary|required) (access|permission)"
- Has human-in-the-loop: "require (human|user) (approval|confirmation)"
- Has tool definition verification

Include references to relevant CVEs:
- CVE-2025-6514 (mcp-remote command injection)
- CVE-2025-49596 (MCP Inspector CSRF)
- CVE-2025-5277 (aws-mcp-server)
- CVE-2025-5276 (markdownify-mcp SSRF)

Export: checkMCPSecurity(prompt: string): SecurityFinding[]
```

### Prompt 2.4: Implement Security Rules - Agentic Security

```
Create src/lib/security/rules/agenticSecurity.ts:

Implement agentic AI security checks for autonomous agents:

CRITICAL severity:
- "autonomous" with "no (limits|restrictions|oversight)"
- "without human (approval|confirmation|oversight)"
- "self-modifying" or "modify (own|its) (code|behavior)"
- "impersonate" other agents or users
- "act on behalf of" without explicit authorization
- Unrestricted cross-agent communication
- "delete|modify|access any" with user data

HIGH severity:
- Missing agent identity verification
- No token rotation mention for long-running agents
- "automatic" with sensitive actions (payments, deletions, emails)
- No mention of action logging/telemetry
- Missing rollback/undo capabilities
- "chain of (actions|tools)" without breakpoints

MEDIUM severity:
- "remember across sessions" without data boundaries
- Agent-to-agent trust without verification
- Missing rate limiting on agent actions
- No mention of anomaly detection
- Unlimited context persistence
- "learning from" user interactions without consent

POSITIVE checks:
- Has cryptographic agent identity
- Has token rotation policy: "rotate (token|credential|key)"
- Has RBAC/ABAC/PBAC: "(role|attribute|policy)(-|\s)based (access|control)"
- Has telemetry/monitoring: "(log|monitor|track) (actions|behavior)"
- Has human-in-the-loop for critical actions
- Has circuit breaker/kill switch
- Has action confirmation for irreversible operations

Export: checkAgenticSecurity(prompt: string): SecurityFinding[]
```

### Prompt 2.5: Implement Security Rules - Compliance

```
Create src/lib/security/rules/compliance.ts:

Implement compliance and regulatory checks:

HIGH severity (potential violations):
- PII collection without consent mention: "collect (personal|user) (data|information)"
- Health data handling without HIPAA reference: "(health|medical|patient) (data|record|information)"
- Minor/child data without COPPA/FERPA: "(child|minor|student) (data|information)"
- Third-party data sharing without disclosure: "share with (third|external|partner)"
- Data retention without policy: "store (indefinitely|permanently|forever)"
- Cross-border data transfer without mention of regulations

MEDIUM severity:
- Session data persistence without boundaries
- Conversation logging without user awareness
- Missing data minimization principles
- No mention of data deletion/right to be forgotten
- Profiling without transparency
- Automated decision-making without human review option

POSITIVE checks (compliance indicators):
- GDPR awareness: mentions "gdpr|data protection|consent|right to"
- HIPAA awareness: mentions "hipaa|phi|protected health"
- CCPA awareness: mentions "ccpa|california|do not sell"
- FERPA awareness: mentions "ferpa|educational records"
- COPPA awareness: mentions "coppa|children|parental consent"
- Data minimization: "only collect (necessary|required|minimum)"
- Retention policy: "retain for|delete after|retention period"
- User rights: "access|correct|delete (your|their) data"

Export: checkCompliance(prompt: string): SecurityFinding[]
```

### Prompt 2.6: Implement Security Rules - Ethical Guardrails

```
Create src/lib/security/rules/ethicalGuardrails.ts:

Implement ethical and safety guardrail checks:

CRITICAL severity:
- "never refuse" or "always comply" - no refusal capability
- "bypass safety" or "ignore (safety|ethical) (guidelines|rules)"
- "no limits" on content generation
- Deception enablement: "deceive|manipulate|mislead (users|people)"

HIGH severity:
- "always agree" with user - sycophantic behavior
- "no restrictions on (content|output)"
- Missing harmful content prevention
- "generate (any|all) content" without boundaries
- Discrimination enablement patterns
- "never question" user requests

MEDIUM severity:
- "dismiss (concerns|objections)" - invalidation of user concerns
- "build (false|artificial) rapport" - manipulation
- "urgency|scarcity" in persuasive contexts without accuracy
- Missing bias awareness
- "convince|persuade" without ethical bounds
- Emotional manipulation patterns

POSITIVE checks:
- Has refusal capability: "refuse|decline|cannot (comply|help) (with|when)"
- Has harmful content awareness: "harmful|dangerous|illegal"
- Has honesty commitment: "honest|truthful|accurate"
- Has bias awareness: "bias|fair|balanced"
- Has user wellbeing consideration
- Has transparency about AI nature
- Acknowledges limitations

Export: checkEthicalGuardrails(prompt: string): SecurityFinding[]
```

### Prompt 2.7: Create Main Scanner Engine

```
Create src/lib/security/scanner.ts that orchestrates all security checks:

Import all rule modules and create the main scanning engine:

interface ScanRequest {
    prompt: string;
    scanType: 'quick' | 'deep' | 'enterprise';
    customRules?: SecurityRule[];
}

interface ScanResult {
    id: string;
    securityScore: number;
    summary: {
        critical: number;
        high: number;
        medium: number;
        low: number;
        passed: number;
    };
    findings: SecurityFinding[];
    recommendations: Recommendation[];
    metadata: {
        scanType: string;
        promptLength: number;
        rulesChecked: number;
        scanDurationMs: number;
        timestamp: string;
    };
}

Implement:
1. scanPrompt(request: ScanRequest): Promise<ScanResult>
   - Run all rule checks based on scan type
   - Quick: promptInjection, credentialExposure, ethicalGuardrails
   - Deep: All quick + mcpSecurity, agenticSecurity, compliance
   - Enterprise: All deep + customRules
   - Deduplicate findings
   - Calculate security score using SEVERITY_SCORES from CLAUDE.md
   - Generate prioritized recommendations
   - Return complete ScanResult

2. calculateSecurityScore(findings: SecurityFinding[]): number
   - Start at 100
   - Apply severity deductions
   - Apply passed check bonuses (max +20)
   - Floor at 0, cap at 100

3. generateRecommendations(findings: SecurityFinding[]): Recommendation[]
   - Group findings by category
   - Prioritize by severity
   - Generate actionable recommendations
   - Include code examples where applicable

4. hashPrompt(prompt: string): string
   - SHA-256 hash for duplicate detection
   - Don't store actual prompt content for privacy

Export the scanner as a singleton with proper error handling.
```

---

## Phase 3: Threat Intelligence System

### Prompt 3.1: Create Threat Intelligence Service

```
Create src/lib/security/threatIntel.ts:

Implement the threat intelligence service:

interface ThreatIndicator {
    id: string;
    source: 'OWASP' | 'CVE' | 'CISA' | 'Community' | 'Internal';
    sourceId?: string;
    threatType: string;
    title: string;
    description: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    indicators: {
        patterns: string[];
        keywords: string[];
        signatures: string[];
    };
    affectedSystems: string[];
    mitigation: string;
    references: { url: string; title: string }[];
    publishedAt: Date;
    isActive: boolean;
}

Implement:

1. ThreatIntelService class with:
   - fetchLatestThreats(filters?: ThreatFilters): Promise<ThreatIndicator[]>
   - getThreatById(id: string): Promise<ThreatIndicator>
   - checkPromptAgainstThreats(prompt: string, threats: ThreatIndicator[]): AffectedThreat[]
   - subscribeToThreatUpdates(callback: (threat: ThreatIndicator) => void): Unsubscribe

2. Integration with Supabase for storage and real-time updates

3. Seed data function to populate initial threat intel:
   - All OWASP LLM Top 10 (2025) vulnerabilities
   - Recent MCP CVEs (CVE-2025-6514, CVE-2025-49596, CVE-2025-59944, CVE-2025-5277, CVE-2025-5276, CVE-2025-5273)
   - Agentic AI risks from OWASP Agentic Top 10 draft

4. Caching layer with 5-minute TTL for performance

5. Method to convert threat indicators to scanner rules:
   threatToSecurityRule(threat: ThreatIndicator): SecurityRule

This enables the "Living Intelligence" system where new threats automatically become scanner rules.
```

### Prompt 3.2: Create Threat Feed UI Components

```
Create the threat intelligence feed UI components:

1. src/components/threats/ThreatFeed.tsx:
   - Displays list of threat cards
   - Filter controls: source, severity, date range, "affects my scans" toggle
   - Search functionality
   - Real-time updates indicator
   - Pagination or infinite scroll

2. src/components/threats/ThreatCard.tsx:
   - Compact card showing: source badge, severity indicator, title, date
   - "Affects Your Scans" badge when threat matches user's past findings
   - Expandable to show full description, mitigation, references
   - "Subscribe to alerts" action

3. src/components/threats/ThreatDetail.tsx:
   - Full threat details view
   - Related CVEs and references
   - Affected systems list
   - Mitigation steps with code examples
   - Link to rescan prompts with new threat detection

4. src/components/threats/ThreatFilters.tsx:
   - Multi-select for sources
   - Multi-select for severities
   - Date range picker
   - "Show only threats affecting my scans" toggle
   - Search input with debounce

5. src/hooks/useThreats.ts:
   - useThreats(filters) - fetch threats with react-query
   - useRealTimeThreats() - subscribe to real-time updates
   - useAffectedThreats(userId) - threats matching user's scan history

Style with dark theme, cyan accents, subtle animations for new threats.
```

---

## Phase 4: User Interface

### Prompt 4.1: Create Layout Components

```
Create the application layout components:

1. src/components/layout/AppLayout.tsx:
   - Main layout wrapper with sidebar and content area
   - Responsive: sidebar collapses to bottom nav on mobile
   - Dark theme with gradient background
   - Grid pattern overlay (subtle)

2. src/components/layout/Sidebar.tsx:
   - Logo and branding
   - Navigation links with icons (lucide-react):
     - Dashboard
     - Scanner
     - Threat Feed
     - Checklist
     - Settings
     - Team (if Team+ tier)
     - Admin (if admin)
   - User profile section at bottom
   - Upgrade prompt for free users
   - Collapse toggle

3. src/components/layout/Header.tsx:
   - Page title
   - Breadcrumbs
   - Quick actions (new scan, export)
   - Notifications bell
   - User menu dropdown

4. src/components/layout/MobileNav.tsx:
   - Bottom navigation for mobile
   - 5 main icons: Dashboard, Scanner, Threats, Checklist, Profile
   - Active state indicator

5. src/components/layout/Footer.tsx:
   - Copyright
   - Links: Privacy, Terms, Docs, Status
   - Social links

Use Tailwind CSS with the design system from CLAUDE.md. Add smooth transitions and hover states.
```

### Prompt 4.2: Create Dashboard Page

```
Create the main dashboard at src/pages/Dashboard.tsx:

Components needed:

1. src/components/dashboard/ScoreOverview.tsx:
   - Large security score ring (animated)
   - Score trend indicator (up/down from last scan)
   - "Run New Scan" CTA button

2. src/components/dashboard/StatsGrid.tsx:
   - 4 stat cards in a grid:
     - Scans this month (with limit for free: "3/3")
     - Average security score
     - Critical issues found (total across scans)
     - Active threats

3. src/components/dashboard/RecentScans.tsx:
   - List of last 5 scans
   - Each showing: date, score badge, finding count, star toggle
   - "View All" link
   - Empty state for new users

4. src/components/dashboard/ThreatHighlights.tsx:
   - Top 3 critical/high threats from feed
   - "Affects your scans" indicator
   - "View All Threats" link

5. src/components/dashboard/QuickActions.tsx:
   - New Scan button (primary)
   - Run Checklist button (secondary)
   - Export Last Report button (pro+)

6. src/components/dashboard/UsageIndicator.tsx (for free users):
   - Progress bar showing scans used
   - Upgrade prompt when near limit

Fetch data using react-query hooks. Show loading skeletons during fetch.
```

### Prompt 4.3: Create Security Scanner Page

```
Create the main scanner interface at src/pages/Scanner.tsx:

Components:

1. src/components/scanner/PromptInput.tsx:
   - Large textarea with monospace font (JetBrains Mono)
   - Line numbers on the left
   - Character count
   - Clear button
   - Paste button
   - Sample prompt dropdown (for demo)
   - Placeholder text with example

2. src/components/scanner/ScanTypeSelector.tsx:
   - Radio/toggle group for scan type:
     - Quick (icon: zap) - "Fast check for critical issues"
     - Deep (icon: search) - "Comprehensive security analysis"
     - Enterprise (icon: shield) - "Full audit with custom rules" (enterprise only)
   - Lock icons on unavailable options with upgrade tooltip

3. src/components/scanner/ScanButton.tsx:
   - Large primary button
   - Loading state with progress animation
   - Disabled state when no input or limit reached
   - Keyboard shortcut hint (Cmd+Enter)

4. src/components/scanner/ScanProgress.tsx:
   - Animated progress steps during scan:
     1. "Analyzing for injection vulnerabilities"
     2. "Checking credential exposure"
     3. "Evaluating compliance requirements"
     4. "Generating recommendations"
   - Each step shows checkmark when complete

5. src/hooks/useScan.ts:
   - useScan() hook that handles:
     - Mutation to run scan
     - Loading state
     - Error handling
     - Redirect to results on completion

The scanner should feel responsive and professional. Add subtle animations.
```

### Prompt 4.4: Create Results Page

```
Create the scan results view at src/pages/Results.tsx:

URL: /results/:scanId

Components:

1. src/components/scanner/ScoreRing.tsx:
   - Animated SVG ring showing security score
   - Color coded: <40 red, 40-60 amber, 60-80 green, 80+ cyan
   - Score number in center with label
   - Animation on mount

2. src/components/scanner/ResultsSummary.tsx:
   - 4 stat boxes: Critical, High, Medium, Passed counts
   - Each with appropriate color
   - Overall assessment text based on score

3. src/components/scanner/FindingsList.tsx:
   - Grouped by category or sorted by severity (toggle)
   - Virtualized list for performance

4. src/components/scanner/FindingCard.tsx:
   - Severity badge with color
   - Title and description
   - Evidence section (the matched text, truncated)
   - Expandable recommendation section
   - References (OWASP, CVE) as links
   - Copy button for recommendation

5. src/components/scanner/ResultsTabs.tsx:
   - Tabs: Overview | Findings | Recommendations | Checklist
   - Smooth transitions between tabs

6. src/components/scanner/ExportOptions.tsx:
   - Export as PDF button (pro+)
   - Copy to clipboard button
   - Share link button
   - Download JSON button

7. src/components/scanner/RescanButton.tsx:
   - "Rescan" button to run again
   - "Edit & Rescan" to go back with prompt pre-filled

8. src/hooks/useScanResult.ts:
   - Fetch scan result by ID
   - Handle not found / unauthorized

Include loading skeleton and error states.
```

### Prompt 4.5: Create Interactive Checklist

```
Create the security checklist at src/pages/Checklist.tsx:

Define 18 questions organized by category in src/lib/security/checklistQuestions.ts:

interface ChecklistQuestion {
    id: string;
    category: string;
    question: string;
    impact: 'critical' | 'high' | 'medium';
    guidance: string;
    resources?: { title: string; url: string }[];
}

Categories and questions:
- Prompt Injection Defense (3 questions)
- Data Protection (3 questions)
- Compliance (3 questions)
- Ethical Guardrails (3 questions)
- Tool & API Security (3 questions)
- Output Safety (3 questions)

(Use the questions from the Lovable prompt I created earlier)

Components:

1. src/components/checklist/ChecklistStepper.tsx:
   - Progress indicator showing current category
   - Animated transitions between categories

2. src/components/checklist/QuestionCard.tsx:
   - Question number badge
   - Question text
   - Impact indicator
   - Three response buttons: Yes (green), Partial (amber), No (red)
   - Optional notes field (expandable)
   - Guidance tooltip

3. src/components/checklist/ChecklistResults.tsx:
   - Compliance score calculation
   - Gap analysis by category
   - Specific recommendations for No/Partial answers
   - Option to link to a scan

4. src/components/checklist/ChecklistExport.tsx:
   - Export as PDF checklist report
   - Include responses, gaps, recommendations

5. src/hooks/useChecklist.ts:
   - State management for responses
   - Calculate compliance score
   - Save to database
   - Load previous responses

Make it feel like a guided assessment, not just a form.
```

---

## Phase 5: Authentication & Subscriptions

### Prompt 5.1: Create Auth Pages

```
Create authentication pages:

1. src/pages/auth/Login.tsx:
   - Email/password form
   - "Continue with Google" button
   - Magic link option
   - "Forgot password" link
   - "Don't have an account? Sign up" link
   - Error handling with toast notifications

2. src/pages/auth/Signup.tsx:
   - Email, password, confirm password
   - Full name (optional)
   - Company (optional)
   - Terms acceptance checkbox
   - "Continue with Google" button
   - "Already have an account? Log in" link

3. src/pages/auth/ForgotPassword.tsx:
   - Email input
   - Submit button
   - Success message with instructions
   - Back to login link

4. src/pages/auth/ResetPassword.tsx:
   - New password input
   - Confirm password input
   - Submit button
   - Redirect to login on success

5. src/pages/auth/VerifyEmail.tsx:
   - Loading state while verifying
   - Success message
   - Error handling
   - Resend verification link

6. src/components/auth/AuthGuard.tsx:
   - Wrapper component that redirects to login if not authenticated
   - Loading state while checking auth

7. src/components/auth/RoleGuard.tsx:
   - Wrapper that checks user role
   - Shows upgrade prompt or redirects if role insufficient

Style these with a centered card layout, subtle gradient background, logo at top.
```

### Prompt 5.2: Implement Stripe Integration

```
Set up Stripe subscription management:

1. src/lib/stripe/client.ts:
   - Initialize Stripe.js with publishable key
   - Create checkout session function
   - Create customer portal session function

2. src/lib/stripe/subscriptions.ts:
   - getSubscriptionStatus(userId)
   - createCheckoutSession(userId, priceId)
   - createPortalSession(userId)
   - handleWebhook(event)

3. supabase/functions/create-checkout-session/index.ts:
   Edge function that:
   - Validates user auth
   - Creates or retrieves Stripe customer
   - Creates checkout session for selected price
   - Returns session URL

4. supabase/functions/create-portal-session/index.ts:
   Edge function that:
   - Validates user auth
   - Creates billing portal session
   - Returns portal URL

5. supabase/functions/stripe-webhook/index.ts:
   Edge function that handles:
   - checkout.session.completed → update user role
   - customer.subscription.updated → update subscription status
   - customer.subscription.deleted → downgrade to free
   - invoice.payment_failed → send notification

6. src/components/subscription/PricingCards.tsx:
   - Display all 4 tiers
   - Current plan indicator
   - Feature comparison
   - CTA buttons

7. src/components/subscription/UpgradePrompt.tsx:
   - Shown when user hits limits
   - Highlights benefits of upgrading
   - Quick upgrade button

8. src/hooks/useSubscription.ts:
   - Get current subscription status
   - Check feature access
   - Trigger checkout flow

9. src/context/SubscriptionContext.tsx:
   - Provide subscription state app-wide
   - Refresh on subscription changes

Create Stripe products and prices for:
- Pro: $19/month (price_pro_monthly)
- Team: $49/month (price_team_monthly)
- Enterprise: Custom (manual)
```

---

## Phase 6: API & Enterprise Features

### Prompt 6.1: Implement API Endpoints

```
Create the public API for Pro/Enterprise users:

1. supabase/functions/api-v1-scan/index.ts:
   POST /api/v1/scan
   - Validate API key from Authorization header
   - Check rate limits
   - Run security scan
   - Log API usage
   - Return scan results
   
   Request: { prompt: string, scan_type: 'quick' | 'deep' }
   Response: { scan_id, security_score, summary, findings, recommendations }

2. supabase/functions/api-v1-scan-get/index.ts:
   GET /api/v1/scan/:id
   - Validate API key
   - Check ownership
   - Return full scan details

3. supabase/functions/api-v1-threats/index.ts:
   GET /api/v1/threats
   - Validate API key
   - Apply filters from query params
   - Return paginated threats

4. supabase/functions/api-v1-checklist/index.ts:
   POST /api/v1/checklist
   - Validate API key
   - Calculate compliance score
   - Return gaps and recommendations

5. src/lib/api/rateLimit.ts:
   - Check and update API call count
   - Return 429 with retry-after when exceeded
   - Different limits by tier: Pro=100, Team=500, Enterprise=unlimited

6. src/pages/ApiDocs.tsx:
   - Interactive API documentation
   - Code examples in JavaScript and Python
   - "Try It" feature using user's API key
   - Rate limit information

7. src/components/settings/ApiKeyManager.tsx:
   - Generate API key (prefixed: ps_live_)
   - Display with masked characters
   - Copy button
   - Regenerate with confirmation
   - Usage stats: calls this month / limit
   - Last used timestamp
```

### Prompt 6.2: Implement Team Management

```
Create team management for Team and Enterprise tiers:

1. src/pages/Team.tsx:
   - Team dashboard
   - Member list with roles
   - Invite form
   - Team settings

2. src/components/team/TeamMemberList.tsx:
   - List all team members
   - Show: name, email, role, joined date
   - Actions: change role, remove member
   - Current user indicator

3. src/components/team/InviteMember.tsx:
   - Email input
   - Role selector (admin, member, viewer)
   - Send invite button
   - Pending invites list

4. src/components/team/TeamSettings.tsx:
   - Team name
   - Default scan settings
   - Notification preferences
   - Transfer ownership

5. src/components/team/TeamScans.tsx:
   - View all team members' scans
   - Filter by member
   - Aggregate statistics

6. supabase/functions/team-invite/index.ts:
   - Validate inviter is team admin
   - Create invite record
   - Send invite email via Resend

7. src/pages/TeamInvite.tsx:
   - Accept invite page
   - Join team flow
   - Create account if needed

8. src/hooks/useTeam.ts:
   - Get team data
   - Invite member
   - Remove member
   - Update member role
   - Check team permissions

Role permissions:
- Admin: full access, can invite/remove, change settings
- Member: scan, view team scans, checklist
- Viewer: view only, no scanning
```

### Prompt 6.3: Implement Enterprise Features

```
Add enterprise-specific features:

1. src/components/enterprise/CustomRulesManager.tsx:
   - List custom security rules
   - Add new rule form:
     - Name, description
     - Category dropdown
     - Severity selector
     - Regex pattern input with test area
     - Recommendation text
   - Edit/delete existing rules
   - Toggle rules on/off
   - Import/export as JSON

2. src/components/enterprise/AuditLog.tsx:
   - Filterable log viewer
   - Columns: timestamp, user, action, resource, details
   - Export as CSV
   - Date range filter
   - User filter
   - Action type filter

3. src/components/enterprise/SSOConfig.tsx:
   - Enable/disable SSO
   - Identity provider selector (SAML, OIDC)
   - Configuration fields:
     - IdP URL
     - Client ID
     - Client Secret
     - Callback URL
   - Test connection button
   - Enforce SSO toggle

4. src/components/enterprise/WhiteLabel.tsx:
   - Logo upload
   - Primary color picker
   - Email template customization
   - PDF report branding

5. src/components/enterprise/UsageAnalytics.tsx:
   - Scans by team member (bar chart)
   - Security score trends (line chart)
   - Common vulnerabilities (pie chart)
   - Export compliance report

6. supabase/functions/audit-log/index.ts:
   - Log audit events
   - Query with filters
   - Export functionality

Use recharts for visualizations. Gate all features behind enterprise role check.
```

---

## Phase 7: Subagent Setup for Security Review

### Prompt 7.1: Create Security Review Subagent

```
Create a specialized security review subagent configuration for use with Claude Code:

Create .claude/agents/security-reviewer.md:

---
name: Security Reviewer
description: Specialized subagent for reviewing AI prompts and configurations for security vulnerabilities following OWASP Top 10 for LLMs 2025
---

# Security Reviewer Agent

You are a specialized security reviewer focused on AI application security. Your expertise covers:

## Core Competencies
- OWASP Top 10 for LLM Applications (2025)
- OWASP Top 10 for Agentic AI (2026 draft)
- MCP (Model Context Protocol) security vulnerabilities
- Prompt injection attack vectors (direct, indirect, jailbreaks)
- Credential and sensitive data exposure
- Compliance requirements (GDPR, HIPAA, FERPA, COPPA, CCPA)

## Review Process

When reviewing a prompt or configuration:

1. **Initial Assessment**
   - Identify the type of AI application (chatbot, agent, RAG, etc.)
   - Note the intended use case and user base
   - Identify any mentioned tools, APIs, or integrations

2. **Vulnerability Scan**
   - Check for prompt injection vulnerabilities
   - Identify credential or secret exposure
   - Evaluate MCP/tool security if applicable
   - Assess agentic security for autonomous systems
   - Review compliance implications
   - Check ethical guardrails

3. **Severity Classification**
   - CRITICAL: Immediate exploitation risk, data breach potential
   - HIGH: Significant security weakness, requires attention
   - MEDIUM: Potential risk under certain conditions
   - LOW: Minor concern, best practice recommendation

4. **Recommendations**
   - Provide specific, actionable remediation steps
   - Include code examples where helpful
   - Reference relevant standards (OWASP, CVE, etc.)

## Output Format

Always structure your review as:

```
## Security Review Summary
- **Overall Risk Level**: [Critical/High/Medium/Low]
- **Key Findings**: [Count by severity]
- **Immediate Actions Required**: [Yes/No]

## Detailed Findings

### [SEVERITY] - [Finding Title]
**Category**: [OWASP LLM category or custom]
**Description**: [What was found]
**Evidence**: [The specific text/pattern]
**Impact**: [Potential consequences]
**Recommendation**: [How to fix]
**References**: [OWASP, CVE, or other standards]

## Positive Security Indicators
[List any good security practices detected]

## Recommended Prompt Additions
[Specific text to add to improve security]
```

## Important Guidelines

- Never suggest removing functionality, only securing it
- Provide balanced assessment - acknowledge what's done well
- Consider the trade-off between security and usability
- Recommend defense-in-depth approaches
- Stay current with emerging threats (MCP, agentic, etc.)


Now create a command to invoke this agent:

Create .claude/commands/security-review.md:

---
name: security-review
description: Run a comprehensive security review on an AI prompt or configuration
arguments:
  - name: target
    description: The file path or text to review
    required: true
---

Run a comprehensive security review using the Security Reviewer agent.

$ARGUMENTS.target

Provide:
1. Overall risk assessment
2. Detailed findings by severity
3. Specific remediation recommendations
4. Suggested prompt additions for better security
```

### Prompt 7.2: Create Compliance Review Subagent

```
Create a compliance-focused subagent:

Create .claude/agents/compliance-reviewer.md:

---
name: Compliance Reviewer
description: Specialized subagent for reviewing AI applications for regulatory compliance (GDPR, HIPAA, FERPA, COPPA, CCPA)
---

# Compliance Reviewer Agent

You are a compliance specialist focused on AI application regulatory requirements.

## Expertise Areas

### GDPR (General Data Protection Regulation)
- Lawful basis for processing
- Data subject rights (access, rectification, erasure, portability)
- Privacy by design
- Data minimization
- Cross-border transfer rules

### HIPAA (Health Insurance Portability and Accountability Act)
- Protected Health Information (PHI) handling
- Minimum necessary standard
- Business Associate Agreements
- Security Rule requirements

### FERPA (Family Educational Rights and Privacy Act)
- Educational records protection
- Parental consent requirements
- Directory information rules

### COPPA (Children's Online Privacy Protection Act)
- Verifiable parental consent
- Data collection limitations for under-13
- Privacy policy requirements

### CCPA/CPRA (California Consumer Privacy Act)
- Right to know, delete, opt-out
- "Do Not Sell" requirements
- Service provider obligations

## Review Process

1. **Data Flow Analysis**
   - What data is collected?
   - How is it processed?
   - Where is it stored?
   - Who has access?
   - Is it shared with third parties?

2. **Regulation Applicability**
   - Which regulations apply based on:
     - User location
     - Data types
     - Industry sector
     - User demographics (minors)

3. **Gap Assessment**
   - Missing disclosures
   - Inadequate consent mechanisms
   - Data retention issues
   - Access control gaps
   - Missing user rights implementations

4. **Recommendations**
   - Specific language to add
   - Process changes needed
   - Technical controls required

## Output Format

```
## Compliance Review Summary
- **Applicable Regulations**: [List]
- **Compliance Status**: [Compliant/Gaps Identified/Non-Compliant]
- **Critical Gaps**: [Count]

## Regulation-by-Regulation Assessment

### [REGULATION]
**Applicability**: [Why this applies]
**Status**: [Compliant/Gap/Non-Compliant]
**Findings**:
- [Specific findings]
**Required Actions**:
- [Specific remediation steps]

## Recommended Prompt Additions
[Specific compliance-related text to add]

## Documentation Requirements
[What policies/procedures need to be in place]
```


Create command:

.claude/commands/compliance-review.md:

---
name: compliance-review
description: Review an AI application for regulatory compliance
arguments:
  - name: target
    description: The file path or text to review
    required: true
  - name: regulations
    description: Specific regulations to check (comma-separated, or "all")
    required: false
    default: "all"
---

Run a compliance review using the Compliance Reviewer agent.

Target: $ARGUMENTS.target
Regulations: $ARGUMENTS.regulations

Provide regulation-by-regulation assessment with specific remediation steps.
```

### Prompt 7.3: Create Threat Intelligence Subagent

```
Create a threat intelligence subagent:

Create .claude/agents/threat-intel.md:

---
name: Threat Intelligence Analyst
description: Specialized subagent for analyzing prompts against current AI security threat intelligence
---

# Threat Intelligence Analyst Agent

You are a threat intelligence analyst specializing in AI/LLM security threats.

## Intelligence Sources

Maintain awareness of:
- OWASP GenAI Security Project updates
- CVE database for AI-related vulnerabilities
- CISA advisories
- MITRE ATLAS (Adversarial Threat Landscape for AI Systems)
- MCP Security advisories
- Academic research on LLM attacks
- Industry incident reports

## Current Threat Landscape (2025)

### Active Threat Categories

1. **MCP Server Attacks**
   - Tool poisoning / rug pulls
   - Line jumping attacks
   - Sampling exploitation
   - Recent CVEs: CVE-2025-6514, CVE-2025-49596, CVE-2025-5277

2. **Agentic AI Attacks**
   - Agent impersonation
   - Cross-agent prompt injection
   - Autonomous action hijacking
   - Memory poisoning

3. **Supply Chain Attacks**
   - Package hallucination (npm, PyPI typosquatting)
   - Model poisoning
   - Adapter/LoRA backdoors

4. **Advanced Prompt Injection**
   - Indirect injection via documents
   - Multi-step jailbreaks
   - Context overflow attacks
   - Unicode/encoding exploits

5. **Data Exfiltration**
   - Prompt extraction attacks
   - Training data extraction
   - PII harvesting

## Analysis Process

1. **Threat Mapping**
   - Map prompt/config to potential attack vectors
   - Identify exposed attack surfaces
   - Assess threat actor motivation

2. **Indicator Matching**
   - Check for known vulnerability patterns
   - Match against current CVE indicators
   - Identify emerging threat signatures

3. **Risk Assessment**
   - Likelihood of exploitation
   - Potential impact
   - Current threat actor activity level

4. **Intelligence Brief**
   - Relevant threats to this specific use case
   - Recommended mitigations
   - Monitoring recommendations

## Output Format

```
## Threat Intelligence Brief

### Target Profile
- **Application Type**: [chatbot/agent/RAG/etc.]
- **Attack Surface**: [identified vectors]
- **Threat Actor Interest**: [Low/Medium/High]

### Relevant Active Threats

#### [Threat Name]
- **Source**: [OWASP/CVE/CISA/etc.]
- **Reference**: [ID]
- **Relevance**: [Why this applies]
- **Indicators Present**: [What we detected]
- **Mitigation**: [Specific steps]

### Emerging Threats to Monitor
[New threats that may become relevant]

### Recommended Monitoring
[What to watch for post-deployment]

### Intelligence Confidence
[Assessment of analysis confidence]
```


Create command:

.claude/commands/threat-analysis.md:

---
name: threat-analysis
description: Analyze a prompt against current AI security threat intelligence
arguments:
  - name: target
    description: The file path or text to analyze
    required: true
---

Run threat intelligence analysis using the Threat Intelligence Analyst agent.

$ARGUMENTS.target

Provide threat mapping, indicator matching, and actionable intelligence brief.
```

---

## Phase 8: Testing & Deployment

### Prompt 8.1: Create Test Suite

```
Set up comprehensive testing:

1. Create src/lib/security/__tests__/scanner.test.ts:
   - Test each rule category
   - Test score calculation
   - Test recommendation generation
   - Use the test prompts from the PromptShield-Test-Prompts.md file

2. Create src/lib/security/__tests__/rules/*.test.ts:
   - Individual tests for each rule file
   - Test pattern matching accuracy
   - Test false positive/negative cases
   - Test edge cases (unicode, long prompts, etc.)

3. Create src/components/__tests__/:
   - Component unit tests with React Testing Library
   - Test user interactions
   - Test loading/error states

4. Create e2e/scanner.spec.ts (Playwright):
   - Full scan flow: input → scan → results
   - Test subscription gating
   - Test export functionality

5. Create e2e/auth.spec.ts:
   - Sign up flow
   - Login flow
   - Password reset flow

6. Create supabase/tests/:
   - RLS policy tests
   - Edge function tests

7. Configure CI/CD in .github/workflows/test.yml:
   - Run tests on PR
   - Run tests before deploy
   - Coverage reporting

Add test data fixtures with known vulnerabilities for validation.
```

### Prompt 8.2: Deploy to Production

```
Set up production deployment:

1. Create vercel.json:
   - Configure build settings
   - Set up redirects
   - Configure headers (security, caching)

2. Configure environment variables in Vercel:
   - All VITE_ prefixed vars
   - No server-side secrets in frontend

3. Set up Supabase production:
   - Create production project
   - Run migrations: npx supabase db push
   - Configure auth providers (Google OAuth)
   - Set up RLS policies
   - Configure edge function secrets

4. Configure Stripe:
   - Create products and prices in Stripe dashboard
   - Set up webhook endpoint
   - Configure customer portal

5. Set up custom domain:
   - Add domain in Vercel
   - Configure DNS
   - SSL auto-provisioned

6. Configure monitoring:
   - Set up Sentry for error tracking
   - Configure PostHog for analytics
   - Set up uptime monitoring

7. Create deployment checklist script that verifies:
   - All env vars set
   - Database migrations applied
   - RLS policies enabled
   - Stripe webhook configured
   - Domain SSL valid

8. Set up backup:
   - Supabase automatic backups
   - Configure retention policy

Document the deployment process in DEPLOYMENT.md.
```

---

## Quick Reference: Claude Code Commands

```bash
# Start Claude Code in project directory
claude

# Run security review on a file
/security-review src/prompts/customer-service.txt

# Run compliance review
/compliance-review src/prompts/health-advisor.txt --regulations "HIPAA,GDPR"

# Run threat analysis
/threat-analysis src/prompts/autonomous-agent.txt

# General development
"Set up the project structure"
"Implement the prompt injection detection rules"
"Create the dashboard page with stats widgets"
"Add Stripe subscription flow"
"Write tests for the scanner"
"Deploy to Vercel"
```

---

## Summary: Build Order

1. **Phase 1**: Project initialization, Supabase setup
2. **Phase 2**: Security scanning engine (all rule modules)
3. **Phase 3**: Threat intelligence system
4. **Phase 4**: User interface (layout, dashboard, scanner, results)
5. **Phase 5**: Auth and subscriptions
6. **Phase 6**: API and enterprise features
7. **Phase 7**: Subagent configuration
8. **Phase 8**: Testing and deployment

Estimated time with Claude Code: **1-2 weeks** for full production build.

---

**You're building the security standard for AI applications. The architecture supports that mission.**
