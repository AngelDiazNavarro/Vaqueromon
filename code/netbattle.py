import pygame
import json
import socket

from settings import *
from support import folder_importer, audio_importer, tile_importer
from monster import Monster, Opponent
from ui import UI, OpponentUI
from attack import AttackAnimationSprite

def send_json(conn, data):
    raw = json.dumps(data).encode("utf-8")
    length = len(raw)
    conn.sendall(length.to_bytes(4, "big") + raw)

def recv_json(conn):
    header = conn.recv(4)
    if not header:
        raise ConnectionError("connection closed")
    length = int.from_bytes(header, "big")
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("connection closed mid-packet")
        data += chunk
    return json.loads(data.decode("utf-8"))

def build_team_from_names(names):
    team = []
    for n in names:
        data = MONSTER_DATA[n]
        entry = {
            "name": n,
            "element": data["element"],
            "max_hp": data["health"],
            "hp": data["health"],
            "abilities": list(ABILITIES_DATA.keys())[:4]
        }
        team.append(entry)
    return team

def apply_action_to_state(state, player_id, action):
    if state.get("winner") is not None:
        return state
    me = "p0" if player_id == 0 else "p1"
    opp = "p1" if player_id == 0 else "p0"

    my_team = state["teams"][me]
    opp_team = state["teams"][opp]
    my_idx = state["active"][me]
    opp_idx = state["active"][opp]
    my_mon = my_team[min(max(my_idx, 0), len(my_team) - 1)]
    opp_mon = opp_team[min(max(opp_idx, 0), len(opp_team) - 1)]

    kind = action["kind"]

    if kind == "attack":
        move = action["move"]
        info = ABILITIES_DATA[move]
        base = info["damage"]
        mult = ELEMENT_DATA[info["element"]][opp_mon["element"]]
        dmg = int(base * mult)
        opp_mon["hp"] = max(0, opp_mon["hp"] - dmg)
        state["log"] = f"{me} used {move}!"
    elif kind == "heal":
        my_mon["hp"] = min(my_mon["max_hp"], my_mon["hp"] + 30)
        state["log"] = f"{me} healed!"
    elif kind == "pass":
        state["log"] = f"{me} passed."

    if opp_mon["hp"] <= 0:
        alive = [m for m in opp_team if m["hp"] > 0]
        if not alive:
            state["winner"] = me
        else:
            for i, m in enumerate(opp_team):
                if m["hp"] > 0:
                    state["active"][opp] = i
                    break

    if state.get("winner") is None:
        state["turn"] = 1 - player_id

    return state

class NetBattle:
    def __init__(self, conn, is_host, local_team_names, remote_team_names):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vaqueromon Battle")
        self.clock = pygame.time.Clock()
        self.conn = conn
        self.is_host = is_host
        self.player_id = 0 if is_host else 1
        self.running = True
        self.state = None
        self.my_action_pending = None

        from support import folder_importer, tile_importer, audio_importer, resource_path

        self.back_surfs = folder_importer("images", "back")
        self.front_surfs = folder_importer("images", "front")
        self.bg_surfs = folder_importer("images", "other")
        self.attack_frames = tile_importer(64, "images", "attacks")
        self.audio = audio_importer("audio")

        self.audio["music"].play(-1)

        if is_host:
            team0 = build_team_from_names(local_team_names)
            team1 = build_team_from_names(remote_team_names)
            self.state = {
                "teams": {"p0": team0, "p1": team1},
                "active": {"p0": 0, "p1": 0},
                "turn": 0,
                "winner": None,
                "log": "Battle start!"
            }
            send_json(self.conn, {"type": "state", "state": self.state})
        else:
            self.state = self.wait_for_state_from_host()

        self.me_key = "p0" if self.player_id == 0 else "p1"
        self.opp_key = "p1" if self.player_id == 0 else "p0"

        self.all_sprites = pygame.sprite.Group()
        self.player_monsters = []
        my_team_state = self.state["teams"][self.me_key]
        for entry in my_team_state:
            name = entry["name"]
            m = Monster(name, self.back_surfs[name])
            m.max_health = entry["max_hp"]
            m.health = entry["hp"]
            m.abilities = entry["abilities"]
            self.player_monsters.append(m)

        self.current_active_me = self.state["active"][self.me_key]
        self.monster = self.player_monsters[self.current_active_me]
        self.all_sprites.add(self.monster)

        opp_team_state = self.state["teams"][self.opp_key]
        self.current_active_opp = self.state["active"][self.opp_key]
        opp_entry = opp_team_state[self.current_active_opp]
        opp_name = opp_entry["name"]
        self.opponent = Opponent(opp_name, self.front_surfs[opp_name], self.all_sprites)
        self.opponent.max_health = opp_entry["max_hp"]
        self.opponent.health = opp_entry["hp"]
        self.opponent.abilities = opp_entry["abilities"]

        self.ui = UI(self.monster, self.player_monsters, self.get_input)
        self.opponent_ui = OpponentUI(self.opponent)

    def wait_for_state_from_host(self):
        while True:
            msg = recv_json(self.conn)
            if msg.get("type") == "state":
                return msg["state"]

    def get_input(self, state, data=None):
        if self.state.get("winner") is not None:
            return
        if self.state["turn"] != self.player_id:
            return

        if state == "attack" and data:
            attack_data = ABILITIES_DATA[data]
            anim_name = attack_data["animation"]
            AttackAnimationSprite(self.opponent, self.attack_frames[anim_name], self.all_sprites)
            self.audio[anim_name].play()
            self.my_action_pending = {"kind": "attack", "move": data}
        elif state == "heal":
            AttackAnimationSprite(self.monster, self.attack_frames["green"], self.all_sprites)
            self.audio["green"].play()
            self.my_action_pending = {"kind": "heal"}
        elif state == "pass":
            self.my_action_pending = {"kind": "pass"}
        elif state == "switch":
            self.my_action_pending = {"kind": "pass"}

    def host_loop_network(self):
        self.conn.settimeout(0.01)
        try:
            msg = recv_json(self.conn)
        except (socket.timeout, ConnectionError):
            return
        if msg.get("type") == "action":
            action = msg["action"]
            self.state = apply_action_to_state(self.state, 1, action)
            send_json(self.conn, {"type": "state", "state": self.state})

    def client_loop_network(self):
        self.conn.settimeout(0.01)
        try:
            msg = recv_json(self.conn)
        except (socket.timeout, ConnectionError):
            return
        if msg.get("type") == "state":
            self.state = msg["state"]

    def sync_from_state(self):
        my_team_state = self.state["teams"][self.me_key]
        opp_team_state = self.state["teams"][self.opp_key]

        for i, entry in enumerate(my_team_state):
            self.player_monsters[i].max_health = entry["max_hp"]
            self.player_monsters[i].health = entry["hp"]

        new_active_me = self.state["active"][self.me_key]
        if new_active_me != self.current_active_me:
            self.monster.kill()
            self.monster = self.player_monsters[new_active_me]
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster
            self.current_active_me = new_active_me

        new_active_opp = self.state["active"][self.opp_key]
        opp_entry = opp_team_state[new_active_opp]
        if new_active_opp != self.current_active_opp or self.opponent.name != opp_entry["name"]:
            self.opponent.kill()
            name = opp_entry["name"]
            self.opponent = Opponent(name, self.front_surfs[name], self.all_sprites)
            self.opponent.max_health = opp_entry["max_hp"]
            self.opponent.health = opp_entry["hp"]
            self.opponent_ui.monster = self.opponent
            self.current_active_opp = new_active_opp
        else:
            self.opponent.max_health = opp_entry["max_hp"]
            self.opponent.health = opp_entry["hp"]

    def draw_monster_floor(self):
        floor = self.bg_surfs.get("floor")
        if not floor:
            return
        for sprite in self.all_sprites:
            if isinstance(sprite, Monster) or isinstance(sprite, Opponent):
                floor_rect = floor.get_frect(center=sprite.rect.midbottom + pygame.Vector2(0, -10))
                self.display_surface.blit(floor, floor_rect)

    def show_win_screen(self):
        surf = self.display_surface
        surf.fill((0, 0, 0))
        font = pygame.font.Font(None, 72)
        win_id = self.state.get("winner")
        if win_id is None:
            text = "Game Over"
        elif win_id == ("p0" if self.player_id == 0 else "p1"):
            text = "You Win!"
        else:
            text = "You Lose!"
        t = font.render(text, True, (255, 255, 255))
        rect = t.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        surf.blit(t, rect)
        pygame.display.update()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    waiting = False
                elif e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            self.clock.tick(60)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False

            if self.state["turn"] == self.player_id and self.my_action_pending and self.state.get("winner") is None:
                if self.is_host:
                    self.state = apply_action_to_state(self.state, self.player_id, self.my_action_pending)
                    send_json(self.conn, {"type": "state", "state": self.state})
                else:
                    send_json(self.conn, {"type": "action", "action": self.my_action_pending})
                self.my_action_pending = None

            if self.is_host:
                self.host_loop_network()
            else:
                self.client_loop_network()

            self.sync_from_state()

            if self.state.get("winner") is not None:
                self.running = False

            if self.state["turn"] == self.player_id and self.state.get("winner") is None:
                self.ui.update()

            self.all_sprites.update(dt)

            self.display_surface.blit(self.bg_surfs["bg"], (0, 0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            self.opponent_ui.draw()

            info_font = pygame.font.Font(None, 28)
            turn_text = "Your turn" if self.state["turn"] == self.player_id else "Opponent's turn"
            t_surf = info_font.render(turn_text, True, (255, 255, 255))
            self.display_surface.blit(t_surf, (40, WINDOW_HEIGHT - 120))
            log_text = self.state.get("log", "")
            log_surf = info_font.render(log_text, True, (255, 255, 0))
            self.display_surface.blit(log_surf, (40, WINDOW_HEIGHT - 150))

            pygame.display.update()

        self.show_win_screen()
        pygame.quit()