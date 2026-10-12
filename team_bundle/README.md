# Nox 红人开发同事工具包 v1.0.0

适用：同事让 Codex / Claude / 其他本地 Agent 开发 TikTok 红人，组合 Nox 实时发现与公开内容核验。需要 Python 3.11+、Node.js 18.17+、npm；音轨核验另需 ffmpeg。Nox服务和TikTok公开访问仍依赖网络与账号权益，不能承诺每个条件组合都有足量供给。

本目录包含流程、固定版本官方 CLI 的安装定义、预算工具、公开视频数据工具、口播证据工具与示例需求。官方 Nox CLI 通过 npm 安装，不复制第三方源代码；它不是旧版 REST `noxKey` SDK。两枚真实 key 在单独加密文件内，不在此目录或 Git 中。

## 同事第一次使用（macOS）

1. 下载 `nox-creator-team-tools-v1.0.0.zip` 和单独的 `nox-credentials-v1.0.0.enc`，解压工具包。向 Lee 通过单独渠道获取解密口令，勿在群聊或 Agent 提示词粘贴。
2. 在工具包的 `team_bundle` 目录打开终端并执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm install --ignore-scripts
python tools/credentials.py import /你保存的位置/nox-credentials-v1.0.0.enc
```

最后一步不回显口令，解密后直接导入本人 macOS 钥匙串，不产生明文 key 文件。两枚 key 为同一授权集合中的槽位1/2；不要共享本人NAS、飞书或Agent登录账号。

3. 零付费检查：

```bash
python tools/nox.py init --root runs/startup-check --task-id startup-check --budget 0
python tools/nox.py call --root runs/startup-check --slot 1 -- quota
python tools/nox.py call --root runs/startup-check --slot 2 -- quota
python tools/nox.py status --root runs/startup-check
```

必须看到两次 `success=true`，任务 `consumed=0`、`blocked=false`。失败时检查凭证类型、服务权益和网络，勿自动反复查红人试错。

4. 把 `AI_AGENT_USAGE.md` 和项目需求交给 Agent。Agent 需使用 `../SKILL.md` 的通用筛选规则及本包 `WORKFLOW.md`，不是把示例的阈值硬套到所有项目。

## 新项目的操作示例

复制 `examples/brief.json`，填写真实目标、内容画像、预算、历史表链接和交付位置。每个项目建新的任务目录：

```bash
python tools/nox.py init --root runs/demo-task --task-id demo-task --budget 50
python tools/nox.py call --root runs/demo-task --slot 1 -- creator search --platform tiktok --keywords '["photography tips"]' --keyword_match all --country '[US]' --language '[en]' --has_email true --page_size 10 --page_num 1
```

上例可能付费。只在用户批准Nox模式及上限后运行。`response-*.json` 中的内部 `id` 只用于查询；交付必须使用当前公开 `channel_handle`，不得写显示名称或Nox内部id：

```bash
python tools/nox.py call --root runs/demo-task --slot 1 -- creator profile -- REAL_ID_FROM_SEARCH
python tools/public_tiktok.py REAL_PUBLIC_HANDLE --output runs/demo-task/public/creator.json --mean-views-min 10000 --engagement-min 0.01
python tools/sample_audio.py runs/demo-task/public/creator.json --samples 3 --output-dir runs/demo-task/audio/creator
```

把真实值替换掉占位符。若需求要求“每条>9000”，再显式添加 `--per-video-min 9000`；否则不要添加。口播比例若为8/10，必须核验10条及8条实质口播，不可用3条抽查宣称满足。要求仅为“有实质口播”时由Agent说明抽查覆盖、核验讲解内容与音源归属。借用他人的旁白、歌曲歌词、短CTA、重复转录不冒充本人实质口播。

`sample_audio.py` 保存公开音轨以供核验；Apple Silicon可选安装 `mlx-whisper` 作本地初始转录。其他机器或未装转录引擎时，Agent/人直接听音核验。自动语言与转录从不等于最终通过。

## 预算和两个 key

- 一个任务的所有槽位共用一个消耗账本，不能新建目录偷偷重置预算。
- 默认槽位1；槽位2仅在负责人授权使用该备用key时显式选择。无自动重试、无静默跨账号轮换。
- 每个付费调用保守预留5 credits（官方0.5.4 search/profile、搜索最多100项），再按响应 `credits.used` 实际结算。这意味着剩余不足5时提前停，不会为了花完预算冒险调用。
- 中断、缺失计费字段、未知响应或异常扣费会锁住付费续跑。保留 `state.json` / `.call.lock`，先与官方用量核对；不要直接删除锁或修改consumed。没有明确证据的消耗为unavailable，不是0。
- 账户余额可能多人共用；任务消耗可按唯一请求响应计量，但余额不能当成这个项目的剩余预算。多人总量管理由负责人另行协调。
- 工具不提供联系人批量导出、发邮件、私信或外部写操作；最终飞书交付须用同事自己授权的 lark-cli / 飞书 Skill，写后完整回读。

## Windows / Linux

Python与Node工具可使用；激活虚拟环境的命令按系统替换。macOS钥匙串导入不适用。把加密凭证包路径放入运行时 `NOX_CREDENTIALS_FILE`，每次调用由 `getpass` 隐藏输入口令，或由公司自己的Secret Store注入 `NOX_API_KEYS`。不要把明文key写入文件/共享终端历史。ffmpeg需自行安装。本次实际验收在macOS完成，其他系统未作端到端认证。

## Lee 取出这次交接口令

仅在制作该凭证包的Mac上执行：

```bash
python tools/credentials.py copy-release-password
```

程序从钥匙串取出口令并复制到剪贴板，不输出到聊天或终端。通过另一渠道交接后清理剪贴板。工具包 zip 与 `.enc` 文件可以同步到NAS；解密口令必须分开交接。
