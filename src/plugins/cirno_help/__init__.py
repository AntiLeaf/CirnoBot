import nonebot
from nonebot import on_command
# from nonebot.adapters import Bot, Event
from nonebot.plugin import Plugin

from typing import Dict, List, Tuple, Set, Union

from .my_config import Config

from ... import kit
from ...kit.nb import message as mskit


global_config = nonebot.get_driver().config
config = Config.parse_obj(global_config)

__plugin_meta__ = kit.nb.plugin.metadata(
    name = '帮助',
    description = '获取插件描述与用法',
    usage = f'.help 插件 id 或命令以查询插件帮助，或者 .help list 以查询所有可用的帮助',
    extra = {
        'command': 'help',
        'alias' : {'帮助', 'man', 'manual'}
    }
)


def generate_availiable_helps() -> str:
    return '\n'.join([plugin.name + (f'（{plugin.metadata.name}）' if plugin.metadata else '') for plugin in nonebot.get_loaded_plugins()])


def generate_help_message(plugin : Plugin) -> str:
    message = plugin.name

    if plugin.metadata:
        md = plugin.metadata

        if md.name:
            message += f'\n名称：{md.name}'
        if md.description:
            message += f'\n描述：{md.description}'
        if md.usage:
            message += f'\n用法：{md.usage}'
        if 'alias' in md.extra:
            message += '\n别名：{}'.format(' '.join(list(md.extra['alias'])))
    
    else:
        message = f'插件 \"{message}\" 未提供帮助信息'
    
    return message


def search_help_messages(key : str) -> Tuple[bool, str]:
    results : List[Plugin] = []

    for plugin in nonebot.get_loaded_plugins():
        flag = False
        if plugin.name == key:
            flag = True
        elif plugin.metadata:
            if plugin.metadata.name == key:
                flag = True
            elif 'command' in plugin.metadata.extra and key == plugin.metadata.extra['command']:
                flag = True
            elif 'alias' in plugin.metadata.extra and key in plugin.metadata.extra['alias']:
                flag = True
        
        if flag:
            results.append(plugin)
    
    if len(results) == 0:
        return False, f'未找到 \"{key}\" 的帮助信息。\n可用的帮助：\n' + generate_availiable_helps()
    elif len(results) == 1:
        return True, generate_help_message(results[0])
    else:
        return True, f'找到 {len(results)} 条结果：\n\n' + '\n\n'.join([generate_help_message(plugin) for plugin in results])


cirno_help = on_command('help', aliases = __plugin_meta__.extra['alias'])

@cirno_help.handle()
async def cirno_help_handler(matcher : kit.nb.matcher.Matcher, event : Union[mskit.GroupMessageEvent, mskit.PrivateMessageEvent], args : mskit.Message = mskit.params.CommandArg()):
    group_id = event.group_id if isinstance(event, mskit.GroupMessageEvent) else 0
    user_id = event.user_id

    args_list = str(args).split()

    if len(args_list) == 1:
        name = str(args_list[0])

        if name == 'list':
            await mskit.send_reply(message = '可用的帮助：\n' + generate_availiable_helps(), event = event)
        else:
            flag, msg = search_help_messages(name)

            await mskit.send_reply(message = ('\n' if flag else '') + msg, event = event)

    else:
        await mskit.send_reply(message = '用法：' + __plugin_meta__.usage, event = event)
    
    # want to block ?
    # matcher.stop_propagation()