# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x (current snapshot) | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in Thanos (the Grok portable snapshot), please report it responsibly.

**Do NOT open a public issue for security vulnerabilities.**

### How to Report

1. Open a private security advisory on GitHub: https://github.com/iamkaanalper/thanos/security/advisories/new (preferred) or contact via social media / GitHub issues (with credit note to original @vibeeval).
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment:** Within 48 hours
- **Assessment:** Within 7 days
- **Fix:** Depending on severity, within 7-30 days
- **Disclosure:** After the fix is released

### Scope

The following are in scope:
- Hook code execution (Python hooks/adapters in hooks/)
- Export script security (export-thanos-portable.ps1)
- Agent prompt injection vulnerabilities
- Credential/secret exposure in any files in the snapshot

The following are out of scope:
- Issues in Grok CLI itself (report to xAI)
- Social engineering attacks
- Denial of service
- Issues in the original vibecosystem (report to https://github.com/vibeeval/vibecosystem)

### Security Best Practices for Contributors

- Never commit secrets, API keys, or credentials
- All hooks run in the user's shell context - be careful with tool calls
- Agent prompts should not instruct bypassing security controls
- Review export script changes carefully

## Hall of Fame

We appreciate security researchers who help keep Thanos safe. Responsible reporters will be credited here (with permission).

This policy is adapted from the original in vibecosystem by @vibeeval.
