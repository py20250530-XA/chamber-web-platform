# 商会数字服务 Web 平台

HTML + TailwindCSS 3.4.19 + 原生 JavaScript 静态前端。网页及配套源码全部在本仓库根目录，配色为深蓝、金色、浅灰；兼容桌面与移动视口。微信公众号和原预约小程序对接不包含在本次范围。

## 页面清单

| 文件 | 页面 |
|---|---|
| `index.html` | 企业服务主页，六类服务入口、落地指南、企业名录、行业合作 |
| `company-application.html` | 企业入库申请 |
| `service-application.html` | 服务需求／求助 |
| `cooperation-application.html` | 合作对接 |
| `activity-application.html` | 活动报名 |
| `research-application.html` | 调研参与 |
| `consultation-application.html` | 乌方合作咨询，可用 `?lang=ru` / `?lang=uz` |
| `applications.html` | 我的申请，可用 `?lang=ru` / `?lang=uz` |
| `ru.html` | 俄语入口 |
| `uz.html` | 乌兹别克语入口 |

## 样式与交互

- `styles.css`：Tailwind 输入及组件样式。
- `tailwind.config.js`：扫描根目录 HTML 和 JS 的 Tailwind 配置。
- `tailwind.css`：已编译样式，纳入 Git，部署无需 CDN 或 Node 运行时。
- `app.js`：导航、多语言、表单校验、草稿、附件元数据、演示提交、查询、修改、撤回、删除及无障碍弹窗。

这是静态页面实现，不连接真实后台，不提供登录、业务受理或跨设备同步。申请仅保存在当前浏览器 localStorage，编号带 `DEMO` 前缀；页面明确标注演示范围。附件只保存文件名称和大小，不保存文件内容、不上传。请使用测试资料。公开企业、活动、指南和正式联系方式不导入未经核实的演示内容。

## 启动预览

需要 Node.js 18 或以上。直接运行预览无需安装依赖：

```bash
npm start
# 默认8000端口，可使用 PORT=8080 npm start 更改
```

`preview.mjs` 只提供10个页面与CSS/JS静态资源，不公开 `.git`、依赖目录、配置文件或其他源码文件。可以将这些 HTML、`tailwind.css` 和 `app.js` 部署到任意静态网站主机。临时公网隧道进程不纳入仓库，域名仅在预览进程和隧道运行时有效。

## 修改和构建

```bash
npm ci --no-audit --no-fund
npm run build
npm run check
```

`package-lock.json` 固定开发依赖，生产网页无第三方脚本或外部CSS请求。不要编辑已编译样式来代替输入源码；改动HTML中的Tailwind类后重新构建。

## 验证

`check-pages.py` 是可选浏览器检查，需 Python、Playwright 包和 `/usr/bin/chromium`；在预览服务运行时执行：

```bash
python3 check-pages.py
```

覆盖10个页面的电脑和390px手机视口、六类表单、重复提交、刷新持久化、筛选、修改、撤回、草稿、附件限制、存储失败、双语咨询和预览服务私密文件拦截。输出首页截图 `preview-desktop.png`、`preview-mobile.png` 到根目录。真实微信与iOS Safari尚需实机复验。

## 文件清单

所有项目源码和截图都位于根目录。`node_modules/` 仅为开发依赖且被Git忽略；不生成压缩交付包、不使用deliverables目录。
