import pygame
import socket
import math

from settings import *
from support import folder_importer
from netbattle import NetBattle, send_json, recv_json

PORT_BASE = 50000

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def connection_screen():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Vaqueromon - Connect")
    clock = pygame.time.Clock()
    big = pygame.font.Font(None, 64)
    font = pygame.font.Font(None, 42)

    bg = (0, 60, 160)
    state = "menu"
    menu_index = 0
    mode = "host"
    room = ""
    ip = ""
    host_ip = get_local_ip()
    waiting = False
    conn = None
    listener = None
    finished = False

    while not finished:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if not waiting and e.type == pygame.KEYDOWN:
                if state == "menu":
                    if e.key in (pygame.K_UP, pygame.K_DOWN):
                        menu_index = 1 - menu_index
                    if e.key == pygame.K_RETURN:
                        mode = "host" if menu_index == 0 else "join"
                        state = "host_room" if mode == "host" else "join_room"

                elif state == "host_room":
                    if e.key == pygame.K_BACKSPACE:
                        room = room[:-1]
                    elif e.key == pygame.K_RETURN:
                        if room.isdigit() and len(room) == 4:
                            port = PORT_BASE + int(room)
                            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            listener.bind(("", port))
                            listener.listen(1)
                            listener.setblocking(False)
                            state = "wait"
                            waiting = True
                    else:
                        if e.unicode.isdigit() and len(room) < 4:
                            room += e.unicode

                elif state == "join_room":
                    if e.key == pygame.K_BACKSPACE:
                        room = room[:-1]
                    elif e.key == pygame.K_RETURN:
                        if room.isdigit() and len(room) == 4:
                            state = "ip"
                    else:
                        if e.unicode.isdigit() and len(room) < 4:
                            room += e.unicode

                elif state == "ip":
                    if e.key == pygame.K_BACKSPACE:
                        ip = ip[:-1]
                    elif e.key == pygame.K_RETURN:
                        if ip.strip():
                            finished = True
                    else:
                        if e.unicode in "0123456789." and len(ip) < 20:
                            ip += e.unicode

        screen.fill(bg)

        if state == "menu":
            t = big.render("Vaqueromon LAN Battle", True, (255, 255, 255))
            screen.blit(t, t.get_frect(center=(WINDOW_WIDTH / 2, 150)))
            h = font.render(("> Host Game" if menu_index == 0 else "  Host Game"), True, (255, 255, 255))
            j = font.render(("> Join Game" if menu_index == 1 else "  Join Game"), True, (255, 255, 255))
            screen.blit(h, (200, 300))
            screen.blit(j, (200, 360))
            iptxt = font.render("Your IP: " + host_ip, True, (255, 255, 255))
            screen.blit(iptxt, (200, 470))

        elif state == "host_room":
            t = big.render("Enter Room", True, (255, 255, 255))
            screen.blit(t, t.get_frect(center=(WINDOW_WIDTH / 2, 150)))
            r = big.render(room or "____", True, (255, 255, 255))
            screen.blit(r, r.get_frect(center=(WINDOW_WIDTH / 2, 300)))
            a = font.render("Share this IP:", True, (255, 255, 255))
            b = big.render(host_ip, True, (255, 255, 255))
            screen.blit(a, (200, 420))
            screen.blit(b, (200, 470))

        elif state == "join_room":
            t = big.render("Enter Room", True, (255, 255, 255))
            screen.blit(t, t.get_frect(center=(WINDOW_WIDTH / 2, 150)))
            r = big.render(room or "____", True, (255, 255, 255))
            screen.blit(r, r.get_frect(center=(WINDOW_WIDTH / 2, 300)))

        elif state == "ip":
            t = big.render("Enter Host IP", True, (255, 255, 255))
            screen.blit(t, t.get_frect(center=(WINDOW_WIDTH / 2, 150)))
            v = big.render(ip or "0.0.0.0", True, (255, 255, 255))
            screen.blit(v, v.get_frect(center=(WINDOW_WIDTH / 2, 300)))
            r = font.render("Room: " + room, True, (255, 255, 255))
            screen.blit(r, (200, 380))

        elif state == "wait":
            t = big.render("Waiting for Player...", True, (255, 255, 255))
            screen.blit(t, t.get_frect(center=(WINDOW_WIDTH / 2, 180)))
            i1 = font.render("IP: " + host_ip, True, (255, 255, 255))
            i2 = font.render("Room: " + room, True, (255, 255, 255))
            screen.blit(i1, (200, 350))
            screen.blit(i2, (200, 400))
            if listener is not None:
                try:
                    conn, addr = listener.accept()
                    conn.settimeout(None)
                    finished = True
                except BlockingIOError:
                    pass

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    if mode == "host":
        return True, int(room), conn
    else:
        return False, int(room), ip.strip()

def team_select_screen():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Vaqueromon - Select Team")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small = pygame.font.Font(None, 28)

    front_surfs = folder_importer("images", "front")
    names = list(MONSTER_DATA.keys())
    cols = 4
    rows = math.ceil(len(names) / cols)
    cursor = 0
    selected = []
    done = False

    grid_rect = pygame.FRect(100, 100, WINDOW_WIDTH - 200, WINDOW_HEIGHT - 260)
    cell_w = grid_rect.width / cols
    cell_h = grid_rect.height / rows

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    cursor = (cursor - 1) % len(names)
                elif e.key == pygame.K_RIGHT:
                    cursor = (cursor + 1) % len(names)
                elif e.key == pygame.K_UP:
                    cursor = (cursor - cols) % len(names)
                elif e.key == pygame.K_DOWN:
                    cursor = (cursor + cols) % len(names)
                elif e.key == pygame.K_SPACE:
                    name = names[cursor]
                    if name in selected:
                        selected.remove(name)
                    else:
                        if len(selected) < 4:
                            selected.append(name)
                elif e.key == pygame.K_RETURN:
                    if len(selected) == 4:
                        done = True

        screen.fill((0, 0, 80))
        title = font.render("Select 4 Vaqueromons", True, (255, 255, 255))
        screen.blit(title, title.get_frect(center=(WINDOW_WIDTH / 2, 60)))

        for i, name in enumerate(names):
            row = i // cols
            col = i % cols
            cx = grid_rect.left + col * cell_w
            cy = grid_rect.top + row * cell_h
            rect = pygame.FRect(cx + 10, cy + 10, cell_w - 20, cell_h - 20)

            bg_color = (60, 60, 60)
            if name in selected:
                bg_color = (0, 140, 0)
            if i == cursor:
                bg_color = (220, 200, 0)
            pygame.draw.rect(screen, bg_color, rect, border_radius=12)

            if name in front_surfs:
                img = front_surfs[name]
                img_rect = img.get_frect(center=(rect.centerx, rect.centery - 20))
                screen.blit(img, img_rect)

            label = small.render(name, True, (255, 255, 255))
            screen.blit(label, label.get_frect(midtop=(rect.centerx, rect.bottom - 28)))

        info = small.render("SPACE select/deselect | ENTER confirm (4)", True, (255, 255, 255))
        screen.blit(info, info.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70)))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    return selected

def host_client_handshake():
    is_host, room, payload = connection_screen()
    port = PORT_BASE + room
    if is_host:
        conn = payload
        conn.settimeout(None)
        return True, conn
    else:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((payload, port))
        c.settimeout(None)
        return False, c

def main():
    is_host, conn = host_client_handshake()
    local_team = team_select_screen()
    send_json(conn, {"type": "team", "team": local_team})
    other = recv_json(conn)
    remote_team = other.get("team", [])
    battle = NetBattle(conn, is_host, local_team, remote_team)
    battle.run()
    conn.close()

if __name__ == "__main__":
    main()