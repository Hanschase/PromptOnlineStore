import os
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.platform.types import *
import requests
import aiohttp

base_url = "https://api.github.com/repos/Hanschase/LangBotPrompts/contents"

# 注册插件
@register(name="PromptOnlineStore", description="LangBot的Prompt在线仓库,使用指令!pstore获取相关信息,欢迎贡献新提示词：https://github.com/Hanschase/LangBotPrompts", version="0.1", author="Hanschase")
class MyPlugin(BasePlugin):
    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.ap = host.ap
        self.all_list = []
        self.page = 0
        self.total_page = 0
        self.ptype = "prompts" #默认为normal模式
        pass

    # 异步初始化
    async def initialize(self):
        pass

    @handler(PersonCommandSent)
    @handler(GroupCommandSent)
    async def send_msg(self,ctx: EventContext):
        help_msg ="""指令：
!pstore help   指令帮助
!pstore list  列出在线列表(normal模式)
!pstore fs    列出在线列表(full-scenario模式)
!pstore next  列表翻页
!pstore <number> 页数翻页
!pstore get <XXX.json/XXX.yaml/all> 下载指定或全部预设
(pstore可简写为p)
=================
注：
1.normal模式下载地址为LangBot/data/prompts
full—scenario模式为LangBot/data/scenario
2.本插件只提供浏览和下载服务,更换预设请通过!default set指令
3.如果您有好的预设，欢迎贡献至：
https://github.com/Hanschase/LangBotPrompts
        """
        if ctx.event.command == "pstore" or ctx.event.command == "p":
            commands = ctx.event.text_message.split()
            ctx.prevent_default()
            ctx.prevent_postorder()
            target_type = ctx.event.launcher_type
            target_id = ctx.event.launcher_id
            if len(commands)>1:
                if commands[1] == "help":
                    await ctx.send_message(target_type,target_id,[help_msg])
                elif commands[1] == "list":
                    self.page = 1
                    self.ptype = "prompts"
                    self.get_info()
                    await self.show(ctx)
                elif commands[1] == "fs":
                    self.page = 1
                    self.ptype = "scenario"
                    self.get_info()
                    await self.show(ctx)
                elif commands[1] == "next":
                    if self.all_list is None:
                        await ctx.send_message(target_type,target_id,["请输入!pstore list 或!pstore fs获取仓库信息"])
                    else:
                        if self.page>=self.total_page:
                            self.page = self.total_page
                        else:
                            self.page += 1
                        await self.show(ctx)
                elif commands[1] == "get":
                    if len(commands)>2:
                        if commands[2] == "all":
                            await self.download_prompts(ctx=ctx,all_flag=True)
                        else:
                            await self.download_prompts(ctx=ctx,pname=commands[2])
                    else:
                        await ctx.send_message(target_type,target_id,["请确保您输入了正确的格式：!pstore get <XXX.json/XXX.yaml/all>"])
                elif commands[1].isdigit():
                    if commands[1]>self.total_page:
                        await ctx.send_message(target_type,target_id,[f"请输入1-{self.total_page}的整数"])
                    else:
                        self.page = int(commands[1])
                        self.get_info()
                        await self.show(ctx)
                else:
                    await ctx.send_message(target_type, target_id,
                                           ["请确保您输入了正确的指令，如有不明白请输入!pstore help查询帮助"])
            else:
                await ctx.send_message(target_type, target_id, ["请输入!pstore help查询提示词在线仓库插件帮助！"])

    async def show(self, ctx: EventContext):
        target_type = ctx.event.launcher_type
        target_id = ctx.event.launcher_id
        self.total_page = len(self.all_list) // 20 + (1 if len(self.all_list) % 20 != 0 else 0)
        start_index = (self.page - 1) * 20 - 1
        if start_index +20 >= len(self.all_list):
            end_index = len(self.all_list)-1
        else:
            end_index = start_index + 20

        show_list = [self.all_list[i] for i in range(start_index, end_index)]
        show_list = '\n'.join(show_list)
        mode = "normal" if self.ptype == "prompts" else "full"
        await ctx.send_message(target_type, target_id, MessageChain([
                        f"={mode}模式提示词仓库=\n",
                        f"{show_list}\n",
                        f"====页数{self.page}/{self.total_page}页===="
                    ]))

    def get_info(self):
        response = requests.get(f"{base_url}/{self.ptype}")
        self.all_list.clear()
        if response.status_code == 200:
            contents = response.json()
            for file in contents:
                self.all_list.append(file["name"])
            self.total_page = len(self.all_list) // 20 + (1 if len(self.all_list) % 20 != 0 else 0)

    async def download_prompts(self,ctx: EventContext,pname = None, all_flag = False):
        target_type = ctx.event.launcher_type
        target_id = ctx.event.launcher_id
        response = requests.get(f"{base_url}/{self.ptype}")
        found = False
        if response.status_code == 200:
            contents = response.json()
            if all_flag:
                await self.check_model(ctx)
                await ctx.send_message(target_type, target_id, MessageChain(["正在下载，请稍后......"]))
                num = 0
                for file in contents:
                    pname = file["name"]
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(file["download_url"]) as response:
                                response.raise_for_status()
                                content = await response.read()
                                with open(f"data/{self.ptype}/{pname}", "wb") as f:
                                    f.write(content)
                        num+=1
                    except Exception as e:
                        self.ap.logger.warning(f"下载预设文件{pname}时发生错误：{e}")
                download_path = os.path.join(os.getcwd(), f'data/{self.ptype}')
                await self.ap.reload(scope="provider")
                await ctx.send_message(target_type, target_id, [f"已成功下载，本次下载共计文件{num}个\n",
                                                                             f"储存地址：{download_path}\n",
                                                                             f"请使用 !default set <预设名>以配置预设"])
                return
            for file in contents:
                if pname == file["name"]:
                    await self.check_model(ctx)
                    found = True
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(file["download_url"]) as response:
                                response.raise_for_status()
                                content = await response.read()
                                with open(f"data/{self.ptype}/{pname}", "wb") as f:
                                    f.write(content)
                        download_path= os.path.join(os.getcwd(), f'data/{self.ptype}/{pname}')
                        await self.ap.reload(scope="provider")
                        await ctx.send_message(target_type, target_id, [f"已成功下载 {pname}\n",
                                                                        f"储存地址：{download_path}\n"
                                                                        f"请使用 !default set {pname.split('.')[0]} 以配置预设"])
                    except Exception as e:
                        await ctx.send_message(target_type, target_id, [f"发生了一个错误：{e}"])
            if not found:
                await ctx.send_message(target_type, target_id, [f"未在{self.ptype}列表中，找到预设文件{pname}，请确保您输入了正确的预设文件名，若列表不是您想要的模式，请输入!pstore list 或者 !pstore fs 切换"])

    #检测配置模式
    async def check_model(self,ctx: EventContext):
        target_type = ctx.event.launcher_type
        target_id = ctx.event.launcher_id
        bot_mode = self.ap.provider_cfg.data["prompt-mode"]
        mode = "normal" if self.ptype == "prompts" else "full-scenario"
        if str(mode).strip() != str(bot_mode).strip():
            await ctx.send_message(target_type,target_id,[f"检测到LangBot预设模式：{bot_mode}，而您下载的预设需要的模式为：{mode}，请在data/config/provider.json或WebUI中修改\"prompt-mode\":\"{mode}\",再使用该预设"])

    # 插件卸载时触发
    def __del__(self):
        pass
