MILO ONLINE CO-OP — INTERNET ROOMS

WHAT CHANGED
- Replaced same-Wi-Fi-only connection with a hosted WebSocket connection.
- Added private rooms with six-character codes.
- Added a public room list.
- Kept the existing game, levels, artwork, controls, powers, lives and game simulation unchanged.

IMPORTANT CURRENT LIMIT
The supplied game engine has one host player and one remote player (2 players total). This update keeps that existing two-player engine. It does NOT add a third playable character. A true 3-player mode requires additional game-engine/player/HUD work.

DEPLOY TO RENDER
1. Create a GitHub repository and upload ALL files in this folder to its root.
2. In Render, choose New + > Web Service and connect that GitHub repository.
3. Render should detect render.yaml. If asked, use:
   Build Command: npm install
   Start Command: npm start
4. Deploy. Open the HTTPS URL Render gives you. The game and WebSocket server are served from the same address.
5. Share that URL with your friend. One player chooses CREATE PRIVATE ROOM (or CREATE PUBLIC ROOM); the other enters the six-character code or joins the public listing.

LOCAL TEST
Install Node.js, open a terminal in this folder, run:
   npm install
   npm start
Then open http://localhost:3000 in two browser windows. This local test is only on the same computer; Render deployment is what makes it reachable over the internet.

NOTES
- Free hosting may sleep when idle and take a little time to wake up.
- Do not use the old Python/Wi-Fi launcher for the hosted version. The new server.js is the entry point.
