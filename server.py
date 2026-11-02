"""Milo online co-op server. Deploy with: uvicorn server:app --host 0.0.0.0 --port $PORT"""
import os, json, secrets, string, time
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Milo Online Co-op")
rooms = {}
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def new_code():
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(6))
        if code not in rooms:
            return code

async def send_json(peer, payload):
    if peer:
        try:
            await peer.send_text(json.dumps(payload))
            return True
        except Exception:
            return False
    return False

async def room_status(room):
    payload = {"type": "peer", "p2": bool(room.get("client")), "p3": bool(room.get("client2")),
               "connected": bool(room.get("client") or room.get("client2")), "roomCode": room["code"],
               "public": room["public"]}
    for peer in list(room.values()):
        if isinstance(peer, WebSocket):
            await send_json(peer, payload)

@app.get("/")
async def home():
    return FileResponse(ROOT / "Milo_Coop.html")

@app.get("/Milo_Coop.html")
async def game_file():
    return FileResponse(ROOT / "Milo_Coop.html")

@app.get("/api/rooms")
async def public_rooms():
    result = []
    for code, room in list(rooms.items()):
        if room.get("public") and room.get("host"):
            result.append({"code": code, "players": 1 + bool(room.get("client")) + bool(room.get("client2")),
                           "maxPlayers": 3, "openSlots": [role for role in ("client", "client2") if not room.get(role)]})
    return {"rooms": result}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    room = None
    role = None
    try:
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                continue
            kind = msg.get("type")
            if kind == "hello":
                requested = msg.get("role")
                if requested not in ("host", "client", "client2"):
                    await send_json(ws, {"type": "error", "message": "Unknown player slot."})
                    continue
                if requested == "host":
                    code = new_code()
                    room = {"code": code, "public": bool(msg.get("public")), "host": ws,
                            "client": None, "client2": None, "created": time.time()}
                    rooms[code] = room
                else:
                    code = str(msg.get("roomCode", "")).upper().strip()
                    room = rooms.get(code)
                    if not room or not room.get("host"):
                        await send_json(ws, {"type": "error", "message": "Room not found. Check the code or refresh public rooms."})
                        await ws.close()
                        return
                    if room.get(requested):
                        await send_json(ws, {"type": "error", "message": "That player slot is already occupied."})
                        await ws.close()
                        return
                role = requested
                room[role] = ws
                await send_json(ws, {"type": "room-created" if role == "host" else "room-joined",
                                     "roomCode": room["code"], "public": room["public"]})
                await room_status(room)
            elif room and role:
                if kind == "chat":
                    payload = {"type": "chat", "name": str(msg.get("name", "Player"))[:20],
                               "message": str(msg.get("message", ""))[:180]}
                    for player_role in ("host", "client", "client2"):
                        await send_json(room.get(player_role), payload)
                elif role == "host" and kind == "state":
                    for player_role in ("client", "client2"):
                        await send_json(room.get(player_role), msg)
                elif role in ("client", "client2") and kind == "input":
                    msg["role"] = role
                    await send_json(room.get("host"), msg)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        if room and role and room.get(role) is ws:
            room[role] = None
            if role == "host":
                for player_role in ("client", "client2"):
                    peer = room.get(player_role)
                    if peer:
                        await send_json(peer, {"type": "error", "message": "The host left. This room has closed."})
                        try: await peer.close()
                        except Exception: pass
                rooms.pop(room["code"], None)
            else:
                await room_status(room)
