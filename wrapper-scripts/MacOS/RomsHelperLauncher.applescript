tell application "Terminal"
    activate
    do script "cd \"$(dirname \"$0\")\" && ./RomsHelper"
end tell