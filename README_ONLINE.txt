MILO COOP — PUBLIC ONLINE GAME DEPLOYMENT

This package serves the game and its WebSocket multiplayer room server from one cloud service. Players do not need Node.js or any software installed. The cloud host runs the server.

WHAT PLAYERS GET
- A public game website that anyone can open.
- CREATE ROOM makes a private six-character invite code.
- A friend enters the code and clicks JOIN.
- Both players can play from different networks.
- Chat and co-op use the same online connection.
- The game supports two players per room.

IMPORTANT
This ZIP is deployment-ready, but it is not already published. You must deploy it to a cloud host to receive a working public URL. Google Sites and GitHub Pages cannot run this WebSocket server. Keep your Google Sites homepage if you like; change its PLAY link to the new cloud game URL.

RECOMMENDED DEPLOYMENT WITH RENDER
1. Extract this ZIP. The files Milo_Coop.html, server.js, package.json, and render.yaml must be at the top level of the folder.
2. Create a GitHub repository for Milo Coop and upload those top-level files to the repository root (not inside another folder).
3. Sign in to Render and choose New > Blueprint.
4. Connect the GitHub repository. Render reads render.yaml, installs the dependency, and starts the web service.
5. Wait for the deployment to finish, then open the HTTPS URL Render provides. That URL is the new public Milo Coop game website.
6. Update the PLAY link on your Google Sites homepage to point to that URL.

HOW TO PLAY
1. Both players open the same Render game URL.
2. Player 1 opens CO-OP and clicks CREATE ROOM.
3. Milo displays a six-character code. Send that code to your friend.
4. Player 2 enters the code and clicks JOIN.
5. Keep the game tab open while hosting the room.

HOSTING NOTES
- Public website means anyone can visit the game. Room joining is still private by code; this build does not show a public room directory.
- Rooms are temporary and disappear when the host leaves or the server restarts.
- The free hosting plan may pause after inactivity, so the first visit after a pause can take longer. Free plans also have usage and performance limits and may change.
- If the cloud service is redeployed or its URL changes, update the Google Sites PLAY link and have both players use the new URL.
- Ask a parent or guardian to help create/manage hosting accounts and review the provider's current plan limits.
