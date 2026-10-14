# GitHub Topics

GitHub allows 20 topics per repository, each 50 characters or less in lowercase letters, numbers and hyphens ([GitHub Docs: Classifying your repository with topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)). Topics drive GitHub topic pages and search, so each one below names either a runtime people install skills into or a job these skills do.

| Topic | Who finds the repo through it |
|-|-|
| `agent-skills` | People browsing the Agent Skills format |
| `claude-code` | Claude Code users looking for plugins and skills |
| `claude-skills` | Claude app users looking for uploadable skills |
| `codex` | OpenAI Codex users |
| `github-copilot` | Copilot users |
| `cursor` | Cursor users |
| `mcp` | People looking for MCP-backed tools (the skills call the ScraperCity MCP server) |
| `go-to-market` | GTM teams |
| `outbound` | Outbound teams |
| `cold-email` | People building cold email programs |
| `email-deliverability` | People fixing inbox placement |
| `cold-calling` | Calling teams |
| `lead-generation` | Anyone after leads |
| `list-building` | People building prospect lists |
| `b2b-data` | People shopping for contact and company data |
| `local-business-data` | People prospecting local businesses |
| `prospecting` | SDRs and founders doing their own outreach |
| `sales-automation` | People automating outbound with agents |
| `lead-enrichment` | People filling CRM gaps |
| `scrapercity` | People who already use ScraperCity |

## Set them

```bash
gh api repos/scrapercity/gtm-skills/topics -X PUT --input - <<'EOF'
{"names":["agent-skills","claude-code","claude-skills","codex","github-copilot","cursor","mcp","go-to-market","outbound","cold-email","email-deliverability","cold-calling","lead-generation","list-building","b2b-data","local-business-data","prospecting","sales-automation","lead-enrichment","scrapercity"]}
EOF
gh repo view scrapercity/gtm-skills --json repositoryTopics
```

Revisit the list when a new agent target lands in `install.sh` or a new skill category is added, and drop the least specific topic to stay at 20.
