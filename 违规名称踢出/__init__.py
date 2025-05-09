from tooldelta import (
    constants,
    Frame,
    Plugin,
    cfg,
    Print,
    Chat,
    Player,
    plugin_entry,
)


class kill(Plugin):
    version = (0, 0, 5)
    name = "违规名称踢出"
    author = "大庆油田"
    description = "简单的违规名称踢出"

    def __init__(self, frame: Frame):
        self.frame = frame
        self.game_ctrl = frame.get_game_control()
        self.make_data_path()
        CFG_DEFAULT = {"踢出词": [], "原因": ""}
        self.cfg, _ = cfg.get_plugin_config_and_version(
            self.name, {}, CFG_DEFAULT, self.version
        )
        self.ci = self.cfg["踢出词"]
        self.yy = self.cfg["原因"]
        self.ListenPacket(constants.PacketIDS.PlayerList, self.on_prejoin)
        self.ListenPlayerJoin(self.on_player_join)
        self.ListenChat(self.on_player_message)

    def on_prejoin(self, pk: dict):
        is_joining = not pk["ActionType"]
        if is_joining:
            for entry_user in pk["Entries"]:
                player = entry_user["Username"]
                xuid = entry_user["XUID"]
                for a in self.ci:
                    if a in player:
                        self.game_ctrl.sendwocmd(f"kick {xuid} {self.yy}")
        return False

    def killpl(self, player: str, xuid: str):
        try:
            self.game_ctrl.sendcmd(f'/testfor "{player}"', True, timeout=4)
        except TimeoutError:
            Print.print_war(f"玩家 {player} 名字为敏感词, 已经踢出")
            self.game_ctrl.sendwocmd(f"kick {xuid} {self.yy}")
        for a in self.ci:
            if a in player:
                self.game_ctrl.sendwocmd(f"kick {xuid} {self.yy}")

    def on_player_message(self, chat: Chat):
        player = chat.player.name
        xuid = chat.player.xuid

        self.killpl(player, xuid)

    def on_player_join(self, playerf: Player):
        player = playerf.name
        xuid = playerf.xuid
        self.killpl(player, xuid)


entry = plugin_entry(kill)
