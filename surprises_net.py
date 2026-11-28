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
#
# Run the server:   python surprises_net.py server --difficulty hard
# Run a client:     python surprises_net.py client --name Obaid
# (start two clients in two terminals to see both players share one deck)
import argparse
import json
import socket
import socketserver
import threading

from surprises import SurpriseDeck

HOST = "127.0.0.1"
PORT = 5050


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
        event, upcoming = game.step(player)
        return {"type": "surprise_result", "event": event, "hp": player["hp"],
                "max_hp": player["max_hp"], "upcoming": upcoming}
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
    return json.loads(sock_file.readline())


def run_client(host, port, name):
    try:
        sock = socket.create_connection((host, port))
    except OSError:
        print(f"Could not connect to {host}:{port}. Is the server running?")
        return
    with sock, sock.makefile("rwb") as f:
        reply = send(f, {"type": "join", "name": name})
        print(f"Joined as {name}. HP {reply['hp']}/{reply['max_hp']}")
        while True:
            choice = input("1) Step  2) Quit\nChoose: ")
            if choice == "1":
                reply = send(f, {"type": "surprise_step"})
                if reply["type"] == "error":
                    print("Error:", reply["message"])
                    break
                print(f"{reply['event']}! HP {reply['hp']}/{reply['max_hp']}"
                      f" ({reply['upcoming']} planned events left)")
                if reply["hp"] <= 0:
                    print("You died!")
                    break
            elif choice == "2":
                break
            else:
                print("Please type 1 or 2.")


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
