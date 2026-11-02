MILO CO-OP — LOCAL WI-FI BUILD

This version keeps the existing game and two-player co-op, and adds:
- Open/close CHAT and CO-OP dropdown panels.
- Local Wi-Fi host/join connection using a WebSocket server address.
- Chat messages relayed between the two connected players.
- Online private rooms and public rooms are intentionally disabled for now.

HOW TO PLAY OVER WI-FI
1. Put this folder on the computer that will host.
2. Install Node.js, then open a terminal in this folder and run: npm install
3. Run: npm start
4. Find the host computer's local IPv4 address (for example, 192.168.1.25).
5. Allow Node.js through the computer's firewall on private networks if prompted.
6. Both players must be connected to the same Wi-Fi network.
7. Open the game on both devices. In CO-OP, enter:
   ws://HOST-IP:3000/ws
   Example: ws://192.168.1.25:3000/ws
8. Host clicks HOST WI-FI. The other player clicks JOIN WI-FI.

The host should create the room first, then the guest joins.
Do not use localhost on the guest device; use the host computer's LAN IP.
If the game is served from the same server on each device, the address can be left
blank and the game will connect to the current page's host.

ONLINE PRIVATE ROOMS AND PUBLIC ROOMS
These are visibly marked unavailable in this build and do not connect.
They can be enabled in a later update after the internet server is deployed.

This build retains the existing two-player architecture. It does not claim to add
three-player support.
