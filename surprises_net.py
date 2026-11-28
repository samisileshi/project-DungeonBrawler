# author: Obaidullah Ahmad
# F15 Special Dungeon Events - networked version (Milestone 3).
#
# Protocol: one JSON object per line, sent over TCP.
#   client -> server  {"type": "join", "name": "Obaid"}
#   server -> client  {"type": "joined", "hp": 100, "max_hp": 100}
#   client -> server  {"type": "surprise_step"}
#   server -> client  {"type": "surprise_result", "event": "mine", "hp": 90,
#                      "max_hp": 100, "upcoming": 5}
#   server -> client  {"type": "error", "message": "..."}  (bad request)
#   client -> server  {"type": "pause"} / {"type": "accept_pause"} / {"type": "resume"}
#   server -> client  {"type": "pause_status", "message": "..."}
#   server -> client  {"type": "paused", "message": "..."}  (step while paused)
#
# Run the server:   python surprises_net.py server --difficulty hard
# Run a client:     python surprises_net.py client --name Obaid
# (start two clients in two terminals to see both players share one deck)
import argparse
import json
import socket
import socketserver
import threading
import time

from surprises import SurpriseDeck

HOST = "127.0.0.1"
PORT = 5050
PAUSE_LIMIT = 30   # seconds a one-player pause lasts (team spec section 24)


# ===== Concurrency + shared state =====
# Every client gets its own thread (ThreadingTCPServer), but all players
# draw from ONE shared deck/queue. The lock makes sure only one thread
# changes the deck at a time, so two players can never dequeue the same
# event or corrupt the queue.
class SurpriseGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.deck = SurpriseDeck()
        self.lock = threading.Lock()
        # Pause state (Feature 14), shared by all players like the deck.
        self.paused_by = None      # name of the player who asked to pause
        self.pause_started = 0.0   # when the pause began (time.time())
        self.mutual = False        # True once another player accepts

    # ===== Pause system =====
    # One player pauses -> game stops for up to PAUSE_LIMIT seconds.
    # Another player accepts -> mutual pause, no time limit.
    # Either player resumes -> game continues.
    # Always called while holding self.lock.
    def _seconds_left(self):
        if self.paused_by is None or self.mutual:
            return None
        left = PAUSE_LIMIT - (time.time() - self.pause_started)
        if left <= 0:
            self.paused_by = None   # nobody accepted in time: auto-resume
            return None
        return int(left) + 1

    def pause_message(self):
        # Returns why the game is paused, or None if it isn't.
        with self.lock:
            left = self._seconds_left()
            if self.paused_by is None:
                return None
            if self.mutual:
                return "Game paused by both players. Choose Resume to continue."
            return f"Game paused by {self.paused_by} ({left}s left)."

    def request_pause(self, name):
        with self.lock:
            self._seconds_left()
            if self.paused_by is not None:
                return "The game is already paused."
            self.paused_by = name
            self.pause_started = time.time()
            self.mutual = False
            return f"Paused. Others have {PAUSE_LIMIT}s to accept."

    def accept_pause(self, name):
        with self.lock:
            self._seconds_left()
            if self.paused_by is None:
                return "Nobody has asked to pause."
            if self.paused_by == name:
                return "You can't accept your own pause."
            self.mutual = True
            return "Mutual pause. No time limit."

    def resume(self, name):
        with self.lock:
            self._seconds_left()
            if self.paused_by is None:
                return "The game isn't paused."
            self.paused_by = None
            self.mutual = False
            return f"{name} resumed the game."

    def step(self, player):
        with self.lock:
            if self.deck.upcoming.is_empty():
                self.deck.balance_events(self.difficulty)
            event = self.deck.pick()
            self.deck.apply_surprises(player, event)
            upcoming = self.deck.upcoming.size
        return event, upcoming


# ===== Sockets: message handler =====
# The team's shared server can call this directly for "surprise_step".
def handle_message(msg, player, game):
    msg_type = msg.get("type")
    if msg_type == "join":
        player["name"] = str(msg.get("name", "player"))
        return {"type": "joined", "hp": player["hp"], "max_hp": player["max_hp"]}
    if msg_type == "surprise_step":
        if player["hp"] <= 0:
            return {"type": "error", "message": "you are dead"}
        paused = game.pause_message()
        if paused:
            return {"type": "paused", "message": paused}
        event, upcoming = game.step(player)
        return {"type": "surprise_result", "event": event, "hp": player["hp"],
                "max_hp": player["max_hp"], "upcoming": upcoming}
    if msg_type == "pause":
        return {"type": "pause_status", "message": game.request_pause(player["name"])}
    if msg_type == "accept_pause":
        return {"type": "pause_status", "message": game.accept_pause(player["name"])}
    if msg_type == "resume":
        return {"type": "pause_status", "message": game.resume(player["name"])}
    return {"type": "error", "message": "unknown message type: " + str(msg_type)}


class SurpriseHandler(socketserver.StreamRequestHandler):
    # Runs in its own thread, once per connected client.
    def handle(self):
        player = {"name": "player", "hp": 100, "max_hp": 100}
        print("Client connected:", self.client_address)
        for line in self.rfile:
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                reply = {"type": "error", "message": "invalid JSON"}
            else:
                reply = handle_message(msg, player, self.server.game)
            self.wfile.write((json.dumps(reply) + "\n").encode())
        print("Client left:", player["name"])


class SurpriseServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address, difficulty):
        super().__init__(address, SurpriseHandler)
        self.game = SurpriseGame(difficulty)


def run_server(host, port, difficulty):
    with SurpriseServer((host, port), difficulty) as server:
        print(f"Surprise server on {host}:{port} ({difficulty})")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


# ===== Client =====
def send(sock_file, msg):
    sock_file.write((json.dumps(msg) + "\n").encode())
    sock_file.flush()
    line = sock_file.readline()
    if not line:
        # An empty read means the server closed the connection.
        raise ConnectionError("server closed the connection")
    return json.loads(line)


def run_client(host, port, name):
    try:
        sock = socket.create_connection((host, port))
    except OSError:
        print(f"Could not connect to {host}:{port}. Is the server running?")
        return
    with sock, sock.makefile("rwb") as f:
        try:
            play(f, name)
        except ConnectionError:
            # Server crashed, was stopped, or the network dropped.
            print("Lost connection to the server. Game over.")


def play(f, name):
    reply = send(f, {"type": "join", "name": name})
    print(f"Joined as {name}. HP {reply['hp']}/{reply['max_hp']}")
    while True:
        choice = input("1) Step  2) Pause  3) Accept pause  4) Resume  5) Quit\n"
                       "Choose: ")
        if choice == "1":
            reply = send(f, {"type": "surprise_step"})
            if reply["type"] == "paused":
                print(reply["message"])
                continue
            if reply["type"] == "error":
                print("Error:", reply["message"])
                break
            print(f"{reply['event']}! HP {reply['hp']}/{reply['max_hp']}"
                  f" ({reply['upcoming']} planned events left)")
            if reply["hp"] <= 0:
                print("You died!")
                break
        elif choice in PAUSE_CHOICES:
            reply = send(f, {"type": PAUSE_CHOICES[choice]})
            print(reply["message"])
        elif choice == "5":
            break
        else:
            print("Please type a number from 1 to 5.")


# Menu number -> message type sent to the server.
PAUSE_CHOICES = {"2": "pause", "3": "accept_pause", "4": "resume"}


def main():
    parser = argparse.ArgumentParser(description="Networked surprise events")
    parser.add_argument("mode", choices=["server", "client"])
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--difficulty", choices=["easy", "normal", "hard"],
                        default="normal")
    parser.add_argument("--name", default="player")
    args = parser.parse_args()
    if args.mode == "server":
        run_server(args.host, args.port, args.difficulty)
    else:
        run_client(args.host, args.port, args.name)


if __name__ == "__main__":
    main()
