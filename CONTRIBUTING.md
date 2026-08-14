# 参与贡献 / Contributing

感谢你对 AccountBindSchool 的关注。本项目当前是本地桌面原型，请优先提交范围明确、可以验证的小改动。

Thank you for contributing to AccountBindSchool. The project is currently a local desktop prototype; prefer focused, verifiable changes.

## 提交前 / Before you start

- Bug 和功能建议请使用对应的 GitHub Issue Form。
- 安全问题不要提交公开 Issue，请按照 [SECURITY.md](SECURITY.md) 私密报告。
- 不要提交真实密码、MAC 地址、令牌或本地 `config.json`。
- 涉及较大行为变化时，先通过 Issue 说明问题和方案。

## 本地开发 / Local development

```bash
git clone https://github.com/ArcPZY/AccountBindSchool.git
cd AccountBindSchool
python -m venv .venv
python -m pip install -r requirements.txt
```

从安全模板创建本地配置：

```powershell
Copy-Item config.example.json config.json
```

macOS / Linux：

```bash
cp config.example.json config.json
```

按照 [README.md](README.md) 获取当前设备 MAC 并完成本地配置，然后运行：

```bash
python main.py
```

## 提交前验证 / Verification

至少运行：

```bash
python -m compileall -q main.py ui utils
python -c "import json; json.load(open('config.example.json', encoding='utf-8'))"
python -c "import xml.etree.ElementTree as ET; ET.parse('docs/assets/account-bind-school-hero.svg')"
```

涉及界面交互时，还应手动验证相关流程；涉及可见变化时，请提供已脱敏的截图或短视频。

## Pull Request

1. 从当前 `main` 创建聚焦的功能分支。
2. 保持改动最小，不重构无关代码。
3. 更新受影响的中英文文档和配置示例。
4. 完成 PR 模板中的验证与安全检查。
5. 清楚说明问题、解决方案、验证环境和结果。

提交 PR 即表示你同意你的贡献按照本项目的 [MIT License](LICENSE) 发布。
