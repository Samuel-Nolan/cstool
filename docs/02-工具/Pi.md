很多人把 Pi当成Claude Code 的替代品，但它真正厉害的不是终端界面，而是SDK。
Pi不只是Agent，它是一套可以嵌入你自己应用的开发框架。你可以基于它搭一套完全属于自己的AI工作流。
定制分四层，由浅到深：
第一层，Prompt 模板。把常用指令写成
Markdown 文件，放在`.pi/prompts/`目录
下。比如写个review.md，以后在Pi里输入`/review`就能直接调用。
第二层，Skills。按需加载的能力包，写一个SKILL.md说明干什么、分几步做。Pi会自动识别场景并加载，你也可以手动/skill:name 调用。
第三层，Extensions。这是核心。用TypeScript 写自定义工具，注册到Pi里LSP、浏览器、调试器、子代理、MCP服务器，whatever 都能接。Pi出厂只有四个工具，但你可以无限扩展。
第四层，Packages。把Extensions、Skills、Prompts 打包成npm包或git仓库，用piinstall' 一键安装。换机器直接同步，团队也能共享。
最爽的是，你甚至不用自己写代码。直接在Pi里描述你想要的扩展，它会读文档、看代码模式，自己生成 TypeScript 保存到’，pi/extensions/，/reload 就生效。
所以Pi不是成品房，是毛坯房加装修工具箱。社区已经有不少现成材料，你也可以自己造。
如果你想搭一个专业的、高效的、完全按你想法来的Al Agent系统，Pi是一个绕不过去的选型。它默认模型本来就会写代码，不多废话，省token，而且你能把它改成任何你想要的样子。