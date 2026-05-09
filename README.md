# 🤖 AI Daily — 自动化 AI 新闻日报

[![自动更新](https://img.shields.io/badge/自动更新-每工作日%2006%3A00-2563eb?style=flat-square)](https://yang-builds.github.io/ai-news/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-在线阅读-22c55e?style=flat-square)](https://yang-builds.github.io/ai-news/)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-d97706?style=flat-square)](https://claude.ai)

> 每个工作日 06:00（北京时间），由 Claude AI 自动搜集全球 AI 资讯，生成精美 HTML 页面并发布到 GitHub Pages。

🌐 **在线阅读**：https://yang-builds.github.io/ai-news/

---

## ✨ 特性

- **全自动**：通过 Claude Code Remote（CCR）云端定时任务，无需本地服务器
- **双语处理**：英文搜索国际媒体（Reuters、Bloomberg、TechCrunch、The Verge 等），标题和摘要翻译为中文
- **双 Tab 设计**：🤖 AI 科技快讯（10条）+ 📈 全球市场动态（5条），同一页面切换
- **头条标记**：每期自动识别最重要一条加 🔥 头条标识
- **零依赖部署**：纯 HTML/CSS，无框架，GitHub Pages 直接托管

---

## 🏗️ 技术架构

双语文件已创建完毕。如果你想进一步操作（预览、合并到原文件、更新 index.html 等），告诉我即可。

| 组件 | 技术 |
|---|---|
| 定时触发 | Claude Code Remote Routine（cron  UTC） |
| 资讯搜集 | Claude WebSearch（英文 → 中文翻译） |
| 页面生成 | Claude 生成纯 HTML/CSS（无框架） |
| 发布方式 | GitHub REST API（Contents API PUT） |
| 托管 | GitHub Pages（main 分支根目录） |

---

## 📰 内容分类

**AI 科技快讯**
| 标签 | 分类 |
|---|---|
| 🇨🇳 中国动态 | 国内 AI 政策、产品、公司动态 |
| 🧠 模型前沿 | 大模型发布、研究突破 |
| 💻 开发工具 | AI 编程工具、框架、开源项目 |
| 💰 商业动向 | 融资、并购、商业化进展 |
| 🏭 行业应用 | 各行业 AI 落地案例 |
| 🔒 安全监管 | AI 安全、伦理、政策法规 |

**市场动态**
| 标签 | 分类 |
|---|---|
| 📊 股市动态 | A股/美股/港股 |
| 🏦 宏观经济 | 央行/CPI/GDP |
| 🛢️ 大宗商品 | 黄金/原油/美元 |
| 📜 政策监管 | 减税/关税/制裁 |

---

*由 [Claude AI](https://claude.ai) 自动生成并发布 · Powered by Anthropic*
