# HelloPlugin

<!--
## 插件开发者详阅

### 开始

此仓库是 LangBot 插件模板，您可以直接在 GitHub 仓库中点击右上角的 "Use this template" 以创建你的插件。  
接下来按照以下步骤修改模板代码：

#### 修改模板代码

- 修改此文档顶部插件名称信息
- 将此文档下方的`<插件发布仓库地址>`改为你的插件在 GitHub· 上的地址
- 补充下方的`使用`章节内容
- 修改`main.py`中的`@register`中的插件 名称、描述、版本、作者 等信息
- 修改`main.py`中的`MyPlugin`类名为你的插件类名
- 将插件所需依赖库写到`requirements.txt`中
- 根据[插件开发教程](https://docs.langbot.app/plugin/dev/tutor.html)编写插件代码
- 删除 README.md 中的注释内容


#### 发布插件

推荐将插件上传到 GitHub 代码仓库，以便用户通过下方方式安装。   
欢迎[提issue](https://github.com/RockChinQ/LangBot/issues/new?assignees=&labels=%E7%8B%AC%E7%AB%8B%E6%8F%92%E4%BB%B6&projects=&template=submit-plugin.yml&title=%5BPlugin%5D%3A+%E8%AF%B7%E6%B1%82%E7%99%BB%E8%AE%B0%E6%96%B0%E6%8F%92%E4%BB%B6)，将您的插件提交到[插件列表](https://github.com/stars/RockChinQ/lists/qchatgpt-%E6%8F%92%E4%BB%B6)

下方是给用户看的内容，按需修改
-->

## 安装

配置完成 [LangBot](https://github.com/RockChinQ/LangBot) 主程序后使用管理员账号向机器人发送命令即可安装：

```
!plugin get https://github.com/Hanschase/PromptOnlineStore
```
或查看详细的[插件安装说明](https://docs.langbot.app/plugin/plugin-intro.html#%E6%8F%92%E4%BB%B6%E7%94%A8%E6%B3%95)

## 使用
输入!p help或者!pstore help查询帮助<br>
指令：<br>
!pstore help   指令帮助<br>
!pstore list  列出在线列表(normal模式)<br>
!pstore fs    列出在线列表(full-scenario模式)<br>
!pstore next  列表翻页<br>
!pstore <number> 页数翻页<br>
!pstore get <XXX.json/XXX.yaml/all> 下载指定或全部预设<br>
(pstore可简写为p)<br>
=================<br>
注：<br>
1.normal模式下载地址为LangBot/data/prompts<br>
full-scenario模式为LangBot/data/scenario<br>
2.本插件只提供浏览和下载服务,更换预设请通过!default set指令<br>
3.如果您有好的预设，欢迎贡献至：<br>
https://github.com/Hanschase/LangBotPrompts
<!-- 插件开发者自行填写插件使用说明 -->
