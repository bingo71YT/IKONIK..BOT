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
