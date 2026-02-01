# PromptShield - Claude Code Quick Start Guide

## Prerequisites

- Node.js 18+ installed
- Claude Code installed (`npm install -g @anthropic-ai/claude-code` or via recommended method)
- Anthropic API access (Pro or Max plan recommended)
- Supabase account (for database)
- Stripe account (for payments)
- Vercel account (for deployment)

## Step 1: Initialize the Project

```bash
# Create project directory
mkdir promptshield && cd promptshield

# Copy the CLAUDE.md file to this directory
# (This file provides context to Claude Code about the project)

# Start Claude Code
claude
```

## Step 2: Use the Build Prompts

Open `BUILD_PROMPTS.md` and follow the prompts in order:

### Phase 1: Project Setup (Day 1)
```
# In Claude Code, paste each prompt from Phase 1:

Prompt 1.1: Create Project Structure
Prompt 1.2: Set Up Supabase
```

### Phase 2: Security Engine (Day 1-2)
```
# Build the core scanning engine:

Prompt 2.1: Prompt Injection Rules
Prompt 2.2: Credential Exposure Rules
Prompt 2.3: MCP Security Rules
Prompt 2.4: Agentic Security Rules
Prompt 2.5: Compliance Rules
Prompt 2.6: Ethical Guardrails Rules
Prompt 2.7: Main Scanner Engine
```

### Phase 3: Threat Intelligence (Day 2)
```
Prompt 3.1: Threat Intelligence Service
Prompt 3.2: Threat Feed UI
```

### Phase 4: User Interface (Day 2-3)
```
Prompt 4.1: Layout Components
Prompt 4.2: Dashboard Page
Prompt 4.3: Scanner Page
Prompt 4.4: Results Page
Prompt 4.5: Security Checklist
```

### Phase 5: Auth & Subscriptions (Day 3)
```
Prompt 5.1: Auth Pages
Prompt 5.2: Stripe Integration
```

### Phase 6: API & Enterprise (Day 4)
```
Prompt 6.1: API Endpoints
Prompt 6.2: Team Management
Prompt 6.3: Enterprise Features
```

### Phase 7: Testing & Deploy (Day 5)
```
Prompt 8.1: Test Suite
Prompt 8.2: Deploy to Production
```

## Step 3: Use the Security Subagents

Once the project is set up, you can use the custom commands:

```bash
# Run a security review on a prompt
/security-review src/prompts/my-gpt.txt

# Run a compliance review
/compliance-review src/prompts/health-bot.txt --regulations HIPAA,GDPR

# Run threat analysis
/threat-analysis configs/autonomous-agent.yaml
```

## Step 4: Configure Environment

Create `.env.local`:

```env
# Supabase
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

# Stripe  
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...

# App
VITE_APP_URL=http://localhost:5173
```

Create `.env` (for server-side, don't commit):

```env
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
RESEND_API_KEY=re_...
```

## Step 5: Run the Seed Data

```bash
# Apply migrations
npx supabase db push

# Run seed data (threat intel + checklist questions)
npx supabase db seed
```

## Step 6: Start Development

```bash
npm run dev
```

Visit `http://localhost:5173`

## Project Structure After Build

```
promptshield/
├── .claude/
│   ├── agents/
│   │   ├── security-reviewer.md
│   │   ├── compliance-reviewer.md
│   │   └── threat-intel.md
│   └── commands/
│       ├── security-review.md
│       ├── compliance-review.md
│       └── threat-analysis.md
├── src/
│   ├── components/
│   ├── pages/
│   ├── lib/
│   │   └── security/
│   │       ├── scanner.ts
│   │       ├── threatIntel.ts
│   │       └── rules/
│   ├── hooks/
│   └── types/
├── supabase/
│   ├── migrations/
│   ├── functions/
│   └── seed.sql
├── CLAUDE.md
├── BUILD_PROMPTS.md
└── package.json
```

## Useful Claude Code Commands

```bash
# General commands
claude                    # Start Claude Code
claude --help             # Show help

# Development workflow
"Run the dev server"
"Run tests"
"Check for TypeScript errors"
"Deploy to Vercel"

# Custom PromptShield commands
/security-review <file>
/compliance-review <file>
/threat-analysis <file>

# Git operations
"Create a PR for this feature"
"What changed since last commit?"
```

## Troubleshooting

### Claude Code not recognizing CLAUDE.md
- Ensure CLAUDE.md is in the project root
- Restart Claude Code: `claude`

### Supabase connection issues
- Check that local Supabase is running: `npx supabase status`
- Verify environment variables are set

### Build errors
- Ask Claude: "What's causing this build error?"
- Check TypeScript: `npm run typecheck`

### Subagent not working
- Verify files exist in `.claude/agents/` and `.claude/commands/`
- Check file naming matches command name

## Support

For issues with:
- **Claude Code**: Check Anthropic docs or file GitHub issue
- **PromptShield**: Review CLAUDE.md for architecture details
- **Supabase**: Check Supabase documentation
- **Stripe**: Check Stripe documentation

---

**Now go build the security standard for AI applications.**
