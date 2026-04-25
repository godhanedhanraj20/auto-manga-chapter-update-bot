<div align="center">
  <img src="https://files.catbox.moe/vhm5zo.jpg" alt="Banner" width="600px" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" />

  <br/>

  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1200&color=2AA889&center=true&vCenter=true&width=500&lines=AUTO+MANGA+BOT;Modular+Architecture;Built+with+Kurigram" />

  <br/>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-yellow?style=flat-square&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Framework-Kurigram-blue?style=flat-square" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />
  </p>

  <h3>One-Click Deploy</h3>
  
  <p>
    <a href="https://heroku.com/deploy?template=https://github.com/KunalG932/auto-manga-chapter-update-bot">
      <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" />
    </a>
  </p>
</div>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:00ffcc,100:0066ff&height=2&section=footer" />
</p>

## What's this?

Hey! This is a powerful Telegram bot designed to make running a manga channel a breeze. Instead of manually checking sites and uploading files, this bot does everything for you—from tracking new chapters to uploading them as clean PDFs.

---

## Cool Features

- **Auto Everything**: It checks 35+ sources every few minutes so you don't have to.
- **Clean Files**: Converts chapters into high-quality PDF or CBZ files automatically.
- **Your Branding**: Add your own watermarks, promo banners, and captions to every post.
- **Smart Tracking**: If one site is down, it checks others to make sure your followers get their fix ASAP.
- **Fast Search**: Built-in search engine to find and track any manga in seconds.
- **Easy Deployment**: Runs on Heroku, VPS, or even your local machine with just a few clicks.

---

## Technical Stuff

```text
Auto Manga Updates   ████████████░░░ 85%
Smart Search Engine  ███████████░░░░ 80%
Plugin Architecture  ██████████████ 100%
Async MongoDB        ████████████░░░ 90%
Configuration System █████████████░░ 95%
```

- **Built with Kurigram**: A super fast and customizable Telegram framework.
- **Motor (MongoDB)**: Everything is stored asynchronously to keep things snappy.
- **APScheduler**: Handles all the background jobs like a pro.
- **Custom Scrapers**: Modular scraper system that's easy to expand.

---

## How it Works (Under the Hood)

```mermaid
graph TD
    subgraph "User Interface"
        U((User)) <-->|Commands/Callbacks| BC[Bot Core]
    end

    subgraph "Logic Processing"
        BC -->|Route| PM{Plugin Manager}
        PM -->|/search| SM[Search Manager]
        PM -->|/settings| DB[(MongoDB)]
    end

    subgraph "Automation (Scheduler)"
        SCH[APScheduler] -->|Intervals| Jobs[Cleanup & Check Jobs]
        
        Jobs -->|Fetch Subs| DB
        Jobs -->|Check Updates| SCRP[Scraper Manager]
        Jobs -->|New Content| DL[Downloader Service]
        DL -->|Processing| PDF[PDF/CBZ Maker]
        PDF -->|Upload| BC
    end

    subgraph "External Integration"
        SCRP -->|Scrape| WEB[35+ Sites]
        DL -->|Upload| CBX[Image Hosting (Catbox/Telegraph)]
    end
```

---

## Getting Started

1. **Clone it**:
   ```bash
   git clone https://github.com/KunalG932/auto-manga-chapter-update-bot.git
   cd auto-manga-chapter-update-bot
   ```

2. **Install deps**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Config**:
   Create a `.env` file and fill in your `API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_DB_URI`, and `OWNER_ID`.

   Optional (recommended for Catbox stability): `CATBOX_USERHASH`.

4. **Blast off**:
   ```bash
   python bot.py
   ```

---

## Deployment

### Heroku (Recommended)

1. Click the **One-Click Deploy** button above.
2. Fill in the required environment variables:
   - `API_ID` - Get from [my.telegram.org](https://my.telegram.org)
   - `API_HASH` - Get from [my.telegram.org](https://my.telegram.org)
   - `BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
   - `MONGO_DB_URI` - Your MongoDB connection string
   - `OWNER_ID` - Your Telegram user ID
   - `CATBOX_USERHASH` *(optional)* - Catbox account userhash for more reliable uploads
3. Deploy and scale the worker dyno.

### Manual Heroku CLI

```bash
# Clone the repo
git clone https://github.com/KunalG932/auto-manga-chapter-update-bot.git
cd auto-manga-chapter-update-bot

# Login to Heroku
heroku login

# Create app
heroku create auto-manga-chapter-update-bot

# Set environment variables
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set MONGO_DB_URI=your_mongo_uri
heroku config:set OWNER_ID=your_user_id
heroku config:set CATBOX_USERHASH=your_catbox_userhash  # optional

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1
```

---

## Contributing & Help

Want to add a new site, fix a bug, or just add a cool feature? 
1. Fork the repo.
2. Make your changes in a new branch.
3. Send a Pull Request!

If you find any bugs or have issues, just open an Issue here or hit us up in the channel.

---

<p align="center">
  <b>Find us here</b><br>
  <a href="https://t.me/nullzair">Message Admin</a> | <a href="https://t.me/codexnano">Join Channel</a>
</p>

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&pause=1000&color=888888&center=true&vCenter=true&width=500&lines=Made+with+by+nullzair" />
</div>
