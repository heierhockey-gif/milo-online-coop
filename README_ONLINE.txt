MILO COOP — ONLINE ROOM-CODE BUILD

WHAT THIS VERSION DOES
- Player 1 clicks CREATE ROOM and receives a random 6-character code.
- Player 2 enters that code and clicks JOIN.
- No Node.js installation or terminal commands are needed on either player's computer.
- Players do not need to be on the same Wi-Fi network.
- Chat and the existing two-player co-op game use the same online connection.
- The game and its WebSocket room service are hosted together.

IMPORTANT: ONE-TIME ONLINE HOSTING SETUP
This ZIP is ready to deploy, but it is not already published on the internet. A hosted service is required to relay room codes and game data between players. GitHub Pages alone cannot run the room server.

Recommended deployment (Render)
1. Create or use a GitHub repository for this game. Upload the contents of this ZIP to the repository's main branch (the files should be at the repository root, including render.yaml).
2. Sign in to Render and choose New > Blueprint.
3. Connect the GitHub repository containing these files.
4. Render reads render.yaml, installs the server dependency, and starts the service. You do not install Node.js on your own computer; Render runs it in the cloud.
5. When deployment finishes, open the HTTPS URL Render gives the service. This is the actual game link both players should use. Do not use the GitHub Pages link for this build.

HOW TO PLAY AFTER DEPLOYMENT
1. Both players open the same Render game URL in a browser.
2. Player 1 opens CO-OP and clicks CREATE ROOM.
3. Milo displays a random 6-character code. Player 1 sends that code to their friend.
4. Player 2 opens CO-OP, types the code, and clicks JOIN.
5. When connected, both players can play and use chat.

NOTES
- The host must keep the game tab open. Closing it ends the room.
- Rooms are temporary and disappear when the host disconnects or the server restarts.
- This is private-code joining, not a public room browser.
- The existing game supports two players per room.
- Free hosting services may pause inactive apps; the first visit after a pause can take a little longer to load.
- If the service is redeployed or its URL changes, both players must use the new game URL.
