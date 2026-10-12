# Creator Development Skill

An evidence-preserving Skill for sourcing and reviewing YouTube, TikTok, and Instagram creators. It separates discovery, mechanical screening, contextual review, and delivered records.

## Install

Clone the repository into your agent's skills directory as `creator-development`, or install the `creator-development/` folder from a release archive. Invoke it with `$creator-development`.

## Inputs and output

Minimum inputs are platform, market, category or product fit, target count, and delivery format. Add thresholds, exclusions, contact needs, audience checks, or competitor rules when they matter.

The output contains public identity, dated evidence, field status, decision and reason, stage counts, coverage gaps, and—when Nox is used—task credit consumption and remaining credit with a measurement status.

## Source modes

| Mode | Requirement | Limit |
|---|---|---|
| `public` | No paid-provider credential | Hidden audience and performance data stay unknown. |
| `nox` | User-owned `NOXINFLUENCER_API_KEY` in the runtime environment | Provider field semantics and quota apply; credentials never enter prompts or files. |

Never commit `.env`. If credit attribution is not deterministic, the Skill reports `unavailable`, not zero.

## Example

> Use `$creator-development` in public mode to find 30 US YouTube home-security creators. Exclude outdoor-sports channels and show evidence for every decision.

## Authorization limits

The Skill does not automatically send outreach, write Feishu, create sample orders, or mutate external systems. Those actions require separate authorization and read-back verification.

## Validate

```bash
bash tests/test-security-scanner.sh
bash tests/validate-security.sh
bash tests/validate-contract.sh
```

GitHub is the canonical editable source for `creator-development-skill`. The department NAS contains onboarding documents and stable release copies only.

## License

MIT

## 团队Nox工具包

已授权Nox模式的同事，可使用 [team_bundle/README.md](team_bundle/README.md) 与 [team_bundle/WORKFLOW.md](team_bundle/WORKFLOW.md)。工具支持本轮独立预算、正式服务只读调用、公开视频指标与口播证据。加密凭证文件由负责人单独交接，不进入此仓库。
