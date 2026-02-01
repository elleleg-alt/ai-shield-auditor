# CLAUDE.md - PromptShield AI Security Validation Platform

## Project Overview

PromptShield is a comprehensive AI security validation platform that helps AI consultants and enterprise teams validate their custom GPT prompts, AI agent configurations, and LLM workflows for security vulnerabilities before deployment.

**Mission:** Become the industry standard for AI application security validation.

**Target Users:**
- Solo AI consultants building custom GPTs
- Enterprise teams deploying AI agents
- Security professionals reviewing AI implementations
- Developers building LLM-powered applications

---

## Tech Stack

```
Frontend:       React 18 + TypeScript + Vite
Styling:        Tailwind CSS (dark theme primary)
Backend:        Supabase (PostgreSQL + Auth + Storage + Edge Functions)
Payments:       Stripe (subscriptions + usage-based billing)
Deployment:     Vercel (frontend) + Supabase (backend)
Analytics:      PostHog or Mixpanel
Email:          Resend
PDF Generation: @react-pdf/renderer
```

---

## Project Structure

```
promptshield/
├── src/
│   ├── components/
│   │   ├── ui/                    # Reusable UI components (shadcn/ui style)
│   │   ├── scanner/               # Security scanner components
│   │   ├── dashboard/             # Dashboard widgets
│   │   ├── threats/               # Threat intelligence components
│   │   ├── checklist/             # Security checklist components
│   │   └── layout/                # Layout components (nav, sidebar, footer)
│   ├── pages/
│   │   ├── Landing.tsx            # Marketing landing page
│   │   ├── Dashboard.tsx          # User dashboard
│   │   ├── Scanner.tsx            # Main security scanner
│   │   ├── Results.tsx            # Scan results view
│   │   ├── ThreatFeed.tsx         # Threat intelligence feed
│   │   ├── Checklist.tsx          # Interactive security checklist
│   │   ├── Settings.tsx           # User settings
│   │   ├── Team.tsx               # Team management (Team+ tiers)
│   │   ├── Admin.tsx              # Admin panel
│   │   └── ApiDocs.tsx            # API documentation
│   ├── lib/
│   │   ├── security/
│   │   │   ├── scanner.ts         # Core scanning engine
│   │   │   ├── rules/
│   │   │   │   ├── promptInjection.ts
│   │   │   │   ├── credentialExposure.ts
│   │   │   │   ├── compliance.ts
│   │   │   │   ├── mcpSecurity.ts
│   │   │   │   ├── agenticSecurity.ts
│   │   │   │   └── ethicalGuardrails.ts
│   │   │   ├── threatIntel.ts     # Threat intelligence service
│   │   │   └── scoring.ts         # Security score calculation
│   │   ├── supabase/
│   │   │   ├── client.ts          # Supabase client
│   │   │   ├── auth.ts            # Auth helpers
│   │   │   └── queries.ts         # Database queries
│   │   ├── stripe/
│   │   │   ├── client.ts          # Stripe client
│   │   │   └── subscriptions.ts   # Subscription management
│   │   └── utils/
│   │       ├── formatters.ts      # Data formatters
│   │       └── validators.ts      # Input validators
│   ├── hooks/
│   │   ├── useAuth.ts             # Authentication hook
│   │   ├── useScan.ts             # Scanning hook
│   │   ├── useThreats.ts          # Threat feed hook
│   │   └── useSubscription.ts     # Subscription status hook
│   ├── types/
│   │   ├── security.ts            # Security-related types
│   │   ├── database.ts            # Database types (generated)
│   │   └── api.ts                 # API types
│   ├── context/
│   │   ├── AuthContext.tsx        # Auth context provider
│   │   └── SubscriptionContext.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── supabase/
│   ├── migrations/                # Database migrations
│   ├── functions/                 # Edge functions
│   │   ├── scan/                  # Scan API endpoint
│   │   ├── threats/               # Threat feed endpoint
│   │   └── webhooks/              # Stripe webhooks
│   └── seed.sql                   # Initial seed data
├── public/
├── CLAUDE.md                      # This file
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── .env.example
```

---

## Database Schema (Supabase)

### Core Tables

```sql
-- Users (extends Supabase auth.users)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT NOT NULL,
    full_name TEXT,
    company TEXT,
    role TEXT DEFAULT 'free' CHECK (role IN ('free', 'pro', 'team', 'enterprise', 'admin')),
    scans_this_month INTEGER DEFAULT 0,
    scans_reset_at TIMESTAMP WITH TIME ZONE,
    api_key TEXT UNIQUE,
    api_calls_this_month INTEGER DEFAULT 0,
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scans
CREATE TABLE public.scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    prompt_content TEXT NOT NULL,
    prompt_hash TEXT, -- For duplicate detection
    scan_type TEXT DEFAULT 'quick' CHECK (scan_type IN ('quick', 'deep', 'enterprise')),
    security_score INTEGER CHECK (security_score >= 0 AND security_score <= 100),
    summary JSONB, -- {critical: 0, high: 0, medium: 0, low: 0, passed: 0}
    findings JSONB, -- Array of finding objects
    recommendations JSONB, -- Array of recommendation objects
    metadata JSONB, -- Additional scan metadata
    is_starred BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Findings (denormalized for querying)
CREATE TABLE public.findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES public.scans(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low', 'passed')),
    rule_id TEXT, -- Reference to the rule that triggered this
    title TEXT NOT NULL,
    description TEXT,
    evidence TEXT, -- The matched pattern or text
    recommendation TEXT,
    cve_reference TEXT,
    owasp_reference TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Threat Intelligence
CREATE TABLE public.threat_intel (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL, -- OWASP, CVE, CISA, Community, Internal
    source_id TEXT, -- External reference ID (CVE-2025-XXXX, etc.)
    threat_type TEXT NOT NULL, -- prompt_injection, credential_exposure, etc.
    title TEXT NOT NULL,
    description TEXT,
    severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    indicators JSONB, -- {patterns: [], keywords: [], signatures: []}
    affected_systems JSONB, -- {platforms: [], frameworks: [], tools: []}
    mitigation TEXT,
    references JSONB, -- [{url, title}]
    published_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Security Checklist Responses
CREATE TABLE public.checklist_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    scan_id UUID REFERENCES public.scans(id) ON DELETE SET NULL,
    responses JSONB NOT NULL, -- {question_id: {response: 'yes'|'no'|'partial', notes: ''}}
    compliance_score INTEGER,
    gaps JSONB, -- Array of identified gaps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Teams (for Team and Enterprise tiers)
CREATE TABLE public.teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    owner_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    stripe_subscription_id TEXT,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Team Members
CREATE TABLE public.team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID REFERENCES public.teams(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    role TEXT DEFAULT 'member' CHECK (role IN ('admin', 'member', 'viewer')),
    invited_by UUID REFERENCES public.profiles(id),
    invited_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    joined_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(team_id, user_id)
);

-- Custom Rules (Enterprise)
CREATE TABLE public.custom_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID REFERENCES public.teams(id) ON DELETE CASCADE,
    created_by UUID REFERENCES public.profiles(id),
    name TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    pattern TEXT NOT NULL, -- Regex pattern
    recommendation TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit Logs (Enterprise)
CREATE TABLE public.audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID REFERENCES public.teams(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    action TEXT NOT NULL, -- scan_created, settings_changed, member_added, etc.
    resource_type TEXT, -- scan, team, user, settings
    resource_id UUID,
    metadata JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API Usage Logs
CREATE TABLE public.api_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    request_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Row Level Security (RLS)

```sql
-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.findings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.threat_intel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.checklist_responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.custom_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.api_logs ENABLE ROW LEVEL SECURITY;

-- Profiles: Users can read/update their own profile
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Scans: Users can CRUD their own scans
CREATE POLICY "Users can view own scans" ON public.scans
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create scans" ON public.scans
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own scans" ON public.scans
    FOR DELETE USING (auth.uid() = user_id);

-- Team members can view team scans
CREATE POLICY "Team members can view team scans" ON public.scans
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.team_members tm
            JOIN public.profiles p ON p.id = scans.user_id
            WHERE tm.user_id = auth.uid()
            AND tm.team_id IN (
                SELECT team_id FROM public.team_members WHERE user_id = scans.user_id
            )
        )
    );

-- Threat intel: All authenticated users can read active threats
CREATE POLICY "Authenticated users can view threats" ON public.threat_intel
    FOR SELECT USING (auth.role() = 'authenticated' AND is_active = TRUE);

-- Admins can manage threats
CREATE POLICY "Admins can manage threats" ON public.threat_intel
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );
```

---

## Security Scanning Engine Architecture

### Severity Definitions

```typescript
type Severity = 'critical' | 'high' | 'medium' | 'low' | 'passed';

// Scoring impact
const SEVERITY_SCORES = {
    critical: -25,  // Immediate security risk
    high: -10,      // Significant vulnerability
    medium: -5,     // Potential risk
    low: -2,        // Minor concern
    passed: +2      // Best practice detected (max +20 bonus)
};
```

### Rule Categories (OWASP LLM Top 10 2025 Aligned)

1. **LLM01 - Prompt Injection** (`promptInjection.ts`)
2. **LLM02 - Sensitive Information Disclosure** (`credentialExposure.ts`)
3. **LLM03 - Supply Chain Vulnerabilities** (`supplyChain.ts`)
4. **LLM04 - Data and Model Poisoning** (`dataPoisoning.ts`)
5. **LLM05 - Improper Output Handling** (`outputHandling.ts`)
6. **LLM06 - Excessive Agency** (`excessiveAgency.ts`)
7. **LLM07 - System Prompt Leakage** (`promptLeakage.ts`)
8. **LLM08 - Vector and Embedding Weaknesses** (`vectorSecurity.ts`)
9. **LLM09 - Misinformation** (`misinformation.ts`)
10. **LLM10 - Unbounded Consumption** (`resourceLimits.ts`)

### Additional Categories

11. **MCP Security** (`mcpSecurity.ts`) - Model Context Protocol vulnerabilities
12. **Agentic Security** (`agenticSecurity.ts`) - Autonomous agent risks
13. **Compliance** (`compliance.ts`) - GDPR, HIPAA, FERPA, COPPA
14. **Ethical Guardrails** (`ethicalGuardrails.ts`) - Bias, manipulation, harm

---

## Bash Commands

```bash
# Development
npm run dev           # Start Vite dev server
npm run build         # Build for production
npm run preview       # Preview production build
npm run lint          # Run ESLint
npm run typecheck     # Run TypeScript compiler check

# Supabase
npx supabase start    # Start local Supabase
npx supabase stop     # Stop local Supabase
npx supabase db reset # Reset database with migrations
npx supabase gen types typescript --local > src/types/database.ts  # Generate types

# Testing
npm run test          # Run Vitest
npm run test:ui       # Run Vitest with UI
npm run test:coverage # Run with coverage

# Deployment
npx vercel            # Deploy to Vercel
npx supabase db push  # Push migrations to production
```

---

## Code Style Guidelines

- Use ES modules (import/export), not CommonJS
- Destructure imports when possible
- Use TypeScript strict mode
- Prefer `const` over `let`, never use `var`
- Use async/await over .then() chains
- Component files: PascalCase (e.g., `SecurityScanner.tsx`)
- Utility files: camelCase (e.g., `formatters.ts`)
- Use Tailwind CSS for styling, avoid inline styles
- Dark theme is primary - use CSS variables for theming
- All database queries should use Supabase client with proper error handling
- Never expose API keys in frontend code - use environment variables

---

## Environment Variables

```env
# Supabase
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=  # Server-side only

# Stripe
VITE_STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=          # Server-side only
STRIPE_WEBHOOK_SECRET=      # Server-side only

# App
VITE_APP_URL=http://localhost:5173
VITE_API_URL=

# Analytics (optional)
VITE_POSTHOG_KEY=
VITE_POSTHOG_HOST=

# Email (Resend)
RESEND_API_KEY=             # Server-side only
```

---

## Subscription Tiers

| Feature | Free | Pro ($19/mo) | Team ($49/mo) | Enterprise |
|---------|------|--------------|---------------|------------|
| Scans/day | 3 | Unlimited | Unlimited | Unlimited |
| Scan type | Quick | Quick + Deep | All | All + Custom |
| Threat feed | 7-day delay | Real-time | Real-time | Real-time + Custom |
| PDF export | ❌ | ✅ | ✅ | ✅ + Branding |
| API access | ❌ | 100 calls/mo | 500 calls/mo | Unlimited |
| Team seats | 1 | 1 | 5 included | Unlimited |
| SSO | ❌ | ❌ | ❌ | ✅ |
| Audit logs | ❌ | ❌ | ❌ | ✅ |
| Custom rules | ❌ | ❌ | ❌ | ✅ |
| Support | Community | Email | Priority | Dedicated |

---

## API Endpoints (Edge Functions)

```
POST /api/v1/scan
  - Input: { prompt: string, scan_type: 'quick' | 'deep' }
  - Auth: API key in Authorization header
  - Returns: { scan_id, security_score, summary, findings, recommendations }

GET /api/v1/scan/:id
  - Auth: API key
  - Returns: Full scan details

GET /api/v1/threats
  - Query params: ?severity=critical,high&limit=10&after=2025-01-01
  - Auth: API key
  - Returns: { threats: [], total, has_more }

POST /api/v1/checklist
  - Input: { responses: { [question_id]: response } }
  - Auth: API key
  - Returns: { compliance_score, gaps, recommendations }

POST /api/v1/webhooks/stripe
  - Stripe webhook handler for subscription events
```

---

## Design System

### Colors (CSS Variables)

```css
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-tertiary: #1a1a26;
    --bg-card: #15151f;
    
    --accent-cyan: #00d4ff;
    --accent-purple: #8b5cf6;
    --accent-green: #10b981;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --accent-pink: #ec4899;
    
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    --border-subtle: rgba(255,255,255,0.06);
    --border-accent: rgba(0,212,255,0.3);
}
```

### Typography

- Headings: `Space Grotesk` (weight: 600-700)
- Body: `Inter` (weight: 400-500)
- Code/Mono: `JetBrains Mono`

### Component Patterns

- Cards: `bg-card border border-subtle rounded-2xl p-6`
- Buttons Primary: `bg-gradient-to-r from-cyan to-purple text-bg-primary`
- Buttons Secondary: `bg-bg-tertiary border border-subtle`
- Inputs: `bg-bg-secondary border-2 border-subtle focus:border-cyan`
- Severity badges: Use corresponding accent colors

---

## Testing Strategy

- **Unit tests**: Security rule patterns, scoring logic, formatters
- **Integration tests**: Database queries, API endpoints
- **E2E tests**: Critical user flows (scan, subscribe, export)
- Use Vitest for unit/integration, Playwright for E2E

---

## Performance Considerations

- Lazy load scan results and threat feed
- Virtualize long lists (findings, threats)
- Cache threat intel with 5-minute TTL
- Debounce scan input (500ms)
- Use Supabase realtime for threat feed updates (Pro+ only)

---

## Security Considerations (Meta!)

- Sanitize all user input before processing
- Never log full prompt content (privacy)
- Hash prompts for duplicate detection
- Rate limit API endpoints
- Validate API keys on every request
- Use RLS for all database access
- Audit log all admin actions
- HTTPS only, secure cookies
- CSP headers configured
