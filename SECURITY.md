# Security Policy / 安全策略

## Supported versions / 支持范围

AccountBindSchool is currently a prototype without stable versioned releases. Security fixes are applied to the latest commit on `main`; no older version receives a support guarantee.

AccountBindSchool 当前是尚未发布稳定版本的原型。安全修复仅面向 `main` 的最新提交，不承诺维护旧版本。

## Report a vulnerability / 报告安全问题

Do not open a public Issue for a suspected vulnerability. Use GitHub's [private vulnerability reporting](https://github.com/ArcPZY/AccountBindSchool/security/advisories/new) and include:

请勿通过公开 Issue 报告疑似漏洞。请使用 GitHub 的[私密漏洞报告](https://github.com/ArcPZY/AccountBindSchool/security/advisories/new)，并提供：

- affected commit or version / 受影响的提交或版本；
- impact and realistic attack scenario / 影响与实际攻击场景；
- minimal reproduction steps / 最小复现步骤；
- suggested mitigation, if available / 可行的缓解建议。

Never include real passwords, MAC addresses, tokens, or personal data. Replace sensitive values with obvious placeholders.

请勿提交真实密码、MAC 地址、令牌或个人信息；请使用明确的占位值替代。

The plaintext local password and spoofable MAC allowlist are already documented prototype limitations. Report them only when you have found an impact beyond the documented security boundary.

明文本地密码与可伪造的 MAC 白名单属于已公开的原型限制；只有在发现超出既有安全边界的新影响时才需要报告。
