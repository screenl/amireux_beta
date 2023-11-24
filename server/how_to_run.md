# 1. Setup Flowise
- Make sure nodejs is installed. Then run `npm install flowise -g` in terminal
- Start flowise with `npx flowise start`
- Go to http://127.0.0.1:3000/, Click the right-top settings button and load `db.json` as database
# 2. Run Flask Server
- Run `source bin/activate` in terminal
- Start the server with `flask --app server run --debug`


**NOTE: The server side can only be runned on unix-like systems**