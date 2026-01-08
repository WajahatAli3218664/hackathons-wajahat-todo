#!/bin/bash

# Setup ngrok for public URL (hides Codespace)
echo "🌐 Setting up public URL without Codespace domain..."

# Install ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

echo "📝 Setup ngrok account:"
echo "1. Go to https://ngrok.com/signup"
echo "2. Get your authtoken"
echo "3. Run: ngrok config add-authtoken YOUR_TOKEN"
echo "4. Run: ./scripts/start-public-urls.sh"

echo "🎯 This will give you clean URLs like:"
echo "Frontend: https://abc123.ngrok.io"
echo "Backend: https://def456.ngrok.io"