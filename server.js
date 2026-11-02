const http = require('http');
const fs = require('fs');
const path = require('path');
const { WebSocketServer, WebSocket } = require('ws');

const PORT = process.env.PORT || 3000;
const ROOT = __dirname;
const rooms = new Map();
const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
function makeCode() {
  let code;
  do { code = Array.from({length:6}, () => alphabet[Math.floor(Math.random()*alphabet.length)]).join(''); }
  while (rooms.has(code));
  return code;
}
function send(ws, data) { if (ws && ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(data)); }
function roomStatus(room) {
  const connected = !!(room.host && room.client);
  send(room.host, {type:'peer', connected});
  send(room.client, {type:'peer', connected});
}
function publicRooms() {
  return [...rooms.values()].filter(r => r.isPublic && r.host && !r.client)
    .map(r => ({code:r.code, players:1, maxPlayers:2}));
}
function broadcastRoomList() {
  const payload = {type:'public-rooms', rooms:publicRooms()};
  for (const ws of clients) send(ws, payload);
}
const clients = new Set();
const server = http.createServer((req,res) => {
  const rawPath = (req.url || '/').split('?')[0];
  if (rawPath === '/healthz') {
    res.writeHead(200, {'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});
    return res.end(JSON.stringify({ok:true, service:'milo-coop-online', activeRooms:rooms.size}));
  }
  let pathname;
  try { pathname = decodeURIComponent(rawPath); }
  catch { res.writeHead(400); return res.end('Bad request'); }
  if (pathname === '/') pathname = '/Milo_Coop.html';
  const file = path.resolve(ROOT, '.' + pathname);
  if (!file.startsWith(ROOT + path.sep) && file !== path.join(ROOT,'Milo_Coop.html')) { res.writeHead(403); return res.end('Forbidden'); }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end('Not found'); }
    const ext = path.extname(file);
    const types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json'};
    res.writeHead(200, {'Content-Type':types[ext] || 'application/octet-stream','Cache-Control':'no-store'});
    res.end(data);
  });
});
const wss = new WebSocketServer({server, path:'/ws', maxPayload:4*1024*1024});
wss.on('connection', ws => {
  clients.add(ws);
  let room = null, role = null;
  send(ws, {type:'public-rooms', rooms:publicRooms()});
  ws.on('message', raw => {
    let msg; try { msg = JSON.parse(raw.toString()); } catch { return; }
    if (msg.type === 'list-rooms') { send(ws,{type:'public-rooms',rooms:publicRooms()}); return; }
    if (msg.type === 'hello') {
      if (role) return;
      if (msg.role === 'host') {
        role = 'host';
        const code = makeCode();
        room = {code, host:ws, client:null, isPublic:!!msg.isPublic};
        rooms.set(code, room);
        send(ws,{type:'room-created',code,isPublic:room.isPublic});
        broadcastRoomList();
      } else if (msg.role === 'client') {
        const code = String(msg.roomCode || '').toUpperCase().replace(/[^A-Z0-9]/g,'');
        const target = rooms.get(code);
        if (!target || !target.host || target.client) { send(ws,{type:'error',message:'That room is unavailable. Check the code or choose another public room.'}); return; }
        room = target; role = 'client'; room.client = ws;
        send(ws,{type:'joined',code});
        roomStatus(room); broadcastRoomList();
      }
      return;
    }
    if (!room || !role) return;
    if (role === 'client' && msg.type === 'input') send(room.host,{type:'input',keys:msg.keys || {}});
    if (role === 'host' && msg.type === 'state') send(room.client, msg);
    if (msg.type === 'chat') {
      const message = String(msg.message || '').trim().slice(0, 180);
      if (message) send(role === 'host' ? room.client : room.host, {
        type:'chat', from:role === 'host' ? 'HOST' : 'PLAYER 2', message
      });
    }
  });
  ws.on('close', () => {
    clients.delete(ws);
    if (room) {
      if (role === 'host') {
        rooms.delete(room.code);
        send(room.client,{type:'error',message:'The host left the room.'});
      } else if (role === 'client' && room.client === ws) room.client = null;
      roomStatus(room);
      broadcastRoomList();
    }
  });
  ws.on('error', () => {});
});
server.listen(PORT, '0.0.0.0', () => console.log(`Milo Online listening on ${PORT}`));
