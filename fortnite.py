# -*- coding: utf-8 -*-

"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019-2020

The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.

Software: PartyBot (fortnitepy-bot)

License: Apache 2.0
"""

try:
    # System imports.
    import asyncio
    import json
    import logging
    import sys

    # Third party imports.
    import partybot
    import aiofiles
    import fortnitepy
    import crayons
    import aiohttp
except ModuleNotFoundError as e:
    print(e)
    print('Failed to import 1 or more modules, running "INSTALL PACKAGES.bat" '
          'might fix the issue, if not please create an issue or join '
          'the support server.')
    sys.exit()

# Imports uvloop and uses it if installed (Unix only).
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if sys.platform == 'win32':
    asyncio.set_event_loop(asyncio.ProactorEventLoop())


def enable_debug() -> None:
    logger = logging.getLogger('fortnitepy.http')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[36m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)
    except Exception:
                if data['loglevel'] == 'debug':
                    send(name(client.user),traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')

            client.owner = []
            for owner in data['fortnite']['owner']:
                user = client.get_user(owner) or client.get_cache_user(owner)
                if not user:
                    try:
                        user = await client.fetch_user(owner)
                    except fortnitepy.HTTPException:
                        if data['loglevel'] == 'debug':
                            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        send(display_name,l("error_while_requesting_userinfo"),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                    except Exception:
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                if not user:
                    send(display_name,l("owner_notfound",owner),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                else:
                    client.add_cache(user)
                    friend = client.get_friend(user.id)
                    if not friend:
                        send(display_name,l("not_friend_with_owner",commands["reload"]),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                        if data['fortnite']['addfriend'] and not client.is_pending(user.id):
                            try:
                                await client.add_friend(user.id)
                            except fortnitepy.HTTPException:
                                if data['loglevel'] == 'debug':
                                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                                send(display_name,l("error_while_sending_friendrequest"),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                            except Exception:
                                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    else:
                        client.owner.append(friend)
                        send(display_name,f'{l("owner")}: {name(friend)}',green,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            if client.owner and data['fortnite']['click_invite']:
                for owner in client.owner:
                    await owner.send(l("click_invite"))

            lists = {
                "blacklist": "blacklist",
                "whitelist": "whitelist",
                "otherbotlist": "botlist"
            }
            async def _(listuser: str) -> None:
                user = client.get_user(listuser) or client.get_cache_user(listuser)
                if not user:
                    try:
                        user = await client.fetch_user(listuser)
                    except fortnitepy.HTTPException:
                        if data['loglevel'] == 'debug':
                            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        send(display_name,l("error_while_requesting_userinfo"),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                    except Exception:
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                if not user:
                    send(display_name,l(f"{data_}_user_notfound",listuser),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                else:
                    client.add_cache(user)
                    if data_ == "blacklist" and data["fortnite"]["blacklist-autoblock"]:
                        try:
                            await user.block()
                        except Exception:
                            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    globals()[list_].append(user.id)

            for list_,data_ in lists.items():
                try:
                    await asyncio.gather(*[_(listuser) for listuser in data['fortnite'][list_]])
                except Exception:
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                if data['loglevel'] == "debug":
                    send(display_name,f"fortnite {data_}list {globals()[list_]}",yellow,add_d=lambda x:f'```\n{x}\n```')

            lists = [
                "outfitmimic",
                "backpackmimic",
                "pickaxemimic",
                "emotemimic"
            ]
            async def _(mimic: str) -> None:
                if isinstance(data['fortnite'][mimic],str):
                    user = client.get_user(mimic) or client.get_cache_user(mimic)
                    if not user:
                        try:
                            user = await client.fetch_user(data['fortnite'][mimic])
                        except fortnitepy.HTTPException:
                            if data['loglevel'] == 'debug':
                                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                            send(display_name,l("error_while_requesting_userinfo"),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                        except Exception:
                            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    if not user:
                        send(display_name,l(f"{mimic}_user_notfound",data['fortnite'][mimic]),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                    else:
                        client.add_cache(user)
                        setattr(client,mimic,user.id)
                        if data['loglevel'] == "debug":
                            send(display_name,f"{mimic} {getattr(client,mimic)}",yellow,add_d=lambda x:f'```\n{x}\n```')
            try:
                await asyncio.gather(*[_(mimic) for mimic in lists])
            except Exception:
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')

            async def _(listuser: str) -> None:
                user = client.get_user(listuser) or client.get_cache_user(listuser)
                if not user:
                    try:
                        user = await client.fetch_user(listuser)
                    except fortnitepy.HTTPException:
                        if data['loglevel'] == 'debug':
                            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        send(display_name,l("error_while_requesting_userinfo"),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                if not user:
                    send(display_name,l("invitelist_user_notfound",listuser),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                else:
                    client.add_cache(user)
                    friend = client.get_friend(user.id)
                    if not friend:
                        send(display_name,l("not_friend_with_inviteuser",listuser,commands["reload"]),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                        if data['fortnite']['addfriend'] and not client.is_pending(user.id) and user.id != client.user.id:
                            try:
                                await client.add_friend(user.id)
                            except fortnitepy.HTTPException:
                                if data['loglevel'] == 'debug':
                                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                                send(display_name,l("error_while_sending_friendrequest"),red,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}',add_d=lambda x:f'>>> {x}')
                    else:
                        client.invitelist.append(friend.id)
            try:
                await asyncio.gather(*[_(listuser) for listuser in data['fortnite']['invitelist']])
            except Exception:
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            if data['loglevel'] == "debug":
                send(display_name,f'invitelist {client.invitelist}',yellow,add_d=lambda x:f'```\n{x}\n```')

            if data['fortnite']['acceptfriend']:
                async def _(pending: fortnitepy.IncomingPendingFriend) -> None:
                    if client.acceptfriend is True:
                        try:
                            await pending.accept()
                        except fortnitepy.HTTPException:
                            if data['loglevel'] == 'debug':
                                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                            try:
                                await pending.decline()
                            except fortnitepy.HTTPException:
                                if data['loglevel'] == 'debug':
                                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    elif client.acceptfriend is False:
                        try:
                            await pending.decline()
                        except fortnitepy.HTTPException:
                            if data['loglevel'] == 'debug':
                                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                try:
                    await asyncio.gather(*[_(pending) for pending in client.incoming_pending_friends])
                except Exception:
                    data["discord"]["enabled"] = False
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')

            if data['discord']['enabled'] and dclient.isready:
                dclient_user = name(dclient.user)

                dclient.owner = []
                for owner in data['discord']['owner']:
                    user = dclient.get_user(owner)
                    if not user:
                        try:
                            user = await dclient.fetch_user(owner)
                        except discord.NotFound:
                            if data['loglevel'] == "debug":
                                send(dclient_user,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        except discord.HTTPException:
                            if data['loglevel'] == 'debug':
                                send(dclient_user,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                            send(dclient_user,l('error_while_requesting_userinfo'),red,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}',add_d=lambda x:f'>>> {x}')
                    if not user:
                        send(dclient_user,l('discord_owner_notfound',owner),red,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}',add_d=lambda x:f'>>> {x}')
                    else:
                        dclient.owner.append(user)
                        send(dclient_user,f"{l('owner')}: {name(user)}",green,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}')

                lists = {
                    "blacklist_": "blacklist",
                    "whitelist_": "whitelist"
                }
                async def _(listuser: str) -> None:
                    listuser = int(listuser)
                    user = dclient.get_user(listuser)
                    if not user:
                        try:
                            user = await dclient.fetch_user(listuser)
                        except discord.NotFound:
                            if data['loglevel'] == "debug":
                                send(dclient_user,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                            send(dclient_user,l(f'discord_{data_}_user_notfound', listuser),red,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}',add_d=lambda x:f'>>> {x}')
                            return
                    globals()[list_].append(user.id)

                for list_,data_ in lists.items():
                    await asyncio.gather(*[_(listuser) for listuser in data['discord'][data_]])
                    if data['loglevel'] == "debug":
                        send(dclient_user,f"discord {data_}list {globals()[list_]}",yellow,add_d=lambda x:f'```\n{x}\n```')
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['addblacklist']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['addblacklist']}] [{l('name_or_id')}]")
                return
            if data["caseinsensitive"]:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(name).lower()) and user.id != client.user.id and user.id not in blacklist}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(name) and user.id != client.user.id and user.id not in blacklist}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if user.id not in blacklist:
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', len(users)))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if user.id not in blacklist:
                    blacklist.append(user.id)
                    if user.display_name:
                        data["fortnite"]["blacklist"].append(user.display_name)
                    else:
                        data["fortnite"]["blacklist"].append(user.id)
                    data_ = load_json("config.json")
                    data_["fortnite"]["blacklist"] = data["fortnite"]["blacklist"]
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                    send(display_name,l('add_to_list', f'{name(user)}', l('blacklist')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                    await reply(message, client, l('add_to_list', f'{name(user)}', l('blacklist')))
                else:
                    await reply(message, client, l('already_in_list', f'{name(user)}', l('blacklist')))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
            if user.id not in blacklist:
                blacklist.append(user.id)
                if user.display_name:
                    data["fortnite"]["blacklist"].append(user.display_name)
                else:
                    data["fortnite"]["blacklist"].append(user.id)
                data_ = load_json("config.json")
                data_["fortnite"]["blacklist"] = data["fortnite"]["blacklist"]
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                send(display_name,l('add_to_list', f'{name(user)}', l('blacklist')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                await reply(message, client, l('add_to_list', f'{name(user)}', l('blacklist')))
            else:
                await reply(message, client, l('already_in_list', f'{name(user)}', l('blacklist')))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_add_to_list', l('blacklist'))}"
                await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['removeblacklist']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['removeblacklist']}] [{l('name_or_id')}]")
                return
            if data["caseinsensitive"]:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and user.id in blacklist}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and user.id in blacklist}
            try:
                user = await client.fetch_user(rawcontent)
                if not user:
                    if user.id in blacklist:
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if user.id in blacklist:
                    blacklist.remove(user.id)
                    try:
                        data["fortnite"]["blacklist"].remove(str(user.display_name))
                    except ValueError:
                        data["fortnite"]["blacklist"].remove(user.id)
                    data_ = load_json("config.json")
                    data_["fortnite"]["blacklist"] = data["fortnite"]["blacklist"]
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                    send(display_name,l('remove_from_list', name(user), l('blacklist')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                    await reply(message, client, l('remove_from_list', name(user), l('blacklist')))
                else:
                    await reply(message, client, l('not_list', name(user), l('blacklist')))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        if user.id in blacklist:
            blacklist.remove(user.id)
            try:
                data["fortnite"]["blacklist"].remove(str(user.display_name))
            except ValueError:
                data["fortnite"]["blacklist"].remove(user.id)
            data_ = load_json("config.json")
            data_["fortnite"]["blacklist"] = data["fortnite"]["blacklist"]
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
            send(display_name,l('remove_from_list', name(user), l('blacklist')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, l('remove_from_list', name(user), l('blacklist')))
        else:
            await reply(message, client, l('not_list', name(user), l('blacklist')))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_remove_from_list', l('blacklist'))}"
                await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['addwhitelist']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['addwhitelist']}] [{l('name_or_id')}]")
                return
            if data["caseinsensitive"]:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and user.id not in whitelist}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and user.id not in whitelist}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if user.id not in whitelist:
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(l("bot"),traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if user.id not in whitelist:
                    whitelist.append(user.id)
                    if user.display_name:
                        data["fortnite"]["whitelist"].append(str(user.display_name))
                    else:
                        data["fortnite"]["whitelist"].append(user.id)
                    data_ = load_json("config.json")
                    data_["fortnite"]["whitelist"] = data["fortnite"]["whitelist"]
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                    send(display_name,l("add_to_list",name(user),l('whitelist')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                    await reply(message, client, l("add_to_list", name(user), l('whitelist')))
                else:
                    await reply(message, client, l("already_list", name(user), l('whitelist')))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
            if user.id not in whitelist:
                whitelist.append(user.id)
                if user.display_name:
                    data["fortnite"]["whitelist"].append(str(user.display_name))
                else:
                    data["fortnite"]["whitelist"].append(user.id)
                data_ = load_json("config.json")
                data_["fortnite"]["whitelist"] = data["fortnite"]["whitelist"]
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                send(display_name,l("add_to_list",name(user),l('whitelist')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                await reply(message, client, l("add_to_list", name(user), l('whitelist')))
            else:
                await reply(message, client, l("already_list", name(user), l('whitelist')))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_add_to_list', l('whitelist'))}"
                await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['removewhitelist']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['removewhitelist']}] [{l('name_or_id')}]")
                return
            if data["caseinsensitive"]:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and user.id in whitelist}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and user.id in whitelist}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if user.id in whitelist:
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(l("bot"),traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l("too_many_users", str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if user.id in whitelist:
                    whitelist.remove(user.id)
                    try:
                        data["whitelist"].remove(str(user.display_name))
                    except ValueError:
                        data["whitelist"].remove(user.id)
                    data_ = load_json("config.json")
                    data_["whitelist"] = data["whitelist"]
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                    send(display_name,l("remove_from_list",name(user),l("whitelist")),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                    await reply(message, client, l("remove_from_list", name(user), l('whitelist')))
                else:
                    await reply(message, client, l("not_list", name(user), l('whitelist')))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        if user.id in whitelist:
            whitelist.remove(user.id)
            try:
                data["whitelist"].remove(str(user.display_name))
            except ValueError:
                data["whitelist"].remove(user.id)
            data_ = load_json("config.json")
            data_["whitelist"] = data["whitelist"]
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
            send(display_name,l("remove_from_list",name(user),l("whitelist")),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, l("remove_from_list", name(user), l('whitelist')))
        else:
            await reply(message, client, l("not_list", name(user), l('whitelist')))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_remove_from_list', l('whitelist'))}"
                await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['addinvitelist']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['addinvitelist']}] [{l('name_or_id')}]")
                return
            if data["caseinsensitive"]:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and user.id not in client.invitelist}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and user.id not in client.invitelist}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if user.id not in client.invitelist:
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l("too_many_users", str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if user.id not in client.invitelist:
                    client.invitelist.append(user.id)
                    if user.display_name:
                        data["fortnite"]["invitelist"].append(str(user.display_name))
                    else:
                        data["fortnite"]["invitelist"].append(user.id)
                    data_ = load_json("config.json")
                    data_["fortnite"]["invitelist"] = data["fortnite"]["invitelist"]
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                    send(display_name,l("add_to_list",name(user),l("invitelist")),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                    await reply(message, client, l("add_to_list", name(user), l('invitelist')))
                else:
                    await reply(message, client, l("already_list", name(user), l('invitelist')))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        if user.id not in client.invitelist:
            client.invitelist.append(user.id)
            if user.display_name:
                data["fortnite"]["invitelist"].append(str(user.display_name))
            else:
                data["fortnite"]["invitelist"].append(user.id)
            data_ = load_json("config.json")
            data_["fortnite"]["invitelist"] = data["fortnite"]["invitelist"]
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
            send(display_name,l("add_to_list",name(user),l("invitelist")),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, l("add_to_list", name(user), l('invitelist')))
        else:
            await reply(message, client, l("already_list", name(user), l('invitelist')))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_add_to_list', l('invitelist'))}"
                await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['removeinvitelist']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['removeinvitelist']}] [{l('name_or_id')}]")
                return
            if data["caseinsensitive"]:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and user.id in client.invitelist}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and user.id in client.invitelist}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if user.id in client.invitelist:
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l("too_many_users", str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if user.id in client.invitelist:
                    client.invitelist.remove(user.id)
                    try:
                        data["fortnite"]["invitelist"].remove(str(user.display_name))
                    except ValueError:
                        data["fortnite"]["invitelist"].remove(user.id)
                    data_ = load_json("config.json")
                    data_["fortnite"]["invitelist"] = data["fortnite"]["invitelist"]
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
                    send(display_name,l("remove_from_list",name(user),l("invitelist")),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                    await reply(message, client, l("remove_from_list", name(user), l('invitelist')))
                else:
                    await reply(message, client, l("not_list", name(user), l('invitelist')))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        if user.id in client.invitelist:
            client.invitelist.remove(user.id)
            try:
                data["fortnite"]["invitelist"].remove(str(user.display_name))
            except ValueError:
                data["fortnite"]["invitelist"].remove(user.id)
            data_ = load_json("config.json")
            data_["fortnite"]["invitelist"] = data["fortnite"]["invitelist"]
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data_, f, ensure_ascii=False, indent=4, sort_keys=False)
            send(display_name,l("remove_from_list",name(user),l("invitelist")),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, l("remove_from_list", name(user), l('invitelist')))
        else:
            await reply(message, client, l("not_list", name(user), l('invitelist')))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_remove_from_list', l('invitelist'))}"
                await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['get']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['get']}] [{l('name_or_id')}]")
                return
            if data["caseinsensitive"]:
                users = {str(member.display_name): member for member in client.party.members if content_ in jaconv.kata2hira(str(member.display_name).lower())}
            else:
                users = {str(member.display_name): member for member in client.party.members if content_ in str(member.display_name)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.party.get_member(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l("too_many_users", str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                member = client.party.get_member(user.id)
                if not member:
                    await reply(message, client, l("user_not_in_party"))
                    return
                send(display_name,f'{name(member)}\n{member.outfit} {member.outfit_variants}\n{partymember_backpack(member)} {member.backpack_variants}\n{member.pickaxe} {member.pickaxe_variants}\n{partymember_emote(member)}',add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                if data['loglevel'] == 'debug':
                    send(display_name,json.dumps(member.meta.schema, indent=2),yellow,add_d=lambda x:f'```\n{x}\n```',add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                await reply(message, client, f'{name(member)}\n{member.outfit} {member.outfit_variants}\n{partymember_backpack(member)} {member.backpack_variants}\n{member.pickaxe} {member.pickaxe_variants}\n{partymember_emote(member)}')
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        member = client.party.get_member(user.id)
        if not member:
            await reply(message, client, l("user_not_in_party"))
            return
        send(display_name,f'{name(member)}\n{member.outfit} {member.outfit_variants}\n{partymember_backpack(member)} {member.backpack_variants}\n{member.pickaxe} {member.pickaxe_variants}\n{partymember_emote(member)}',add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
        if data['loglevel'] == 'debug':
            send(display_name,json.dumps(member.meta.schema, indent=2),yellow,add_d=lambda x:f'>>> {x}',add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
        await reply(message, client, f'{name(member)}\n{member.outfit} {member.outfit_variants}\n{partymember_backpack(member)} {member.backpack_variants}\n{member.pickaxe} {member.pickaxe_variants}\n{partymember_emote(member)}')""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_get_userinfo')}"
                await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['friendcount']:
        try:
            send(display_name,f"{l('friendcount')}: {len(client.friends)}",add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, f"{l('friendcount')}: {len(client.friends)}")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['pendingcount']:
        try:
            send(display_name,f"{l('pendingcount')}: {len(client.pending_friends)}\n{l('outbound')}: {len(client.outgoing_pending_friends)}\n{l('inbound')}: {len(client.incoming_pending_friends)}",add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, f"{l('pendingcount')}: {len(client.pending_friends)}\n{l('outbound')}: {len(client.outgoing_pending_friends)}\n{l('inbound')}: {len(client.incoming_pending_friends)}")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['blockcount']:
        try:
            send(display_name,f"{l('blockcount')}: {len(client.blocked_users)}",add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, f"{l('blockcount')}: {len(client.blocked_users)}")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['friendlist']:
        try:
            text = ''
            for friend in client.friends:
                client.add_cache(friend)
                text += f'\n{name(friend)}'
            send(display_name,text,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, f'{text}')
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['pendinglist']:
        try:
            outgoing = ''
            incoming = ''
            for pending in client.pending_friends:
                client.add_cache(pending)
                if pending.outgoing:
                    outgoing += f'\n{name(pending)}'
                elif pending.incoming:
                    incoming += f'\n{name(pending)}'
            send(display_name,f"{l('outbound')}: {outgoing}\n{l('inbound')}: {incoming}",add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, f"{l('outbound')}: {outgoing}\n{l('inbound')}: {incoming}")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['blocklist']:
        try:
            text = ''
            for block in client.blocked_users:
                client.add_cache(block)
                text += f'\n{name(block)}'
            send(display_name,text,add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
            await reply(message, client, f'{text}')
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['wait']:
        try:
            if not client.acceptinvite:
                if isinstance(message, fortnitepy.message.MessageBase) or isinstance(getattr(message,"base",None), fortnitepy.message.MessageBase):
                    if (not (message.author.id in [owner.id for owner in client.owner])
                        and not (message.author.id in whitelist and data['fortnite']['whitelist-ownercommand'])
                        and not (message.author.id in [owner.id for owner in dclient.owner])
                        and not (message.author.id in whitelist_ and data['discord']['whitelist-ownercommand'])):
                        await reply(message, client, l('invite_is_decline'))
                        return
            client.acceptinvite = False
            try:
                client.timer_.cancel()
            except AttributeError:
                pass
            client.timer_ = Timer(data['fortnite']['waitinterval'], client.inviteaccept)
            client.timer_.start()
            await reply(message, client, l('decline_invite_for', str(data['fortnite']['waitinterval'])))
        except Exception:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['join']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['join']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.has_friend(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.has_friend(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.has_friend(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                friend = client.get_friend(user.id)
                if not friend:
                    await reply(message, client, l('not_friend_with_user'))
                else:
                    await friend.join_party()
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            friend = client.get_friend(user.id)
            if not friend:
                await reply(message, client, l('not_friend_with_user'))
            else:
                await friend.join_party()
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_full_or_already_or_offline'))
        except fortnitepy.NotFound:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_notfound'))
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_private'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_joining_to_party'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"{l('enter_to_join_party')}"
                await reply(message, client, text)
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_full_or_already_or_offline'))
        except fortnitepy.NotFound:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_notfound'))
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_private'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_joining_to_party'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['joinid']:
        try:
            await client.join_party(party_id=args[1])
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_full_or_already'))
        except fortnitepy.NotFound:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_notfound'))
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_private'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['join']}] [{l('party_id')}]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['leave']:
        try:
            await client.party.me.leave()
            await reply(message, client, l('party_leave', client.party.id))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_leaving_party'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['invite']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['invite']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.has_friend(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.has_friend(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.has_friend(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                friend = client.get_friend(user.id)
                if not friend:
                    await reply(message, client, l('not_friend_with_user'))
                    return
                await friend.invite()
                await reply(message, client, l('user_invited', name(friend), client.party.id))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            friend = client.get_friend(user.id)
            if not friend:
                await reply(message, client, l('not_friend_with_user'))
                return
            await friend.invite()
            await reply(message, client, l('user_invited', name(friend), client.party.id))
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_full_or_already'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_sending_partyinvite'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_invite_user')}"
                await reply(message, client, text)
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('party_full_or_already'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_sending_partyinvite'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['inviteall']:
        try:
            [loop.create_task(client.party.invite(inviteuser)) for inviteuser in client.invitelist]
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['message']:
        try:
            text = rawcontent.split(' : ')
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if text[0] in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.has_friend(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if text[0] in str(user.display_name) and user.id != client.user.id and client.has_friend(user.id)}
            try:
                user = await client.fetch_user(text[0])
                if user:
                    if client.has_friend(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                friend = client.get_friend(user.id)
                if not friend:
                    await reply(message, client, l('not_friend_with_user'))
                    return
                await friend.send(text[1])
                await reply(message, client, l('user_sent', name(friend), text[1]))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            friend = client.get_friend(user.id)
            if not friend:
                await reply(message, client, l('not_friend_with_user'))
                return
            await friend.send(text[1])
            await reply(message, client, l('user_sent', name(friend), text[1]))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l("error_while_requesting_userinfo"))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user, "text": text} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_send')}"
                await reply(message, client, text)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l("error_while_requesting_userinfo"))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['message']}] [{l('name_or_id')}] : [{l('content')}]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['partymessage']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['partymessage']}] [{l('content')}]")
                return
            await client.party.send(rawcontent)
            await reply(message, client, l('party_sent', client.party.id, rawcontent))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['sendall']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['sendall']}] [{l('content')}]")
                return
            tasks = {}
            for client_ in loadedclients:
                mes = AllMessage(rawcontent, message.author, client_, message)
                task = loop.create_task(process_command(mes))
                tasks[client_] = [task, mes]
            await asyncio.gather(*[i[0] for i in tasks.values()])
            for client_,list_ in tasks.items():
                result = list_[1].result
                if result.get(client_.user.id):
                    results = '\n'.join(result[client_.user.id])
                    await reply(message, client, f"[{name(client_.user)}] {results}")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['status']:
        try:
            client.status_ = rawcontent
            await client.change_status()
            await reply(message, client, l('set_to', l('status'), rawcontent))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['status']}] [{l('content')}]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['avatar']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['avatar']}] [ID]")
                return
            if len(args) > 4:
                background_colors = [args[2], args[3], args[4]]
            elif len(args) == 2:
                background_colors = None
            else:
                background_colors = getattr(fortnitepy.KairosBackgroundColorPreset, args[2])
            avatar = fortnitepy.Avatar(asset=args[1], background_colors=background_colors)
            client.set_avatar(avatar)
            await reply(message, client, l('set_to', l('avatar'), f"{args[1]}, {background_colors}"))
        except AttributeError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('color_must_be'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['banner']:
        try:
            await client.party.me.edit_and_keep(partial(client.party.me.set_banner,args[1],args[2],client.party.me.banner[2]))
            await reply(message, client, l('set_to', l('banner'), f"{args[1]}, {args[2]}"))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['banner']}] [{l('bannerid')}] [{l('color')}]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['level']:
        try:
            await client.party.me.edit_and_keep(partial(client.party.me.set_banner,client.party.me.banner[0],client.party.me.banner[1],int(args[1])))
            await reply(message, client, l('set_to', l('level'), args[1]))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except ValueError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('must_be_int'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['level']}] [{l('level')}]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['bp']:
        try:
            await client.party.me.edit_and_keep(partial(client.party.me.set_battlepass_info,True,args[1],args[2],args[3]))
            await reply(message, client, l('set_to', l('bpinfo'), f"{l('tier')}: {args[1]}, {l('xpboost')}: {args[2]}, {l('friendxpboost')}: {args[3]}"))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_bpinfo'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['bp']}] [{l('tier')}] [{l('xpboost')}] [{l('friendxpboost')}]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['privacy']:
        try:
            privacies = [
                "privacy_public",
                "privacy_friends_allow_friends_of_friends",
                "privacy_friends",
                "privacy_private_allow_friends_of_friends",
                "privacy_private"
            ]
            for privacy in privacies:
                if args[1] in commands[privacy]:
                    priv = getattr(PartyPrivacy,privacy.replace("privacy_","",1).upper()).value
                    await client.party.set_privacy(priv)
                    await reply(message, client, l('set_to', l('privacy'), l(privacy.replace("privacy_","",1))))
                    break
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['privacy']}] [[{commands['privacy_public']}] / [{commands['privacy_friends_allow_friends_of_friends']}] / [{commands['privacy_friends']}] / [{commands['privacy_private_allow_friends_of_friends']}] / [{commands['privacy_private']}]]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error')) 

    elif args[0] in commands['getuser']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['getuser']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    users[str(user.display_name)] = user
                    client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            text = str()
            for user in users.values():
                text += f'\n{name(user)}'
            send(display_name,text)
            await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['getfriend']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['getfriend']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.has_friend(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.has_friend(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.has_friend(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            text = str()
            for user in users.values():
                friend = client.get_friend(user.id)
                if not friend:
                    return
                if not friend.nickname:
                    text += f'\n{str(friend.display_name)} / {friend.id}'
                else:
                    text += f'\n{friend.nickname}({str(friend.display_name)}) / {friend.id}'
                if friend.last_presence and friend.last_presence.avatar:
                    text += f"\n{l('avatar')}: {friend.last_presence.avatar.asset}"
                if friend.last_logout:
                    text += "\n{1}: {0.year}/{0.month}/{0.day} {0.hour}:{0.minute}:{0.second}".format(friend.last_logout, l('lastlogin'))
            send(display_name,text)
            await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['getpending']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['getpending']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.is_pending(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.is_pending(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.is_pending(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            text = str()
            for user in users.values():
                pending = client.get_pending_friend(user.id)
                if not pending:
                    return
                text += f'\n{str(pending.display_name)} / {pending.id}'
            send(display_name,text)
            await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['getblock']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['getblock']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.is_blocked(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.is_blocked(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.is_blocked(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            text = str()
            for user in users.values():
                block = client.get_blocked_user(user.id)
                if not block:
                    return
                text += f'\n{str(block.display_name)} / {block.id}'
            send(display_name,text)
            await reply(message, client, text)
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['info']:
        try:
            if args[1] in commands['info_party']:
                text = str()
                text += f"{client.party.id}\n{l('member_count')}: {client.party.member_count}\n{client.party.playlist_info[0]}"
                for member in client.party.members:
                    client.add_cache(member)
                    if data['loglevel'] == 'normal':
                        text += f'\n{str(member.display_name)}'
                    else:
                        text += f'\n{str(member.display_name)} / {member.id}'
                send(display_name,text)
                await reply(message, client, text)
                if data['loglevel'] == 'debug':
                    send(display_name,json.dumps(client.party.meta.schema,indent=4),yellow,add_d=lambda x:f'```\n{x}\n```')
            
            elif True in [args[1] in commands[key] for key in ("cid", "bid", "petcarrier", "pickaxe_id", "eid", "emoji_id", "toy_id", "id")]:
                type_ = convert_to_type(args[1])
                if rawcontent2 == '':
                    await reply(message, client, f"[{commands[convert_to_old_type(type_)]}] [ID]")
                    return
                result = await loop.run_in_executor(None, search_item, data["search-lang"], "id", rawcontent2, type_)
                if not result and data["sub-search-lang"] != data["search-lang"]:
                    result = await loop.run_in_executor(None, search_item, data["sub-search-lang"], "id", rawcontent2, type_)
                if not result:
                    await reply(message, client, l('item_notfound'))
                else:
                    if len(result) > search_max:
                        await reply(message, client, l('too_many_items', str(len(result))))
                        return
                    if len(result) == 1:
                        await reply(message, client, f"{convert_backend_type(result[0]['backendType'])}: {result[0]['name']} | {result[0]['id']}\n{result[0]['description']}\n{result[0]['rarity']}\n{result[0]['set']}")
                    else:
                        text = str()
                        for count, item in enumerate(result):
                            text += f"\n{count+1} {convert_backend_type(item['backendType'])}: {item['name']} | {item['id']}"
                        text += f"\n{l('enter_to_show_info')}"
                        await reply(message, client, text)
                        client.select[message.author.id] = {
                            "exec": [
                                """\
                                await reply(message, client, f"{convert_backend_type(item['backendType'])}: {item['name']} | {item['id']}\n{item['description']}\n{item['rarity']}\n{item['set']}")""" for item in result
                                ],
                                "variable": [
                                    {"item": item} for item in result
                                ]
                            }

            elif True in  [args[1] in commands[key] for key in ("outfit", "backpack", "pet", "pickaxe", "emote", "emoji", "toy", "item")]:
                type_ = convert_to_type(args[1])
                if rawcontent2 == '':
                    await reply(message, client, f"[{commands[convert_to_old_type(type_)]}] [{l('itemname')}]")
                    return
                result = await loop.run_in_executor(None, search_item, data["search-lang"], "name", rawcontent2, type_)
                if not result and data["sub-search-lang"] != data["search-lang"]:
                    result = await loop.run_in_executor(None, search_item, data["sub-search-lang"], "name", rawcontent2, type_)
                if not result:
                    await reply(message, client, l('item_notfound'))
                else:
                    if len(result) > search_max:
                        await reply(message, client, l('too_many_items', str(len(result))))
                        return
                    if len(result) == 1:
                        await reply(message, client, f"{convert_backend_type(result[0]['backendType'])}: {result[0]['name']} | {result[0]['id']}\n{result[0]['description']}\n{result[0]['rarity']}\n{result[0]['set']}")
                    else:
                        text = str()
                        for count, item in enumerate(result):
                            text += f"\n{count+1} {convert_backend_type(item['backendType'])}: {item['name']} | {item['id']}"
                        text += f"\n{l('enter_to_show_info')}"
                        await reply(message, client, text)
                        client.select[message.author.id] = {
                            "exec": [
                                """\
                                await reply(message, client, f"{convert_backend_type(item['backendType'])}: {item['name']} | {item['id']}\n{item['description']}\n{item['rarity']}\n{item['set']}")""" for item in result
                            ],
                            "variable": [
                                {"item": item} for item in result
                            ]
                        }
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['info']}] [[{commands['info_party']}] / [{commands['item']}] / [{commands['id']}] / [{commands['outfit']}] / [{commands['backpack']}] / [{commands['pickaxe']}] / [{commands['emote']}]]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['pending']:
        try:
            pendings = []
            for pending in client.pending_friends:
                client.add_cache(pending)
                if pending.incoming:
                    pendings.append(pending)
            if args[1] in commands['true']:
                for pending in pendings:
                    try:
                        await pending.accept()
                        await reply(message, client, l('add_friend', f'{str(pending.display_name)} / {pending.id}'))
                    except fortnitepy.HTTPException:
                        if data['loglevel'] == 'debug':
                            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        await reply(message, client, l('error_while_sending_friendrequest'))
                        return
                    except Exception:
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        await reply(message, client, l('error'))
                        return
            elif args[1] in commands['false']:
                for pending in pendings:
                    try:
                        await pending.decline()
                        await reply(message, client, l('friend_request_decline', f'{str(pending.display_name)} / {pending.id}'))
                    except fortnitepy.HTTPException:
                        if data['loglevel'] == 'debug':
                            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        await reply(message, client, l('error_while_declining_friendrequest'))
                        return
                    except Exception:
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                        await reply(message, client, l('error'))
                        return
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['pending']}] [[{commands['true']}] / [{commands['false']}]]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['removepending']:
        try:
            pendings = []
            for pending in client.pending_friends:
                client.add_cache(pending)
                if pending.outgoing:
                    pendings.append(pending)
            for pending in pendings:
                try:
                    await pending.cancel()
                    await reply(message, client, l('remove_pending', f'{str(pending.display_name)} / {pending.id}'))
                except fortnitepy.HTTPException:
                    if data['loglevel'] == 'debug':
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, l('error_while_removing_friendrequest'))
                    return
                except Exception:
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, l('error'))
                    return
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['addfriend']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['addfriend']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and not client.has_friend(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and not client.has_friend(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if not client.has_friend(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache( user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if client.has_friend(user.id):
                    await reply(message, client, l('already_friend'))
                    return
                await client.add_friend(user.id)
                await reply(message, client, l('friend_request_to', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            if client.has_friend(user.id):
                await reply(message, client, l('already_friend'))
                return
            await client.add_friend(user.id)
            await reply(message, client, l('friend_request_to', f'{name(user)}'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_sending_friendrequest'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_send_friendrequest')}"
                await reply(message, client, text)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_sending_friendrequest'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['removefriend']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['removefriend']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.has_friend(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.has_friend(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.has_friend(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if not client.has_friend(user.id):
                    await reply(message, client, l('not_friend_with_user'))
                    return
                await client.remove_or_decline_friend(user.id)
                await reply(message, client, l('remove_friend', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            if not client.has_friend(user.id):
                await reply(message, client, l('not_friend_with_user'))
                return
            await client.remove_or_decline_friend(user.id)
            await reply(message, client, l('remove_friend', f'{name(user)}'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_removing_friend')""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_remove_friend')}"
                await reply(message, client, text)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_removing_friend'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['removeallfriend']:
        try:
            friend_count = len(client.friends)
            await client.remove_all_friends()
            await reply(message, client, l('remove_allfriend',friend_count))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_removing_friend'))
        except Exception:
            send(name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['remove_offline_for']:
        try:
            kwargs = {}
            kwargs["days"] = int(args[1])
            kwargs["hours"] = int(args[2]) if args[2:3] else 0
            kwargs["minutes"] = int(args[3]) if args[3:4] else 0
            offline_for = datetime.timedelta(**kwargs)
            utcnow = datetime.datetime.utcnow()
            event = asyncio.Event(loop=loop)
            removed = []  

            async def _(friend: fortnitepy.Friend):
                last_logout = None
                if friend.last_logout:
                    last_logout = friend.last_logout
                elif friend.created_at > client.booted_utc:
                    last_logout = await friend.fetch_last_logout()
                if last_logout and ((utcnow - last_logout) > offline_for): 
                    if event.is_set():
                        await event.wait()
                    try:
                        await friend.remove()
                    except fortnitepy.HTTPException as e:
                        if e.message_code != "errors.com.epicgames.common.throttled":
                            raise
                        if "Operation access is limited by throttling policy" not in e.message:
                            raise
                        event.set()
                        await asyncio.sleep(int(e.message_vars[0]) + 1)
                        await friend.remove()
                        event.clear()
                    removed.append(friend)
            max_worker = 5
            worker = 0
            def dec(*args):
                nonlocal worker
                worker -= 1
                
            tasks = []
            val = len(client.friends)
            for num,friend in enumerate(client.friends):
                if worker >= max_worker:
                    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                worker += 1
                task = loop.create_task(_(friend))
                task.add_done_callback(dec)
                tasks.append(task)
            await asyncio.gather(*tasks)
            await reply(message, client, l('remove_allfriend',len(removed)))
            await asyncio.sleep(2)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_removing_friend'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['remove_offline_for']}] [{l('day')}] [{l('hour')}]({l('optional')}) [{l('minute')}]({l('optional')})")
        except Exception:
            send(name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['acceptpending']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['acceptpending']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.is_pending(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.is_pending(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.is_pending(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if not client.is_pending(user.id):
                    await reply(message, client, l('not_pending_with_user'))
                    return
                await client.accept_friend(user.id)
                await reply(message, client, l('friend_add', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            if not client.is_pending(user.id):
                await reply(message, client, l('not_pending_with_user'))
                return
            await client.accept_friend(user.id)
            await reply(message, client, l('friend_add', f'{name(user)}'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_accepting_friendrequest'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_accept_pending')}"
                await reply(message, client, text)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_accepting_friendrequest'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['declinepending']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['declinepending']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.is_pending(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.is_pending(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.is_pending(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if not client.is_pending(user.id):
                    await reply(message, client, l('nor_pending_with_user'))
                    return
                await client.remove_or_decline_friend(user.id)
                await reply(message, client, l('friend_request_decline', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            if not client.is_pending(user.id):
                await reply(message, client, l('nor_pending_with_user'))
                return
            await client.remove_or_decline_friend(user.id)
            await reply(message, client, l('friend_request_decline', f'{name(user)}'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_declining_friendrequest'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_decline_pending')}"
                await reply(message, client, text)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_declining_friendrequest'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['blockfriend']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['blockfriend']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and not client.is_blocked(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and not client.is_blocked(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if not client.is_blocked(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if client.is_blocked(user.id):
                    await reply(message, client, l('already_block'))
                    return
                await client.block_user(user.id)
                await reply(message, client, l('block_user', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            if client.is_blocked(user.id):
                await reply(message, client, l('already_block'))
                return
            await client.block_user(user.id)
            await reply(message, client, l('block_user', f'{name(user)}'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_blocking_user'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_block_user')}"
                await reply(message, client, text)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_blocking_user'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['unblockfriend']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['unblockfriend']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in jaconv.kata2hira(str(user.display_name).lower()) and user.id != client.user.id and client.is_blocked(user.id)}
            else:
                users = {str(user.display_name): user for user in cache_users.values() if content_ in str(user.display_name) and user.id != client.user.id and client.is_blocked(user.id)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.is_blocked(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                if not client.is_blocked(user.id):
                    await reply(message, client, l('not_block'))
                    return
                await client.unblock_user(user.id)
                await reply(message, client, l('unblock_user', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            if not client.is_blocked(user.id):
                await reply(message, client, l('not_block'))
                return
            await client.unblock_user(user.id)
            await reply(message, client, l('unblock_user', f'{name(user)}'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_unblocking_user'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_unblock_user')}"
                await reply(message, client, text)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_unblocking_user'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['voice']:
        try:
            if args[1] in commands['true']:
                client.voice = True
                await client.enable_voice()
                send(display_name,l('set_to', 'voice', l('on')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                await reply(message, client, l('set_to', 'voice', l('on')))
            elif args[1] in commands['false']:
                client.voice = False
                await client.disable_voice()
                send(display_name,l('set_to', 'voice', l('off')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                await reply(message, client, l('set_to', 'voice', l('off')))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands[key]}] [[{commands['true']}] / [{commands['false']}]]")
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))
        return

    elif args[0] in commands['chatban']:
        try:
            reason = rawcontent.split(' : ')
            if rawcontent == '':
                await reply(message, client, f"[{commands['chatban']}] [{l('name_or_id')}] : [{l('reason')}({l('optional')})]")
                return
            if data['caseinsensitive']:
                users = {str(member.display_name): member for member in client.party.members if content_ in jaconv.kata2hira(str(member.display_name).lower())}
            else:
                users = {str(member.display_name): member for member in client.party.members if content_ in str(member.display_name)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.party.get_member(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                member = client.party.get_member(user.id)
                if not member:
                    await reply(message, client, l('user_not_in_party'))
                    return
                try:
                    await member.chatban(reason[1])
                except IndexError:
                    await member.chatban()
                await reply(message, client, l('chatban_user', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            member = client.party.get_member(user.id)
            if not member:
                await reply(message, client, l('user_not_in_party'))
                return 
            try:
                await member.chatban(reason[1])
            except IndexError:
                await member.chatban()
            await reply(message, client, l('chatban_user', f'{name(user)}'))
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.NotFound:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('user_notfound'))
        except ValueError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('already_chatban'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user, "reason": reason} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_chatban')}"
                await reply(message, client, text)
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.NotFound:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('user_notfound'))
        except ValueError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('already_chatban'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['promote']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['promote']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(member.display_name): member for member in client.party.members if content_ in jaconv.kata2hira(str(member.display_name).lower())}
            else:
                users = {str(member.display_name): member for member in client.party.members if content_ in str(member.display_name)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.party.get_member(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                member = client.party.get_member(user.id)
                if not member:
                    await reply(message, client, l('user_not_in_party'))
                    return
                await member.promote()
                await reply(message, client, l('promote_user', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            member = client.party.get_member(user.id)
            if not member:
                await reply(message, client, l('user_not_in_party'))
                return
            await member.promote()
            await reply(message, client, l('promote_user', f'{name(user)}'))
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('already_party_leader'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_promoting_party_leader'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_promote_user')}"
                await reply(message, client, text)
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('already_party_leader'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_promoting_party_leader'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['kick']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['kick']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(member.display_name): member for member in client.party.members if content_ in jaconv.kata2hira(str(member.display_name).lower())}
            else:
                users = {str(member.display_name): member for member in client.party.members if content_ in str(member.display_name)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.party.get_member(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                member = client.party.get_member(user.id)
                if not member:
                    await reply(message, client, l('user_not_in_party'))
                    return
                await member.kick()
                await reply(message, client, l('kick_user', f'{name(user)}'))
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            member = client.party.get_member(user.id)
            if not member:
                await reply(message, client, l('user_not_in_party'))
                return
            await member.kick()
            await reply(message, client, l('kick_user', f'{name(user)}'))
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('cant_kick_yourself'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_kicking_user'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_kick_user')}"
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.PartyError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('cant_kick_yourself'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_kicking_user'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['hide']:
        try:
            if rawcontent == '':
                await client.hide()
                await reply(message, client, l('hide_all_user'))
            else:
                if data['caseinsensitive']:
                    users = {str(member.display_name): member for member in client.party.members if content_ in jaconv.kata2hira(str(member.display_name).lower())}
                else:
                    users = {str(member.display_name): member for member in client.party.members if content_ in str(member.display_name)}
                try:
                    user = await client.fetch_user(rawcontent)
                    if user:
                        if client.party.get_member(user.id):
                            users[str(user.display_name)] = user
                            client.add_cache(user)
                except fortnitepy.HTTPException:
                    if data['loglevel'] == 'debug':
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, l("error_while_requesting_userinfo"))
                if len(users) > search_max:
                    await reply(message, client, l('too_many_users', str(len(users))))
                    return
                if len(users) == 0:
                    await reply(message, client, l('user_notfound'))
                    return
                if len(users) == 1:
                    user = tuple(users.values())[0]
                    member = client.party.get_member(user.id)
                    if not member:
                        await reply(message, client, l('user_not_in_party'))
                        return
                    await client.hide(member.id)
                    await reply(message, client, l('hide_user', f'{name(user)}'))
                else:
                    client.select[message.author.id] = {
                        "exec": [
                            """\
            try:
                member = client.party.get_member(user.id)
                if not member:
                    await reply(message, client, l('user_not_in_party'))
                    return
                await client.hide(member.id)
                await reply(message, client, l('hide_user', f'{name(user)}'))
            except fortnitepy.Forbidden:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l('not_party_leader'))
            except fortnitepy.NotFound:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l('user_not_in_party'))""" for user in users.values()
                        ],
                        "variable": [
                            {"user": user} for user in users.values()
                        ]
                    }
                    text = str()
                    for count, user in enumerate(users.values()):
                        text += f"\n{count+1} {name(user)}"
                    text += f"\n{l('enter_to_hide_user')}"
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.NotFound:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('user_not_in_party'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['show']:
        try:
            if rawcontent == '':
                await client.show()
                await reply(message, client, l('show_all_user'))
            else:
                if data['caseinsensitive']:
                    users = {str(member.display_name): member for member in client.party.members if content_ in jaconv.kata2hira(str(member.display_name).lower())}
                else:
                    users = {str(member.display_name): member for member in client.party.members if content_ in str(member.display_name)}
                try:
                    user = await client.fetch_user(rawcontent)
                    if user:
                        if client.party.get_member(user.id):
                            users[str(user.display_name)] = user
                            client.add_cache(user)
                except fortnitepy.HTTPException:
                    if data['loglevel'] == 'debug':
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, l("error_while_requesting_userinfo"))
                if len(users) > search_max:
                    await reply(message, client, l('too_many_users', str(len(users))))
                    return
                if len(users) == 0:
                    await reply(message, client, l('user_notfound'))
                    return
                if len(users) == 1:
                    user = tuple(users.values())[0]
                    member = client.party.get_member(user.id)
                    if not member:
                        await reply(message, client, l('user_not_in_party'))
                        return
                    await client.show(member.id)
                    await reply(message, client, l('show_user', f'{name(user)}'))
                else:
                    client.select[message.author.id] = {
                        "exec": [
                            """\
            try:
                member = client.party.get_member(user.id)
                if not member:
                    await reply(message, client, l('user_not_in_party'))
                    return
                await client.show(member.id)
                await reply(message, client, l('show_user', f'{name(user)}'))
            except fortnitepy.Forbidden:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l('not_party_leader'))
            except fortnitepy.NotFound:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l('user_not_in_party'))""" for user in users.values()
                        ],
                        "variable": [
                            {"user": user} for user in users.values()
                        ]
                    }
                    text = str()
                    for count, user in enumerate(users.values()):
                        text += f"\n{count+1} {name(user)}"
                    text += f"\n{l('enter_to_show_user')}"
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except fortnitepy.NotFound:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('user_not_in_party'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['ready']:
        try:
            await client.party.me.set_ready(fortnitepy.ReadyState.READY)
            await reply(message, client, l('set_to', l('readystate'), l('ready')))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['unready']:
        try:
            await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            await reply(message, client, l('set_to', l('readystate'), l('unready')))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['sitout']:
        try:
            await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            await reply(message, client, l('set_to', l('readystate'), l('sitout')))
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['match']:
        try:
            await client.party.me.set_in_match(players_left=int(args[1]) if args[1:2] else 100)
            await reply(message, client, l('set_to', l('matchstate'), l('remaining', args[1] if args[1:2] else "100")))
        except ValueError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('remaining_must_be_between_0_and_255'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['unmatch']:
        try:
            await client.party.me.clear_in_match()
            await reply(message, client, l('set_to', l('matchstate'), l('off')))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['swap']:
        try:
            if rawcontent == '':
                await reply(message, client, f"[{commands['swap']}] [{l('name_or_id')}]")
                return
            if data['caseinsensitive']:
                users = {str(member.display_name): member for member in client.party.members if content_ in jaconv.kata2hira(str(member.display_name).lower())}
            else:
                users = {str(member.display_name): member for member in client.party.members if content_ in str(member.display_name)}
            try:
                user = await client.fetch_user(rawcontent)
                if user:
                    if client.party.get_member(user.id):
                        users[str(user.display_name)] = user
                        client.add_cache(user)
            except fortnitepy.HTTPException:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l("error_while_requesting_userinfo"))
            if len(users) > search_max:
                await reply(message, client, l('too_many_users', str(len(users))))
                return
            if len(users) == 0:
                await reply(message, client, l('user_notfound'))
                return
            if len(users) == 1:
                user = tuple(users.values())[0]
                member = client.party.get_member(user.id)
                if not member:
                    await reply(message, client, l('user_not_in_party'))
                    return
                real_members = client.party.meta.squad_assignments
                assignments = client.visual_members
                await member.swap_position()
                await reply(message, client, l('swap_user', f'{name(user)}'))
                if client.party.me.leader:
                    await asyncio.sleep(0.5)
                    prop = client.party.meta.set_squad_assignments(assignments)
                    await client.party.patch(updated=prop)
                    await asyncio.sleep(2)
                    client.party.meta.set_squad_assignments(real_members)
            else:
                client.select[message.author.id] = {
                    "exec": [
                        """\
        try:
            member = client.party.get_member(user.id)
            if not member:
                await reply(message, client, l('user_not_in_party'))
                return
            real_members = client.party.meta.squad_assignments
            assignments = client.visual_members
            await member.swap_position()
            await reply(message, client, l('swap_user', f'{name(user)}}'))
            if client.party.me.leader:
                await asyncio.sleep(0.5)
                prop = client.party.meta.set_squad_assignments(assignments)
                await client.party.patch(updated=prop)
                client.party.meta.set_squad_assignments(real_members)
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_swapping_user'))""" for user in users.values()
                    ],
                    "variable": [
                        {"user": user} for user in users.values()
                    ]
                }
                text = str()
                for count, user in enumerate(users.values()):
                    text += f"\n{count+1} {name(user)}"
                text += f"\n{l('enter_to_swap_user')}"
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_swapping_user'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['stop']:
        try:
            client.stopcheck = True
            if await client.change_asset(message.author.id, "Emote", ""):
                await reply(message, client, l('stopped'))
            else:
                await reply(message, client, l('locked'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['setenlightenment']:
        try:
            if await client.change_asset(message.author.id, "Outfit", client.party.me.outfit, client.party.me.outfit_variants,(args[1],args[2])) is True:
                await reply(message, client, l('set_to', 'enlightenment', f'{args[1]}, {args[2]}'))
            else:
                await reply(message, client, l('locked'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['setenlightenment']}] [{l('number')}] [{l('number')}]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['addeditems']:
        try:
            async with aiohttp.ClientSession() as session:
                res = await session.get("https://benbotfn.tk/api/v1/newCosmetics")
                res = await res.json()
            flag = False
            items = res["items"]
            for item in items:
                if client.stopcheck:
                    client.stopcheck = False
                    break
                if item["backendType"] in ignoretype:
                    continue
                if await client.change_asset(message.author.id, convert_backend_type(item["backendType"]), item["id"]):
                    if data['loglevel'] == 'normal':
                        await reply(message, client, f"{item['shortDescription']}: {item['name']}")
                    else:
                        await reply(message, client, f"{item['shortDescription']}: {item['name']} | {item['id']}")
                    await asyncio.sleep(5)
            else:
                await reply(message, client, l('all_end', l('addeditem')))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['shopitems']:
        try:
            store = await client.fetch_item_shop()
            items = []
            for item in (store.featured_items
                         + store.daily_items
                         + store.special_featured_items
                         + store.special_daily_items):
                for grant in item.grants:
                    if convert_backend_type(grant["type"]) in ignoretype:
                        continue
                    item = {
                        "id": grant["asset"],
                        "type": convert_to_asset(convert_to_old_type(convert_backend_type(grant["type"]))),
                        "backendType": grant["type"]
                    }
                    items.append(item)
            for item in items:
                if client.stopcheck:
                    client.stopcheck = False
                    break
                if item["backendType"] in ignoretype:
                    continue
                if await client.change_asset(message.author.id, convert_backend_type(item["backendType"]), item["id"]):
                    i = await loop.run_in_executor(None,search_item,data["search-lang"],"id",item["id"],convert_backend_type(item["backendType"]))
                    if i:
                        i = i[0]
                        if data['loglevel'] == 'normal':
                            await reply(message, client, f"{i['shortDescription']}: {i['name']}")
                        else:
                            await reply(message, client, f"{i['shortDescription']}: {i['name']} | {i['id']}")
                    else:
                        await reply(message, client, item["id"])
                    await asyncio.sleep(5)
            else:
                await reply(message, client, l('all_end', l('shopitem')))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif True in [args[0] in commands[key] for key in ("alloutfit", "allbackpack", "allpet", "allpickaxe", "allemote", "allemoji", "alltoy")]:
        type_ = convert_to_type(args[0])
        try:
            if getattr(client,f"{convert_to_old_type(type_)}lock") and client.lock_check(message.author.id):
                await reply(message, client, l('locked'))
                return
            with open(f'items/{type_}_{data["search-lang"]}.json', 'r', encoding='utf-8') as f:
                allitem = json.load(f)
            for item in allitem:
                if client.stopcheck:
                    client.stopcheck = False
                    break
                await client.change_asset(message.author.id, type_, item["id"])
                await asyncio.sleep(2)
            else:
                await reply(message, client, l('all_end', l(convert_to_old_type(type_))))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif True in [args[0] in commands[key] for key in ("cid", "bid", "petcarrier", "pickaxe_id", "eid", "emoji_id", "toy_id", "id")]:
        type_ = convert_to_type(args[0])
        if rawcontent == '':
            await reply(message, client, f"[{commands[convert_to_old_type(type_)]}] [ID]")
            return
        try:
            result = await loop.run_in_executor(None, search_item, data["search-lang"], "id", rawcontent, type_)
            if result is None and data["sub-search-lang"] != data["search-lang"]:
                result = await loop.run_in_executor(None, search_item, data["sub-search-lang"], "id", rawcontent, type_)
            if result is None:
                await reply(message, client, l('item_notfound'))
            else:
                if len(result) > search_max:
                    await reply(message, client, l('too_many_items', str(len(result))))
                    return
                if len(result) == 1:
                    if await client.change_asset(message.author.id, convert_backend_type(result[0]['backendType']), result[0]['id']) is True:
                        if data['loglevel'] == 'normal':
                            await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']}")
                        else:
                            await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']} | {result[0]['id']}")
                    else:
                        await reply(message, client, l('locked'))
                else:
                    text = str()
                    for count, item in enumerate(result):
                        if data['loglevel'] == 'normal':
                            text += f"\n{count+1} {item['shortDescription']}: {item['name']}"
                        else:
                            text += f"\n{count+1} {item['shortDescription']}: {item['name']} | {item['id']}"
                    text += f"\n{l('enter_to_change_asset')}"
                    await reply(message, client, text)
                    client.select[message.author.id] = {
                        "exec": [
                            """\
                            if await client.change_asset(message.author.id, convert_backend_type(item['backendType']), item['id']) is True:
                                if data['loglevel'] == 'normal':
                                    await reply(message, client, f"{item['shortDescription']}: {item['name']}")
                                else:
                                    await reply(message, client, f"{item['shortDescription']}: {item['name']} | {item['id']}")
                            else:
                                await reply(message, client, l('locked'))""" for item in result
                        ],
                        "variable": [
                            {"item": item} for item in result
                        ]
                    }
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif True in [args[0] in commands[key] for key in ("outfit", "backpack", "pet", "pickaxe", "emote", "emoji", "toy", "item")]:
        type_ = convert_to_type(args[0])
        if rawcontent == '':
            await reply(message, client, f"[{commands[convert_to_old_type(type_)]}] [{l('itemname')}]")
            return
        try:
            result = await loop.run_in_executor(None, search_item, data["search-lang"], "name", rawcontent, type_)
            if result is None and data["sub-search-lang"] != data["search-lang"]:
                result = await loop.run_in_executor(None, search_item, data["sub-search-lang"], "name", rawcontent, type_)
            if result is None:
                await reply(message, client, l('item_notfound'))
            else:
                if len(result) > search_max:
                    await reply(message, client, l('too_many_items', str(len(result))))
                    return
                if len(result) == 1:
                    if await client.change_asset(message.author.id, convert_backend_type(result[0]['backendType']), result[0]['id']) is True:
                        if data['loglevel'] == 'normal':
                            await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']}")
                        else:
                            await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']} | {result[0]['id']}")
                    else:
                        await reply(message, client, l('locked'))
                else:
                    text = str()
                    for count, item in enumerate(result):
                        if data['loglevel'] == 'normal':
                            text += f"\n{count+1} {item['shortDescription']}: {item['name']}"
                        else:
                            text += f"\n{count+1} {item['shortDescription']}: {item['name']} | {item['id']}"
                    text += f"\n{l('enter_to_change_asset')}"
                    await reply(message, client, text)
                    client.select[message.author.id] = {
                        "exec": [
                            """\
                            if await client.change_asset(message.author.id, convert_backend_type(item['backendType']), item['id']) is True:
                                if data['loglevel'] == 'normal':
                                    await reply(message, client, f"{item['shortDescription']}: {item['name']}")
                                else:
                                    await reply(message, client, f"{item['shortDescription']}: {item['name']} | {item['id']}")
                            else:
                                await reply(message, client, l('locked'))""" for item in result
                        ],
                        "variable": [
                            {"item": item} for item in result
                        ]
                    }
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['set']:
        if rawcontent == '':
            await reply(message, client, f"[{commands['set']}] [{l('setname')}]")
            return
        try:
            result = await loop.run_in_executor(None, search_item, data["search-lang"], "set", rawcontent)
            if result is None and data["sub-search-lang"] != data["search-lang"]:
                result = await loop.run_in_executor(None, search_item, data["sub-search-lang"], "set", rawcontent)
            if result is None:
                await reply(message, client, l('item_notfound'))
            else:
                if len(result) > search_max:
                    await reply(message, client, l('too_many_items', str(len(result))))
                    return
                if len(result) == 1:
                    if await client.change_asset(message.author.id, convert_backend_type(result[0]["backendType"]), result[0]['id']) is True:
                        if data['loglevel'] == 'normal':
                            await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']} | {result[0]['set']}")
                        else:
                            await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']} | {result[0]['id']}({result[0]['set']})")
                    else:
                        await reply(message, client, l('locked'))
                else:
                    text = str()
                    for count, item in enumerate(result):
                        if data['loglevel'] == 'normal':
                            text += f"\n{count+1} {item['shortDescription']}: {item['name']} | {result[0]['set']}"
                        else:
                            text += f"\n{count+1} {item['shortDescription']}: {item['name']} | {item['id']}({result[0]['set']})"
                    text += f"\n{l('enter_to_change_asset')}"
                    await reply(message, client, text)
                    client.select[message.author.id] = {
                        "exec": [
                            """\
                            if await client.change_asset(message.author.id, convert_backend_type(item["backendType"]), item['id']) is True:
                                if data['loglevel'] == 'normal':
                                    await reply(message, client, f"{item['shortDescription']}: {item['name']} | {item['set']}")
                                else:
                                    await reply(message, client, f"{item['shortDescription']}: {item['name']} | {item['id']}({item['set']})")
                            else:
                                await reply(message, client, l('locked'))""" for item in result
                        ],
                        "variable": [
                            {"item": item}
                        ]
                    }
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['setstyle']:
        try:
            if True not in [args[1] in commands[key] for key in ("outfit", "backpack", "pickaxe")]:
                await reply(message, client, f"[{commands['setstyle']}] [[{commands['outfit']}] / [{commands['backpack']}] / [{commands['pickaxe']}]]")
                return
            type_ = convert_to_asset(args[1])
            id_ = member_asset(client.party.me, type_)
            type_ = convert_to_new_type(type_)
            if type_ == "Back Bling" and (id_.startswith("pet_carrier_") or id_.startswith("pet_")):
                type_ = "Pet"
            result = await loop.run_in_executor(None, search_style, data["search-lang"], id_, type_)
            if result is None:
                await reply(message, client, l('no_stylechange'))
            else:
                text = str()
                for count, item in enumerate(result):
                    text += f"\n{count+1} {item['name']}"
                text += f"\n{l('enter_to_set_style')}"
                await reply(message, client, text)
                client.select[message.author.id] = {"exec": [f"await client.change_asset('{message.author.id}', '{type_}', '{id_}', {variants['variants']})" for variants in result]}
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['setstyle']}] [[{commands['outfit']}] / [{commands['backpack']}] / [{commands['pet']}] / [{commands['pickaxe']}]]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['addstyle']:
        try:
            if True not in [args[1] in commands[key] for key in ("outfit", "backpack", "pickaxe")]:
                await reply(message, client, f"[{commands['addstyle']}] [[{commands['outfit']}] / [{commands['backpack']}] / [{commands['pickaxe']}]]")
                return
            type_ = convert_to_asset(args[1])
            id_ = member_asset(client.party.me, type_)
            variants_ = eval(f"client.party.me.{type_}_variants")
            type_ = convert_to_new_type(type_)
            if type_ == "Back Bling" and (id_.startswith("pet_carrier_") or id_.startswith("pet_")):
                type_ = "Pet"
            result = await loop.run_in_executor(None, search_style, data["search-lang"], id_, type_)
            if result is None:
                await reply(message, client, l('no_stylechange'))
            else:
                text = str()
                for count, item in enumerate(result):
                    text += f"\n{count+1} {item['name']}"
                text += f"\n{l('enter_to_set_style')}"
                await reply(message, client, text)
                client.select[message.author.id] = {"exec": [f"await client.change_asset('{message.author.id}', '{type_}', '{id_}', {variants_} + {variants['variants']})" for variants in result]}
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['addstyle']}] [[{commands['outfit']}] / [{commands['backpack']}] / [{commands['pet']}] / [{commands['pickaxe']}]]")
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['setvariant']:
        try:
            if True not in [args[1] in commands[key] for key in ("outfit", "backpack", "pet", "pickaxe")]:
                await reply(message, client, f"[{commands['setvariant']}] [[{commands['outfit']}] / [{commands['backpack']}] / [{commands['pet']}] / [{commands['pickaxe']}]]")
                return
            variantdict={}
            for count,text in enumerate(args[2:]):
                if count % 2 != 0:
                    continue
                try:
                    variantdict[text]=args[count+3]
                except IndexError:
                    break
            type_ = convert_to_type(args[1])
            id_ = member_asset(client.party.me, convert_to_asset(args[1]))
            variants = client.party.me.create_variants(item='AthenaCharacter', enlightenment=enlightenment, **variantdict)
            type_ = convert_to_new_type(type_)
            if type_ == "Back Bling" and (id_.startswith("pet_carrier_") or id_.startswith("pet_")):
                type_ = "Pet"
            if await client.change_asset(message.author.id, type_, id_, variants, client.party.me.enlightenments) is False:
                await reply(message, client, l('locked'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['setvariant']}] [ID] [variant] [{l('number')}]")
        except Exception:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0] in commands['addvariant']:
        try:
            if True not in [args[1] in commands[key] for key in ("outfit", "backpack", "pet", "pickaxe")]:
                await reply(message, client, f"[{commands['addvariant']}] [[{commands['outfit']}] / [{commands['backpack']}] / [{commands['pet']}] / [{commands['pickaxe']}]]")
                return
            variantdict={}
            for count,text in enumerate(args[2:]):
                if count % 2 != 0:
                    continue
                try:
                    variantdict[text]=args[count+3]
                except IndexError:
                    break
            type_ = convert_to_type(args[1])
            id_ = member_asset(client.party.me, convert_to_asset(args[1]))
            variants = client.party.me.create_variants(item='AthenaCharacter', enlightenment=enlightenment, **variantdict)
            variants += eval(f"client.party.me.{convert_to_asset(args[1])}_variants")
            type_ = convert_to_new_type(type_)
            if type_ == "Back Bling" and (id_.startswith("pet_carrier_") or id_.startswith("pet_")):
                type_ = "Pet"
            if await client.change_asset(message.author.id, type_, id_, variants, client.party.me.enlightenments) is False:
                await reply(message, client, l('locked'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except IndexError:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, f"[{commands['addvariant']}] [ID] [variant] [{l('number')}]")
        except Exception:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif True in [args[0].lower().startswith(id_) for id_ in ("cid_", "bid_", "petcarrier_", "pickaxe_id_", "eid_", "emoji_", "toy_")]:
        try:
            type_ = convert_to_type(args[0])
            if not await client.change_asset(message.author.id, type_, args[0]):
                await reply(message, client, l('locked'))
        except fortnitepy.HTTPException:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error_while_changing_asset'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    elif args[0].lower().startswith('playlist_'):
        try:
            await client.party.set_playlist(args[0])
            await reply(message, client, l('set_playlist', args[0]))
            data['fortnite']['playlist']=args[0]
        except fortnitepy.Forbidden:
            if data['loglevel'] == 'debug':
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('not_party_leader'))
        except Exception:
            send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await reply(message, client, l('error'))

    else:
        keys = {
            "outfitmimic": ["outfitmimic", l('mimic', l("outfit"))],
            "backpackmimic": ["backpackmimic", l('mimic', l("backpack"))],
            "pickaxemimic": ["pickaxemimic", l('mimic', l("pickaxe"))],
            "emotemimic": ["emotemimic", l('mimic', l("emote"))]
        }
        for key,value in keys.items():
            if args[0] in commands[key]:
                try:
                    if args[1] in commands['true']:
                        setattr(client,value[0],True)
                        send(display_name,l('set_to', value[1], l('on')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                        await reply(message, client, l('set_to', value[1], l('on')))
                    elif args[1] in commands['false']:
                        setattr(client,value[0],False)
                        send(display_name,l('set_to', value[1], l('off')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                        await reply(message, client, l('set_to', value[1], l('off')))
                    else:
                        if data['caseinsensitive']:
                            users = {str(user.display_name): user for user in client.party.members if content_ in jaconv.kata2hira(str(user.display_name).lower())}
                        else:
                            users = {str(user.display_name): user for user in client.party.members if content_ in str(user.display_name)}
                        try:
                            user = await client.fetch_user(rawcontent)
                            if user:
                                users[str(user.display_name)] = user
                                client.add_cache(user)
                        except fortnitepy.HTTPException:
                            if data['loglevel'] == 'debug':
                                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                            await reply(message, client, l("error_while_requesting_userinfo"))
                        if len(users) > search_max:
                            await reply(message, client, l('too_many_users', str(len(users))))
                            return
                        if len(users) == 0:
                            await reply(message, client, l('user_notfound'))
                            return
                        if len(users) == 1:
                            user = tuple(users.values())[0]
                            setattr(client,value[0],user.id)
                            send(display_name,l('set_to', value[1], l('off')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                            await reply(message, client, l('set_to', value[1], name(user)))
                        else:
                            client.select[message.author.id] = {
                                "exec": [
                                    """\
                                        setattr(client,value[0],user.id)
                                        send(display_name,l('set_to', value[1], l('off')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                                        await reply(message, client, l('set_to', value[1], name(user)))""" for user in users.values()
                                ],
                                "variable": [
                                    {"user": user, "value": value} for user in users.values()
                                ]
                            }
                            text = str()
                            for count, user in enumerate(users.values()):
                                text += f"\n{count+1} {name(user)}"
                            text += f"\n{l('enter_to_mimic_user')}"
                            await reply(message, client, text)
                except IndexError:
                    if data['loglevel'] == 'debug':
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, f"[{commands[key]}] [[{commands['true']}] / [{commands['false']}] / {l('name_or_id')}]")
                except Exception:
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, l('error'))
                return

        keys = {
            "outfitlock": ["outfitlock", l('lock', l("outfit"))],
            "backpacklock": ["backpacklock", l('lock', l("backpack"))],
            "pickaxelock": ["pickaxelock", l('lock', l("pickaxe"))],
            "emotelock": ["emotelock", l('lock', l("emote"))],
            "whisper": ["whisper", l('command_from', l('whisper'))],
            "partychat": ["partychat", l('command_from', l('partychat'))],
            "discord": ["discord", l('command_from', l('discord'))],
            "web": ["web", l('command_from', l('web'))],
            "disablewhisperperfectly": ["whisperperfect", l('disable_perfect', l('whisper'))],
            "disablepartychatperfectly": ["partychatperfect", l('disable_perfect', l('partychat'))],
            "disablediscordperfectly": ["discordperfect", l('disable_perfect', l('discord'))],
            "acceptinvite": ["acceptinvite", l('invite')],
            "acceptfriend": ["acceptfriend", l('friend_request')],
            "joinmessageenable": ["joinmessageenable", l('join_', l('message'))],
            "randommessageenable": ["randommessageenable", l('join_', l('randommessage'))]
        }
        for key,value in keys.items():
            if args[0] in commands[key]:
                try:
                    if args[1] in commands['true']:
                        setattr(client,value[0],True)
                        send(display_name,l('set_to', value[1], l('on')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                        await reply(message, client, l('set_to', value[1], l('on')))
                    elif args[1] in commands['false']:
                        setattr(client,value[0],False)
                        send(display_name,l('set_to', value[1], l('off')),add_p=lambda x:f'[{now()}] [{client.user.display_name}] {x}')
                        await reply(message, client, l('set_to', value[1], l('off')))
                except IndexError:
                    if data['loglevel'] == 'debug':
                        send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, f"[{commands[key]}] [[{commands['true']}] / [{commands['false']}]]")
                except Exception:
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    await reply(message, client, l('error'))
                return


        if ': ' in message.content:
            return
        if content.isdigit() and client.select.get(message.author.id):
            try:
                if int(args[0]) == 0:
                    await reply(message, client, l('please_enter_valid_number'))
                    return
                exec_ = client.select[message.author.id]["exec"][int(args[0])-1]
                variable = globals()
                variable.update(locals())
                if client.select[message.author.id].get("variable"):
                    variable.update(client.select[message.author.id]["variable"][int(args[0])-1])
                await aexec(exec_, variable)
            except IndexError:
                if data['loglevel'] == 'debug':
                    send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l('please_enter_valid_number'))
            except Exception:
                send(display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                await reply(message, client, l('error'))
        else:
            if do_itemsearch:
                result = await loop.run_in_executor(None, search_item, data["search-lang"], "name", content, "Item")
                if not result and data["sub-search-lang"] != data["search-lang"]:
                    result = await loop.run_in_executor(None, search_item, data["sub-search-lang"], "name", content, "Item")
                if result:
                    if len(result) > search_max:
                        await reply(message, client, l('too_many_items', str(len(result))))
                        return
                    if len(result) == 1:
                        if await client.change_asset(message.author.id, convert_backend_type(result[0]["backendType"]), result[0]['id']) is True:
                            if data['loglevel'] == 'normal':
                                await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']}")
                            else:
                                await reply(message, client, f"{result[0]['shortDescription']}: {result[0]['name']} | {result[0]['id']}")
                        else:
                            await reply(message, client, l('locked'))
                    else:
                        text = str()
                        for count, item in enumerate(result):
                            if data['loglevel'] == 'normal':
                                text += f"\n{count+1} {item['shortDescription']}: {item['name']}"
                            else:
                                text += f"\n{count+1} {item['shortDescription']}: {item['name']} | {item['id']}"
                        text += f"\n{l('enter_to_change_asset')}"
                        await reply(message, client, text)
                        client.select[message.author.id] = {
                            "exec": [
                                """\
                                    if await client.change_asset(message.author.id, convert_backend_type(item["backendType"]), item['id']) is True:
                                        if data['loglevel'] == 'normal':
                                            await reply(message, client, f"{item['shortDescription']}: {item['name']}")
                                        else:
                                            await reply(message, client, f"{item['shortDescription']}: {item['name']} | {item['id']}")
                                    else:
                                        await reply(message, client, l('locked'))""" for item in result
                            ],
                            "variable": [
                                {"item": item} for item in result
                            ]
                        }

#========================================================================================================================
#========================================================================================================================
#========================================================================================================================
#========================================================================================================================
#========================================================================================================================

bot_ready = True
first_boot = True
filename = 'device_auths.json'
web_text = ''
cache_users = {}
cache_items = {}
cache_banners = {}
client_name = {}
ignoretype = [
    "Contrail",
    "Glider",
    "Wrap",
    "Loading Screen",
    "Music",
    "Spray",
    "Battle Bus"
]
clients = []
loadedclients = []
whitelist = []
whitelist_ = []
blacklist = []
blacklist_ = []
otherbotlist = []
storedlogs = []
format_pattern = re.compile(r"""\{(.*?)\}""")

config_tags={
    "['fortnite']": [dict],
    "['fortnite']['email']": [str,"can_be_multiple"],
    "['fortnite']['owner']": [str,"can_be_multiple"],
    "['fortnite']['platform']": [str,"select_platform"],
    "['fortnite']['outfit']": [str],
    "['fortnite']['outfit_style']": [str],
    "['fortnite']['backpack']": [str],
    "['fortnite']['backpack_style']": [str],
    "['fortnite']['pickaxe']": [str],
    "['fortnite']['pickaxe_style']": [str],
    "['fortnite']['emote']": [str],
    "['fortnite']['playlist']": [str],
    "['fortnite']['banner']": [str],
    "['fortnite']['banner_color']": [str],
    "['fortnite']['avatar_id']": [str],
    "['fortnite']['avatar_color']": [str,"can_linebreak"],
    "['fortnite']['level']": [int],
    "['fortnite']['tier']": [int],
    "['fortnite']['xpboost']": [int],
    "['fortnite']['friendxpboost']": [int],
    "['fortnite']['privacy']": [str,"select_privacy"],
    "['fortnite']['whisper']": [bool_,"select_bool"],
    "['fortnite']['partychat']": [bool_,"select_bool"],
    "['fortnite']['disablewhisperperfectly']": [bool_,"select_bool"],
    "['fortnite']['disablepartychatperfectly']": [bool_,"select_bool"],
    "['fortnite']['ignorebot']": [bool_,"select_bool"],
    "['fortnite']['joinmessageenable']": [bool_,"select_bool"],
    "['fortnite']['randommessageenable']": [bool_,"select_bool"],
    "['fortnite']['joinemote']": [bool_,"select_bool"],
    "['fortnite']['click_invite']": [bool_,"select_bool"],
    "['fortnite']['disable_voice']": [bool_,"select_bool"],
    "['fortnite']['outfitmimic']": [bool_,"select_bool"],
    "['fortnite']['backpackmimic']": [bool_,"select_bool"],
    "['fortnite']['pickaxemimic']": [bool_,"select_bool"],
    "['fortnite']['emotemimic']": [bool_,"select_bool"],
    "['fortnite']['mimic-ignorebot']": [bool_,"select_bool"],
    "['fortnite']['mimic-ignoreblacklist']": [bool_,"select_bool"],
    "['fortnite']['outfitlock']": [bool_,"select_bool"],
    "['fortnite']['backpacklock']": [bool_,"select_bool"],
    "['fortnite']['pickaxelock']": [bool_,"select_bool"],
    "['fortnite']['emotelock']": [bool_,"select_bool"],
    "['fortnite']['acceptinvite']": [bool_,"select_bool"],
    "['fortnite']['acceptfriend']": [bool_none,"select_bool_none"],
    "['fortnite']['addfriend']": [bool_,"select_bool"],
    "['fortnite']['invite-ownerdecline']": [bool_,"select_bool"],
    "['fortnite']['inviteinterval']": [bool_,"select_bool"],
    "['fortnite']['interval']": [int],
    "['fortnite']['waitinterval']": [int],
    "['fortnite']['hide-user']": [bool_,"select_bool"],
    "['fortnite']['hide-blacklist']": [bool_,"select_bool"],
    "['fortnite']['show-owner']": [bool_,"select_bool"],
    "['fortnite']['show-whitelist']": [bool_,"select_bool"],
    "['fortnite']['show-bot']": [bool_,"select_bool"],
    "['fortnite']['blacklist']": [str,"can_be_multiple"],
    "['fortnite']['blacklist-declineinvite']": [bool_,"select_bool"],
    "['fortnite']['blacklist-autoblock']": [bool_,"select_bool"],
    "['fortnite']['blacklist-autokick']": [bool_,"select_bool"],
    "['fortnite']['blacklist-autochatban']": [bool_,"select_bool"],
    "['fortnite']['blacklist-ignorecommand']": [bool_,"select_bool"],
    "['fortnite']['whitelist']": [str,"can_be_multiple"],
    "['fortnite']['whitelist-allowinvite']": [bool_,"select_bool"],
    "['fortnite']['whitelist-declineinvite']": [bool_,"select_bool"],
    "['fortnite']['whitelist-ignorelock']": [bool_,"select_bool"],
    "['fortnite']['whitelist-ownercommand']": [bool_,"select_bool"],
    "['fortnite']['whitelist-ignoreng']": [bool_,"select_bool"],
    "['fortnite']['invitelist']": [str,"can_be_multiple"],
    "['fortnite']['otherbotlist']": [str,"can_be_multiple"],
    "['discord']": [dict],
    "['discord']['enabled']": [bool_,"select_bool"],
    "['discord']['token']": [str],
    "['discord']['owner']": [int,"can_be_multiple"],
    "['discord']['channels']": [str,"can_be_multiple"],
    "['discord']['status']": [str],
    "['discord']['status_type']": [str,"select_status"],
    "['discord']['discord']": [bool_,"select_bool"],
    "['discord']['disablediscordperfectly']": [bool_,"select_bool"],
    "['discord']['ignorebot']": [bool_,"select_bool"],
    "['discord']['blacklist']": [str,"can_be_multiple"],
    "['discord']['blacklist-ignorecommand']": [bool_,"select_bool"],
    "['discord']['whitelist']": [str,"can_be_multiple"],
    "['discord']['whitelist-ignorelock']": [bool_,"select_bool"],
    "['discord']['whitelist-ownercommand']": [bool_,"select_bool"],
    "['discord']['whitelist-ignoreng']": [bool_,"select_bool"],
    "['web']": [dict],
    "['web']['enabled']": [bool_,"select_bool"],
    "['web']['ip']": [str],
    "['web']['port']": [int],
    "['web']['password']": [str],
    "['web']['login_required']": [bool_,"select_bool"],
    "['web']['web']": [bool_,"select_bool"],
    "['web']['log']": [bool_,"select_bool"],
    "['replies-matchmethod']": [str,"select_matchmethod"],
    "['ng-words']": [str,"can_be_multiple"],
    "['ng-word-matchmethod']": [str,"select_matchmethod"],
    "['ng-word-kick']": [bool_,"select_bool"],
    "['ng-word-chatban']": [bool_,"select_bool"],
    "['ng-word-blacklist']": [bool_,"select_bool"],
    "['restart_in']": [int],
    "['search_max']": [int],
    "['lang']": [str,"select_lang"],
    "['search-lang']": [str,"select_ben_lang"],
    "['sub-search-lang']": [str,"select_ben_lang"],
    "['no-logs']": [bool_,"select_bool"],
    "['ingame-error']": [bool_,"select_bool"],
    "['discord-log']": [bool_,"select_bool"],
    "['omit-over2000']": [bool_,"select_bool"],
    "['skip-if-overflow']": [bool_,"select_bool"],
    "['hide-email']": [bool_,"select_bool"],
    "['hide-token']": [bool_,"select_bool"],
    "['hide-webhook']": [bool_,"select_bool"],
    "['webhook']": [str],
    "['caseinsensitive']": [bool_,"select_bool"],
    "['loglevel']": [str,"select_loglevel"],
    "['debug']": [bool_,"select_bool"]
}
config_tags_raw = copy.deepcopy(config_tags)
commands_tags={
    "['usercommands']": [str,"can_be_multiple"],
    "['true']": [str,"can_be_multiple"],
    "['false']": [str,"can_be_multiple"],
    "['me']": [str,"can_be_multiple"],
    "['prev']": [str,"can_be_multiple"],
    "['eval']": [str,"can_be_multiple"],
    "['exec']": [str,"can_be_multiple"],
    "['restart']": [str,"can_be_multiple"],
    "['relogin']": [str,"can_be_multiple"],
    "['reload']": [str,"can_be_multiple"],
    "['addblacklist']": [str,"can_be_multiple"],
    "['removeblacklist']": [str,"can_be_multiple"],
    "['addwhitelist']": [str,"can_be_multiple"],
    "['removewhitelist']": [str,"can_be_multiple"],
    "['addblacklist_discord']": [str,"can_be_multiple"],
    "['removeblacklist_discord']": [str,"can_be_multiple"],
    "['addwhitelist_discord']": [str,"can_be_multiple"],
    "['removewhitelist_discord']": [str,"can_be_multiple"],
    "['addinvitelist']": [str,"can_be_multiple"],
    "['removeinvitelist']": [str,"can_be_multiple"],
    "['get']": [str,"can_be_multiple"],
    "['friendcount']": [str,"can_be_multiple"],
    "['pendingcount']": [str,"can_be_multiple"],
    "['blockcount']": [str,"can_be_multiple"],
    "['friendlist']": [str,"can_be_multiple"],
    "['pendinglist']": [str,"can_be_multiple"],
    "['blocklist']": [str,"can_be_multiple"],
    "['outfitmimic']": [str,"can_be_multiple"],
    "['backpackmimic']": [str,"can_be_multiple"],
    "['pickaxemimic']": [str,"can_be_multiple"],
    "['emotemimic']": [str,"can_be_multiple"],
    "['whisper']": [str,"can_be_multiple"],
    "['partychat']": [str,"can_be_multiple"],
    "['discord']": [str,"can_be_multiple"],
    "['web']": [str,"can_be_multiple"],
    "['disablewhisperperfectly']": [str,"can_be_multiple"],
    "['disablepartychatperfectly']": [str,"can_be_multiple"],
    "['disablediscordperfectly']": [str,"can_be_multiple"],
    "['acceptinvite']": [str,"can_be_multiple"],
    "['acceptfriend']": [str,"can_be_multiple"],
    "['joinmessageenable']": [str,"can_be_multiple"],
    "['randommessageenable']": [str,"can_be_multiple"],
    "['wait']": [str,"can_be_multiple"],
    "['join']": [str,"can_be_multiple"],
    "['joinid']": [str,"can_be_multiple"],
    "['leave']": [str,"can_be_multiple"],
    "['invite']": [str,"can_be_multiple"],
    "['inviteall']": [str,"can_be_multiple"],
    "['message']": [str,"can_be_multiple"],
    "['partymessage']": [str,"can_be_multiple"],
    "['sendall']": [str,"can_be_multiple"],
    "['status']": [str,"can_be_multiple"],
    "['avatar']": [str,"can_be_multiple"],
    "['banner']": [str,"can_be_multiple"],
    "['level']": [str,"can_be_multiple"],
    "['bp']": [str,"can_be_multiple"],
    "['privacy']": [str,"can_be_multiple"],
    "['privacy_public']": [str,"can_be_multiple"],
    "['privacy_friends_allow_friends_of_friends']": [str,"can_be_multiple"],
    "['privacy_friends']": [str,"can_be_multiple"],
    "['privacy_private_allow_friends_of_friends']": [str,"can_be_multiple"],
    "['privacy_private']": [str,"can_be_multiple"],
    "['getuser']": [str,"can_be_multiple"],
    "['getfriend']": [str,"can_be_multiple"],
    "['getpending']": [str,"can_be_multiple"],
    "['getblock']": [str,"can_be_multiple"],
    "['info']": [str,"can_be_multiple"],
    "['info_party']": [str,"can_be_multiple"],
    "['pending']": [str,"can_be_multiple"],
    "['removepending']": [str,"can_be_multiple"],
    "['addfriend']": [str,"can_be_multiple"],
    "['removefriend']": [str,"can_be_multiple"],
    "['removeallfriend']": [str,"can_be_multiple"],
    "['remove_offline_for']": [str,"can_be_multiple"],
    "['acceptpending']": [str,"can_be_multiple"],
    "['declinepending']": [str,"can_be_multiple"],
    "['blockfriend']": [str,"can_be_multiple"],
    "['unblockfriend']": [str,"can_be_multiple"],
    "['voice']": [str,"can_be_multiple"],
    "['chatban']": [str,"can_be_multiple"],
    "['promote']": [str,"can_be_multiple"],
    "['kick']": [str,"can_be_multiple"],
    "['hide']": [str,"can_be_multiple"],
    "['show']": [str,"can_be_multiple"],
    "['ready']": [str,"can_be_multiple"],
    "['unready']": [str,"can_be_multiple"],
    "['sitout']": [str,"can_be_multiple"],
    "['match']": [str,"can_be_multiple"],
    "['unmatch']": [str,"can_be_multiple"],
    "['swap']": [str,"can_be_multiple"],
    "['outfitlock']": [str,"can_be_multiple"],
    "['backpacklock']": [str,"can_be_multiple"],
    "['pickaxelock']": [str,"can_be_multiple"],
    "['emotelock']": [str,"can_be_multiple"],
    "['stop']": [str,"can_be_multiple"],
    "['addeditems']": [str,"can_be_multiple"],
    "['shopitems']": [str,"can_be_multiple"],
    "['alloutfit']": [str,"can_be_multiple"],
    "['allbackpack']": [str,"can_be_multiple"],
    "['allpet']": [str,"can_be_multiple"],
    "['allpickaxe']": [str,"can_be_multiple"],
    "['allemote']": [str,"can_be_multiple"],
    "['allemoji']": [str,"can_be_multiple"],
    "['alltoy']": [str,"can_be_multiple"],
    "['cid']": [str,"can_be_multiple"],
    "['bid']": [str,"can_be_multiple"],
    "['petcarrier']": [str,"can_be_multiple"],
    "['pickaxe_id']": [str,"can_be_multiple"],
    "['eid']": [str,"can_be_multiple"],
    "['emoji_id']": [str,"can_be_multiple"],
    "['toy_id']": [str,"can_be_multiple"],
    "['id']": [str,"can_be_multiple"],
    "['outfit']": [str,"can_be_multiple"],
    "['backpack']": [str,"can_be_multiple"],
    "['pet']": [str,"can_be_multiple"],
    "['pickaxe']": [str,"can_be_multiple"],
    "['emote']": [str,"can_be_multiple"],
    "['emoji']": [str,"can_be_multiple"],
    "['toy']": [str,"can_be_multiple"],
    "['item']": [str,"can_be_multiple"],
    "['set']": [str,"can_be_multiple"],
    "['setvariant']": [str,"can_be_multiple"],
    "['addvariant']": [str,"can_be_multiple"],
    "['setstyle']": [str,"can_be_multiple"],
    "['addstyle']": [str,"can_be_multiple"],
    "['setenlightenment']": [str,"can_be_multiple"]
}
error_config = []
error_commands = []

outfit_keys = ("cid", "outfit", "outfitmimic", "outfitlock", "alloutfit")
backpack_keys = ("bid", "backpack", "backpackmimic", "backpacklock", "allbackpack")
pet_keys = ("petcarrier", "pet", "allpet")
pickaxe_keys = ("pickaxe_id", "pickaxe", "pickaxemimic", "pickaxelock", "allpickaxe")
emote_keys = ("eid", "emote", "emotemimic", "emotelock", "allemote")
emoji_keys = ("emoji_id", "emoji", "allemoji")
toy_keys = ("toy_id", "toy", "alltoy")
item_keys = ("id", "item")

app = Sanic(__name__)
app.secret_key = os.urandom(32)
app.static('/images', './templates/images')
env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'), extensions=['jinja2.ext.do'])
auth = LoginManager()

fortnitepy_auth = fortnitepy.Auth()
launcher_token = fortnitepy_auth.ios_token
fortnite_token = fortnitepy_auth.fortnite_token
oauth_url = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token"
fortnite_token_url = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token"
exchange_auth_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
device_auth_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/deviceAuthorization"
exchange_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
user_lookup_url = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{user_id}"


if not load_config():
    sys.exit(1)
if error_config or error_commands:
    bot_ready = False
for key in error_config:
    config_tags[key].append("fix_required")
for key in error_commands:
    commands_tags[key].append("fix_required")
search_max = data["search_max"]

if data['debug']:
    logger = logging.getLogger('fortnitepy.auth')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[36m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)

    logger = logging.getLogger('fortnitepy.http')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[36m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)

    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[35m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)

if os.getcwd().startswith('/app') or os.getcwd().startswith('/home/runner'):
    data['web']['ip'] = "0.0.0.0"
else:
    data['web']['ip'] = data['web']['ip'].format(ip=socket.gethostbyname(socket.gethostname()))

if True:
    send(l('bot'),f'{l("lobbybot")}: gomashio\n{l("credit")}\n{l("library")}: Terbau',cyan)
    text = ""
    if data['loglevel'] == 'normal':
        text += f'\n{l("loglevel")}: {l("normal")}\n'
    elif data['loglevel'] == 'info':
        text += f'\n{l("loglevel")}: {l("info")}\n'
    elif data['loglevel'] == 'debug':
        text += f'\n{l("loglevel")}: {l("debug")}\n'
    if data.get('debug',False) is True:
        text += f'\n{l("debug")}: {l("on")}\n'
    else:
        text += f'\n{l("debug")}: {l("off")}\n'
    text += f'\nPython {platform.python_version()}\n'
    text += f'fortnitepy {fortnitepy.__version__}\n'
    text += f'discord.py {discord.__version__}\n'
    text += f'Sanic {sanic.__version__}\n'
    send(l('bot'),text,green)
    if data.get('debug',False) is True:
        send(l('bot'),f'[{now()}] {l("debug_is_on")}',red)
    send(l('bot'),l("booting"))

dclient = discord.Client()
dclient.owner = []
dclient.isready = False
dclient.boot_time = None
if True: #discord
    @dclient.event
    async def on_ready() -> None:
        loop = asyncio.get_event_loop()
        dclient.boot_time = time.time()
        dclient_user = name(dclient.user)
        send(dclient_user,f"{l('login')}: {dclient_user}",green,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}')
        dclient.isready = True
        loop.create_task(status_loop())

        dclient.owner = []
        for owner in data['discord']['owner']:
            user = dclient.get_user(owner)
            if not user:
                try:
                    user = await dclient.fetch_user(owner)
                except discord.NotFound:
                    if data['loglevel'] == "debug":
                        send(dclient_user,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                except discord.HTTPException:
                    if data['loglevel'] == 'debug':
                        send(dclient_user,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    send(dclient_user,l('error_while_requesting_userinfo'),red,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}',add_d=lambda x:f'>>> {x}')
            if not user:
                send(dclient_user,l('discord_owner_notfound',owner),red,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}',add_d=lambda x:f'>>> {x}')
            else:
                dclient.owner.append(user)
                send(dclient_user,f"{l('owner')}: {name(user)}",green,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}')

        lists = {
            "blacklist_": "blacklist",
            "whitelist_": "whitelist"
        }
        async def _(listuser: str) -> None:
            listuser = int(listuser)
            user = dclient.get_user(listuser)
            if not user:
                try:
                    user = await dclient.fetch_user(listuser)
                except discord.NotFound:
                    if data['loglevel'] == "debug":
                        send(dclient_user,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
                    send(dclient_user,l(f'discord_{data_}_user_notfound', listuser),red,add_p=lambda x:f'[{now()}] [{dclient_user}] {x}',add_d=lambda x:f'>>> {x}')
                    return
            globals()[list_].append(user.id)

        for list_,data_ in lists.items():
            await asyncio.gather(*[_(listuser) for listuser in data['discord'][data_]])
            if data['loglevel'] == "debug":
                send(dclient_user,f"discord {data_}list {globals()[list_]}",yellow,add_d=lambda x:f'```\n{x}\n```')

    @dclient.event
    async def on_message(message: discord.Message) -> None:
        await process_command(message)

    async def change_status() -> None:
        var = defaultdict(lambda: None)

        var.update(
                {
                    "get_client_data": get_client_data,
                    "all_friend_count": sum([len(client_.friends) for client_ in clients]),
                    "all_pending_count": sum([len(client_.pending_friends) for client_ in clients]),
                    "all_block_count": sum([len(client_.blocked_users) for client_ in clients]),
                    "guild_count": len(dclient.guilds),
                    "get_guild_member_count": get_guild_member_count,
                    "boot_time": int(time.time() - dclient.boot_time)
                }
            )
        
        activity = discord.Activity(name=eval_format(data['discord']['status'],var),type=data['discord']['status_type'])
        await dclient.change_presence(activity=activity)

    async def status_loop() -> None:
        while True:
            try:
                await change_status()
            except Exception:
                send(dclient.user.display_name,traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            await asyncio.sleep(30)

select_bool = select(
    [
        {"value": "True","display_value": l('bool_true')},
        {"value": "False","display_value": l('bool_false')}
    ]
)
select_bool_none = select(
    [
        {"value": "True","display_value": l('bool_true')},
        {"value": "False","display_value": l('bool_false')},
        {"value": "None","display_value": l('bool_none')}
    ]
)
select_platform = select(
    [
        {"value": "WIN","display_value": "Windows"},
        {"value": "MAC","display_value": "Mac"},
        {"value": "PSN","display_value": "PlayStation"},
        {"value": "XBL","display_value": "Xbox"},
        {"value": "SWT","display_value": "Switch"},
        {"value": "IOS","display_value": "IOS"},
        {"value": "AND","display_value": "Android"}
    ]
)
select_privacy = select(
    [
        {"value": i,"display_value": l(i)} for i in ["public","friends_allow_friends_of_friends","friends","private_allow_friends_of_friends","private"]
    ]
)
select_status = select(
    [
        {"value": i,"display_value": l(i)} for i in ["playing","listening","watching"]
    ]
)
select_matchmethod = select(
    [
        {"value": i,"display_value": l(i)} for i in ["full","contains","starts","ends"]
    ]
)
select_loglevel = select(
    [
        {"value": "normal","display_value": l('normal')},
        {"value": "info","display_value": l('info')},
        {"value": "debug","display_value": l('debug')}
    ]
)
select_lang = select(
    [
        {"value": re.sub(r"lang(\\|/)","",i).replace(".json",""),"display_value": re.sub(r"lang(\\|/)","",i).replace(".json","")} for i in glob("lang/*.json") if "_old.json" not in i
    ]
)
select_ben_lang = select(
    [
        {"value": i,"display_value": i} for i in ["ar","de","en","es","es-419","fr","it","ja","ko","pl","pt-BR","ru","tr","zh-CN","zh-Hant"]
    ]
)

converter = {
    "can_be_multiple": CanBeMultiple,
    "can_linebreak": CanLinebreak,
    "select_bool": select_bool,
    "select_bool_none": select_bool_none,
    "select_platform": select_platform,
    "select_privacy" :select_privacy,
    "select_status": select_status,
    "select_loglevel": select_loglevel,
    "select_lang": select_lang,
    "select_ben_lang": select_ben_lang,
    "select_matchmethod": select_matchmethod,
    "red": Red,
    "fix_required": FixRequired
}
for key,value in config_tags.items():
    for count,tag in enumerate(value):
        config_tags[key][count] = converter.get(tag,tag)
for key,value in commands_tags.items():
    for count,tag in enumerate(value):
        commands_tags[key][count] = converter.get(tag,tag)

if True: #Web
    @app.route("/favicon.ico", methods=["GET"])
    async def favicon(request: Request):
        return sanic.response.redirect("/images/icon.png")

    if os.environ.get("FORTNITE_LOBBYBOT_STATUS") == "-1":
        @app.route("/", methods=["GET"])
        async def main(request: Request):
            return sanic.response.html(
                "<h2>Fortnite-LobbyBot<h2>"
                "<p>初めに<a href='https://github.com/gomashio1596/Fortnite-LobbyBot/blob/master/README.md' target='_blank'>README</a>をお読みください</p>"
                "<p>First, please read <a href='https://github.com/gomashio1596/Fortnite-LobbyBot/blob/master/README_EN.md' target='_blank'>README<a/></p>"
                "<p>質問などは私(Twitter @gomashio1596 Discord gomashio#4335)か<a href='https://discord.gg/NEnka5N' target='_blank'>Discordサーバー</a>まで</p>"
                "<p>For questions, Contact to me(Twitter @gomashio1596 Discord gomashio#4335) or ask in <a href='https://discord.gg/NEnka5N' target='_blank'>Discord server</a></p>"
                "<p><a href='https://glitch.com/edit/#!/remix/fortnite-lobbybot' target='_blank'>ここをクリック</a>してRemix</p>"
                "<p><a href='https://glitch.com/edit/#!/remix/fortnite-lobbybot' target='_blank'>Click here</a> to Remix</p>"
                "<a href='https://discord.gg/NEnka5N' target='_blank'><img src='https://discordapp.com/api/guilds/718709023427526697/widget.png?style=banner1'></img></a>"
            )
    elif data["status"] == 0:
        @app.route("/", methods=["GET", "POST"])
        async def main(request: Request):
            flash_messages = []
            flash_messages_red = []
            if request.method == "GET":
                data = load_json("config.json")
                return render_template(
                    "config_editor.html",
                    l=l,
                    data=data,
                    config_tags=config_tags,
                    len=len,
                    type=type,
                    can_be_multiple=CanBeMultiple,
                    can_linebreak=CanLinebreak,
                    select=select,
                    str=str,
                    int=int,
                    bool=bool,
                    list=list,
                    map=map,
                    red=Red,
                    fix_required=FixRequired,
                    flash_messages=flash_messages,
                    flash_messages_red=flash_messages_red
                )
            else:
                flag = False
                raw = request.form
                data = load_json("config.json")
                corrected = data
                for key_,tags in config_tags.items():
                    keys = key_.replace("'","").replace("[","").split("]")
                    key = keys[0]
                    nest = len(keys) - 1

                    if nest == 1:
                        if dict in tags:
                            if not corrected.get(key):
                                corrected[key] = {}
                        else:
                            value = raw.get(f"['{key}']")
                        
                        if FixRequired in tags and value == corrected.get(key):
                            flash_messages_red.append(l('this_field_fix_required', key))
                            flag = True
                        if CanBeMultiple in tags:
                            if str in tags:
                                corrected[key] = re.split(r'\r\n|\n',value) if value else []
                            elif int in tags:
                                corrected[key] = [int(i) for i in re.split(r'\r\n|\n',value)] if value else []
                        elif str in tags:
                            corrected[key] = value.replace(r"\\n",r"\n").replace(r"\n","\n") if value else ""
                        elif int in tags:
                            corrected[key] = int(value) if value else 0
                        elif bool_ in tags:
                            corrected[key] = bool_.create(value)
                        elif bool_none in tags:
                            corrected[key] = bool_none.create(value)
                    elif nest == 2:
                        key2 = keys[1]

                        if dict in tags:
                            if not corrected.get(key):
                                if not corrected.get(key).get(key2):
                                    corrected[key][key2] = {}
                        else:
                            value2 = raw.get(f"['{key}']['{key2}']")
                        
                        if FixRequired in tags and value2 == corrected.get(key,{}).get(key2):
                            flash_messages_red.append(l('this_field_fix_required', f"{key}: {key2}"))
                            flag = True
                        if CanBeMultiple in tags:
                            if str in tags:
                                corrected[key][key2] = re.split(r'\r\n|\n',value2) if value2 else []
                            elif int in tags:
                                corrected[key][key2]  = [int(i) for i in re.split(r'\r\n|\n',value2)] if value2 else []
                        elif str in tags:
                            corrected[key][key2]  = value2.replace(r"\\n",r"\n").replace(r"\n","\n") if value2 else ""
                        elif int in tags:
                            corrected[key][key2] = int(value2) if value2 else 0
                        elif bool_ in tags:
                            corrected[key][key2] = bool_.create(value2)
                        elif bool_none in tags:
                            corrected[key][key2] = bool_none.create(value2)
                if flag:
                    return render_template(
                        "config_editor.html",
                        l=l,
                        data=data,
                        config_tags=config_tags,
                        len=len,
                        type=type,
                        can_be_multiple=CanBeMultiple,
                        can_linebreak=CanLinebreak,
                        select=select,
                        str=str,
                        int=int,
                        bool=bool,
                        list=list,
                        map=map,
                        red=Red,
                        fix_required=FixRequired,
                        flash_messages=flash_messages,
                        flash_messages_red=flash_messages_red
                    )
                else:
                    corrected["status"] = 1
                    with open('config.json', 'w', encoding='utf-8') as f:
                        json.dump(corrected, f, ensure_ascii=False, indent=4, sort_keys=False)
                    Thread(target=restart,args=(1,)).start()
                    return sanic.response.redirect("/")
    else:
        @app.route("/", methods=["GET", "POST"])
        async def main(request: Request):
            if request.method == "GET":
                return render_template(
                    "main.html",
                    l=l,
                    authenticated=auth.authenticated(request),
                    data=data
                )
            elif request.method == "POST":
                if auth.authenticated(request):
                    Thread(target=restart,args=(1,)).start()
                return sanic.response.redirect("/")

        @app.route("/login", methods=["GET", "POST"])
        async def login(request: Request):
            if auth.authenticated(request):
                return sanic.response.redirect("/")
            else:
                flash_messages = []
                if request.method == "GET":
                    return render_template("login.html", l=l, flash_messages=flash_messages)
                elif request.method == "POST":
                    if request.form.get("password","") == data["web"]["password"]:
                        r = sanic.response.redirect("/")
                        auth.login_user(request, r)
                        return r
                    else: 
                        flash_messages.append(l('invalid_password'))
                        return render_template("login.html", l=l, flash_messages=flash_messages)

        @app.route("/text")
        @auth.login_required
        async def web_text_(request: Request):
            return sanic.response.json(
                {
                    "text": web_text
                }
            )

        @app.route("/logout")
        @auth.login_required
        async def logout(request: Request):
            r = sanic.response.redirect("/")
            auth.logout_user(request, r)
            return r

        @app.route("/config_editor", methods=["GET", "POST"])
        @auth.login_required
        async def config_editor(request: Request):
            flash_messages = []
            flash_messages_red = []
            if request.method == "GET":
                data = load_json("config.json")
                return render_template(
                    "config_editor.html",
                    l=l,
                    data=data,
                    config_tags=config_tags,
                    len=len,
                    type=type,
                    can_be_multiple=CanBeMultiple,
                    can_linebreak=CanLinebreak,
                    select=select,
                    str=str,
                    int=int,
                    bool=bool,
                    list=list,
                    map=map,
                    red=Red,
                    fix_required=FixRequired,
                    flash_messages=flash_messages,
                    flash_messages_red=flash_messages_red
                )
            else:
                flag = False
                raw = request.form
                data = load_json("config.json")
                corrected = data
                for key_,tags in config_tags.items():
                    keys = key_.replace("'","").replace("[","").split("]")
                    key = keys[0]
                    nest = len(keys) - 1

                    if nest == 1:
                        if dict in tags:
                            if not corrected.get(key):
                                corrected[key] = {}
                        else:
                            value = raw.get(f"['{key}']")
                        
                        if FixRequired in tags and value == corrected.get(key):
                            flash_messages_red.append(l('this_field_fix_required', key))
                            flag = True
                        if CanBeMultiple in tags:
                            if str in tags:
                                corrected[key] = re.split(r'\r\n|\n',value) if value else []
                            elif int in tags:
                                corrected[key] = [int(i) for i in re.split(r'\r\n|\n',value)] if value else []
                        elif str in tags:
                            corrected[key] = value.replace(r"\\n",r"\n").replace(r"\n","\n") if value else ""
                        elif int in tags:
                            corrected[key] = int(value) if value else 0
                        elif bool_ in tags:
                            corrected[key] = bool_.create(value)
                        elif bool_none in tags:
                            corrected[key] = bool_none.create(value)
                    elif nest == 2:
                        key2 = keys[1]

                        if dict in tags:
                            if not corrected.get(key):
                                if not corrected.get(key).get(key2):
                                    corrected[key][key2] = {}
                        else:
                            value2 = raw.get(f"['{key}']['{key2}']")
                        
                        if FixRequired in tags and value2 == corrected.get(key,{}).get(key2):
                            flash_messages_red.append(l('this_field_fix_required', f"{key}: {key2}"))
                            flag = True
                        if CanBeMultiple in tags:
                            if str in tags:
                                corrected[key][key2] = re.split(r'\r\n|\n',value2) if value2 else []
                            elif int in tags:
                                corrected[key][key2]  = [int(i) for i in re.split(r'\r\n|\n',value2)] if value2 else []
                        elif str in tags:
                            corrected[key][key2]  = value2.replace(r"\\n",r"\n").replace(r"\n","\n") if value2 else ""
                        elif int in tags:
                            corrected[key][key2] = int(value2) if value2 else 0
                        elif bool_ in tags:
                            corrected[key][key2] = bool_.create(value2)
                        elif bool_none in tags:
                            corrected[key][key2] = bool_none.create(value2)
                if flag:
                    return render_template(
                        "config_editor.html",
                        l=l,
                        data=corrected,
                        config_tags=config_tags,
                        len=len,
                        type=type,
                        can_be_multiple=CanBeMultiple,
                        can_linebreak=CanLinebreak,
                        select=select,
                        str=str,
                        int=int,
                        bool=bool,
                        list=list,
                        map=map,
                        red=Red,
                        fix_required=FixRequired,
                        flash_messages=flash_messages,
                        flash_messages_red=flash_messages_red
                    )
                else:
                    corrected["status"] = 1
                    with open('config.json', 'w', encoding='utf-8') as f:
                        json.dump(corrected, f, ensure_ascii=False, indent=4, sort_keys=False)
                    if raw.get("reload"):
                        Thread(target=restart, args=(1,)).start()
                        return sanic.response.redirect("/")
                    else:
                        flash_messages.append(l('web_saved'))
                        return render_template(
                            "config_editor.html",
                            l=l,
                            data=corrected,
                            config_tags=config_tags,
                            len=len,
                            join=str.join,
                            split=str.split,
                            type=type,
                            can_be_multiple=CanBeMultiple,
                            can_linebreak=CanLinebreak,
                            select=select,
                            str=str,
                            int=int,
                            bool=bool,
                            list=list,
                            map=map,
                            red=Red,
                            fix_required=FixRequired,
                            flash_messages=flash_messages,
                            flash_messages_red=flash_messages_red
                        )

        @app.route("/commands_editor", methods=["GET", "POST"])
        @auth.login_required
        async def commands_editor(request: Request):
            flash_messages = []
            flash_messages_red = []
            if request.method == "GET":
                data = load_json("commands.json")
                return render_template(
                    "commands_editor.html",
                    l=l,
                    data=data,
                    commands_tags=commands_tags,
                    len=len,
                    join=str.join,
                    split=str.split,
                    type=type,
                    can_be_multiple=CanBeMultiple,
                    select=select,
                    str=str,
                    int=int,
                    bool=bool,
                    list=list,
                    red=Red,
                    fix_required=FixRequired,
                    flash_messages=flash_messages,
                    flash_messages_red=flash_messages_red
                )
            elif request.method == "POST":
                flag = False
                raw = request.form
                data = load_json("commands.json")
                corrected = data
                for key_,tags in commands_tags.items():
                    keys = key_.replace("'","").replace("[","").split("]")
                    key = keys[0]
                    nest = len(keys) - 1

                    if nest == 1:
                        if dict in tags:
                            if not corrected[key]:
                                corrected[key] = {}
                        else:
                            value = raw.get(f"['{key}']")
                        
                        if FixRequired in tags and value == corrected.get(key):
                            flash_messages_red.append(l('this_field_fix_required', key))
                            flag = True
                        corrected[key] = re.split(r'\r\n|\n',value) if value else []
                if flag:
                    return render_template(
                        "commands_editor.html",
                        l=l,
                        data=corrected,
                        commands_tags=commands_tags,
                        len=len,
                        join=str.join,
                        split=str.split,
                        type=type,
                        can_be_multiple=CanBeMultiple,
                        select=select,
                        str=str,
                        int=int,
                        bool=bool,
                        list=list,
                        red=Red,
                        fix_required=FixRequired,
                        flash_messages=flash_messages,
                        flash_messages_red=flash_messages_red
                    )
                else:
                    with open('commands.json', 'w', encoding='utf-8') as f:
                        json.dump(corrected, f, ensure_ascii=False, indent=4, sort_keys=False)
                    if raw.get("reload"):
                        Thread(target=restart, args=(1,)).start()
                        return sanic.response.redirect("/")
                    else:
                        flash_messages.append(l('web_saved'))
                        return render_template(
                            "commands_editor.html",
                            l=l,
                            data=corrected,
                            commands_tags=commands_tags,
                            len=len,
                            type=type,
                            can_be_multiple=CanBeMultiple,
                            select=select,
                            str=str,
                            int=int,
                            bool=bool,
                            list=list,
                            red=Red,
                            fix_required=FixRequired,
                            flash_messages=flash_messages,
                            flash_messages_red=flash_messages_red
                        )

        @app.route("/replies_editor", methods=["GET", "POST"])
        @auth.login_required
        async def replies_editor(request: Request):
            flash_messages = []
            flash_messages_red = []
            if request.method == "GET":
                data = load_json("replies.json")
                return render_template(
                    "replies_editor.html",
                    l=l,
                    data=data,
                    flash_messages=flash_messages,
                    flash_messages_red=flash_messages_red,
                    len=len,
                    enumerate=enumerate,
                    str=str
                )
            elif request.method == "POST":
                raw = request.form
                corrected = {}
                for num in range(0,int(raw["number"][0])):
                    trigger = raw.get(f"trigger{str(num)}")
                    if not trigger:
                        flash_messages_red.append(l('cannot_be_empty'))
                        break
                    content = raw.get(f"content{str(num)}")
                    if not content:
                        flash_messages_red.append(l('cannot_be_empty'))
                        break
                    corrected[trigger] = content
                with open('replies.json', 'w', encoding='utf-8') as f:
                    json.dump(corrected, f, ensure_ascii=False, indent=4, sort_keys=False)
                if raw.get("reload"):
                    Thread(target=restart, args=(1,)).start()
                    return sanic.response.redirect("/")
                else:
                    flash_messages.append(l('web_saved'))
                    return render_template(
                        "replies_editor.html",
                        l=l,
                        data=corrected,
                        flash_messages=flash_messages,
                        flash_messages_red=flash_messages_red,
                        len=len,
                        enumerate=enumerate,
                        str=str
                    )

        @app.route("/party_viewer", methods=["GET"])
        @auth.login_required
        async def party_viewer(request: Request):
            return render_template(
                "party_viewer.html",
                l=l,
                clients=clients,
                enumerate=enumerate
            )

        @app.route("/clients<num>", methods=["GET", "POST"])
        @auth.login_required
        async def clients_viewer(request: Request, num: str):
            num = int(num)
            client = clients[num] if clients[num:num+1] else None

            if not client:
                sanic.exceptions.abort(404)
            flash_messages = []
            if request.method == "GET":
                return render_template(
                    "clients_viewer.html",
                    l=l,
                    client=client,
                    none=None,
                    len=len,
                    flash_messages=flash_messages
                )
            else:
                if request.form.get("command"):
                    content = request.form["command"][0] if isinstance(request.form["command"],list) else request.form["command"]
                    message = WebMessage(content, request.cookies.get(auth.cookie_key, 'NoID'), client)
                    await process_command(message)
                    result = message.result
                    if result:
                        for mes in message.result:
                            for m in mes.split('\n'):
                                flash_messages.append(m)

                    return render_template(
                        "clients_viewer.html",
                        l=l,
                        client=client,
                        none=None,
                        len=len,
                        flash_messages=flash_messages
                    )
                else:
                    return sanic.response.redirect(f"/clients{num}")

        @app.route("/clients_info/<num>", methods=["GET"])
        @auth.login_required
        async def clients_info(request: Request, num: str):
            num = int(num)
            client = clients[num] if len(clients[num:num+1]) == 1 else None

            if not client:
                return sanic.response.json(
                    {
                        "error": "account_not_exists"
                    }
                )
            elif not client.isready:
                return sanic.response.json(
                    {
                        "error": "account_not_loaded"
                    }
                )
            elif not client.party or not client.party.me:
                return sanic.response.json(
                    {
                        "error": "party_moving"
                    }
                )
            else:
                return sanic.response.json(
                    {
                        "display_name": client.user.display_name,
                        "id": client.user.id,
                        "leader": client.party.me.leader,
                        "banner": search_banner(client.party.me.banner[0]),
                        "level": client.party.me.banner[2],
                        "outfit": member_asset(client.party.me, "outfit"),
                        "outfit_variants": client.party.me.outfit_variants,
                        "backpack": member_asset(client.party.me, "backpack"),
                        "backpack_variants": client.party.me.backpack_variants,
                        "pickaxe": member_asset(client.party.me, "pickaxe"),
                        "pickaxe_variants": client.party.me.pickaxe_variants,
                        "contrail": member_asset(client.party.me, "contrail"),
                        "emote": member_asset(client.party.me, "emote"),
                        "party_id": client.party.id,
                        "members": [
                            {
                                "display_name": i.display_name,
                                "id": i.id,
                                "leader": i.leader,
                                "banner": search_banner(i.banner[0]),
                                "level": i.banner[2],
                                "outfit": member_asset(i, "outfit"),
                                "outfit_variants": i.outfit_variants,
                                "backpack": member_asset(i, "backpack"),
                                "backpack_variants": i.backpack_variants,
                                "pickaxe": member_asset(i, "pickaxe"),
                                "pickaxe_variants": i.pickaxe_variants,
                                "contrail": member_asset(i, "contrail"),
                                "emote": member_asset(i, "emote")
                            } for i in client.party.members
                        ]
                    }
                )

        @app.route("/boot_switch", methods=["GET", "POST"])
        @auth.login_required
        async def boot_switch(request: Request):
            if request.method == "GET":
                return render_template(
                    "boot_switch.html",
                    l=l,
                    len=len
                )
            elif request.method == "POST":
                raw = request.form
                for i in raw.keys():
                    if "on" in i or "off" in i:
                        break
                on_or_off = i
                num = int(re.sub(r"on|off","", on_or_off))
                on_or_off = i.replace(str(num),"")
                loop = asyncio.get_event_loop()
                if on_or_off == "on":
                    clients[num].booting = True
                    loop.create_task(clients[num].start())
                elif on_or_off == "off":
                    loop.create_task(clients[num].close())
                return sanic.response.redirect("/boot_switch")

        @app.route("/boot_info", methods=["GET"])
        @auth.login_required
        async def boot_info(request: Request):
            data = {}
            for client in clients:
                if not client.booting and not client.isready:
                    data[client.email] = {
                        "info": "info_closed",
                        "booting": client.booting,
                        "isready": client.isready
                    }
                elif client.booting:
                    data[client.email] = {
                        "info": "info_booting",
                        "booting": client.booting,
                        "isready": client.isready
                    }
                elif client.isready:
                    data[client.email] = {
                        "info": "info_ready",
                        "booting": client.booting,
                        "isready": client.isready
                    }
            return sanic.response.json(data)

        @app.exception(sanic.exceptions.NotFound)
        async def not_found(request: Request, exception: Exception):
            return render_template("not_found.html", l=l)

        @auth.no_auth_handler
        async def unauthorized(request: Request, *args, **kwargs):
            return sanic.response.redirect("/")

loop = asyncio.get_event_loop()
if data.get('web',{}).get('enabled',True) is True or data.get('status',1)  == 0:
    loop.create_task(run_app())

Thread(target=dprint,args=(),daemon=True).start()
Thread(target=store_banner_data).start()
if data.get("status",1) != 0:
    try:
        langs = [
            data["search-lang"],
            data["sub-search-lang"] 
        ] if data["sub-search-lang"] and data["sub-search-lang"] != data["search-lang"] else [
            data["search-lang"]
        ]
        store_item_data(langs)
    except Exception:	
        send(l('bot'),l('api_downing'),red)
    langs = [
        data["search-lang"],
        data["sub-search-lang"] 
    ] if data["sub-search-lang"] and data["sub-search-lang"] != data["search-lang"] else [
        data["search-lang"]
    ]
    items = {}
    styles = {}
    with ThreadPoolExecutor() as executor:
        items_futures = {executor.submit(search_item,lang,mode,data['fortnite'][type_.split(',')[0]],",".join(convert_to_new_type(i) for i in type_.split(','))): type_.split(',')[0] for lang in langs for mode in ("name","id") for type_ in ("outfit","backpack,pet","pickaxe","emote,emoji,toy")}
    for future,type_ in items_futures.items():
        result = future.result()
        if result and not items.get(type_):
            items[type_] = result[0]
    with ThreadPoolExecutor() as executor:
        styles_futures = {executor.submit(search_style,data["search-lang"],items.get(type_.split(',')[0],{}).get("id"),",".join(convert_to_new_type(i) for i in type_.split(','))): type_.split(',')[0] for type_ in ("outfit","backpack,pet","pickaxe") if data["fortnite"][f"{type_.split(',')[0]}_style"]}
    for future,type_ in styles_futures.items():
        result = future.result()
        if result and not styles.get(type_):
            variants = [i["variants"] for i in result if data["fortnite"][f"{type_}_style"] in i["name"]]
            if variants:
                styles[type_] = variants[0]
    for email in data["fortnite"]["email"]:
        email = email.strip()
        try:
            device_auth_details = get_device_auth_details().get(email.lower(), {})
            if not device_auth_details:
                device_auth_details = loop.run_until_complete(generate_device_auth_and_store(email))
            client = Client(
                auth=fortnitepy.DeviceAuth(
                    **device_auth_details
                ),
                default_party_config=fortnitepy.DefaultPartyConfig(
                    privacy=data['fortnite']['privacy']
                ),
                default_party_member_config=fortnitepy.DefaultPartyMemberConfig(
                    meta=[
                        partial(ClientPartyMember.set_outfit, items.get("outfit",{}).get("id",data["fortnite"]["outfit"]), variants=styles.get("outfit")),
                        partial(ClientPartyMember.set_backpack, items.get("backpack",{}).get("id",data["fortnite"]["backpack"]), variants=styles.get("backpack")),
                        partial(ClientPartyMember.set_pickaxe, items.get("pickaxe",{}).get("id",data["fortnite"]["pickaxe"]), variants=styles.get("pickaxe")),
                        partial(ClientPartyMember.set_battlepass_info, has_purchased=True, level=data['fortnite']['tier'], self_boost_xp=data['fortnite']['xpboost'], friend_boost_xp=data['fortnite']['friendxpboost']),
                        partial(ClientPartyMember.set_banner, icon=data['fortnite']['banner'], color=data['fortnite']['banner_color'], season_level=data['fortnite']['level'])
                    ]
                ),
                platform=fortnitepy.Platform(data['fortnite']['platform'].upper()),
                emote=items.get("emote",{}).get("id",data["fortnite"]["emote"])
            )
        except ValueError:
            send(l("bot"),traceback.format_exc(),red,add_d=lambda x:f'>>> {x}')
            send(l("bot"),l('error_while_setting_client'),red,add_d=lambda x:f'>>> {x}')
            continue
        clients.append(client)

if data.get('status',1) != 0 and bot_ready:
    loop.create_task(run_bot())
try:
    loop.run_forever()
except KeyboardInterrupt:
    sys.exit(1)

    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[35m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)


async def main() -> None:
    settings = partybot.BotSettings()
    device_auths = partybot.DeviceAuths(
        filename='device_auths.json'
    )

    await settings.load_settings_from_file('config.json')
    await device_auths.load_device_auths()

    if settings.debug:
        enable_debug()

    client = partybot.PartyBot(
        settings=settings,
        device_auths=device_auths
    )

    client.add_cog(partybot.CosmeticCommands(client))
    client.add_cog(partybot.PartyCommands(client))
    client.add_cog(partybot.ClientCommands(client))

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method="GET",
            url="https://partybot.net/api/discord"
        ) as r:
            invite = (await r.json())['invite'] if r.status == 200 else "8heARRB"

    print(crayons.cyan(client.message % 'PartyBot made by xMistt. '
                       'Massive credit to Terbau for creating the library.'))
    print(crayons.cyan(client.message % f'Discord server: https://discord.gg/{invite} - For support, questions, etc.'))

    if (settings.email and settings.password) and \
            (settings.email != 'email@email.com' and settings.password != 'password1'):
        try:
            await client.start()
        except fortnitepy.errors.AuthException as e:
            print(crayons.red(client.message % f"[ERROR] {e}"))
    else:
        print(crayons.red(client.message % f"[ERROR] Failed to login as no (or default) "
                          "account details provided."))

    await client.http.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
