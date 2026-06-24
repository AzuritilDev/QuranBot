# ﴾ QuranBot ﴿

<p align="center">
  <img src="docs/assets/quranbotlogo.webp" width="350" />
</p>

<p>
  <a href="LICENSE">
    <img alt="GitHub License" src="https://img.shields.io/github/license/AzuritilDev/QuranBot">
  </a>
  <a href="https://github.com/AzuritilDev/QuranBot/commit/main">
        <img src="https://img.shields.io/github/last-commit/AzuritilDev/QuranBot">
  </a>
  <a href="https://github.com/AzuritilDev/QuranBot/issues">
        <img src="https://img.shields.io/github/issues/AzuritilDev/QuranBot">
  </a>
  <a href="https://github.com/AzuritilDev/QuranBot/releases/latest">
      <img src="https://img.shields.io/github/v/release/AzuritilDev/QuranBot">
  </a>
  <a href="https://github.com/AzuritilDev/QuranBot/stargazers">
    <img src="https://img.shields.io/github/stars/AzuritilDev/QuranBot">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff">
  </a>
  <a href="https://docs.astral.sh/uv/">
    <img src="https://img.shields.io/badge/uv-261230.svg?logo=uv&logoColor=#de5fe9">
  </a>
  <a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white">
  </a>
  <a href="https://redis.io/">
    <img src="https://img.shields.io/badge/Redis-%23DD0031.svg?logo=redis&logoColor=white">
  </a>
</p>

## Disclaimers

### 1. Religious Disclaimer
The translations of the Holy Quran provided in this application are sourced from the Saheeh International translation. While this translation is widely trusted and highly regarded, no translation can perfectly capture the absolute depth, nuance, and meaning of the original Arabic text. The interpretations remain the scholarly effort of the translators. Users should consult qualified Islamic scholars for definitive rulings or detailed study.

### 2. Calculation Disclaimer
Prayer times are calculated automatically using the [Adhanpy](https://github.com/alphahm/adhanpy/) (Adhan) library. These calculations are based on high-precision astronomical equations and standard global calculation methods (e.g., ISNA, MWL). Because slight geographic and atmospheric variations exist, these prayer times are estimates. Users are encouraged to verify times visually or by listening to the local Adhan from their nearest mosque.

### 3. Limitation of Liability
The developers and contributors of this application shall not be held liable for any direct, indirect, or incidental damages or loss of profits arising from the use, interpretation, or reliance on the information, prayer times, or translations provided herein.

### 4. Open Source and Copyright Acknowledgment
This application utilizes open-source software and copyrighted materials:
* **Adhanpy / Adhan Library:** Powered by the open-source adhanpy library (developed by alphahm), based on the upstream Batoul Apps Adhan ecosystem, and distributed under the MIT License.
* **Saheeh International Quran:** Used in accordance with standard permissions for the digital display and distribution of the meaning of the Quran.

## ⏾ Overview
<br /> بسم الله الرحمن الرحيم

<img src="docs/assets/quranbotthumbnail.jpg.png" style="vertical-align: middle;" />

This is an open-source, discord.py-based discord bot I made for displaying Islamic scripture. <br />
So that it is easy to access Islamic information while using Discord. <br />
It's written in Python and supports Docker. <br />
And the ease of use? So easy to set up that you might forget that you ever set it up! <br />

Amongst the reasons why I made this are:

It was narrated by Uthman that The Prophet(ﷺ) said:
>"The best among you are those who learn the Qur'an and teach it."
(Sahih al-Bukhari 5027)

It was narrated by Abu Huraira that The Prophet(ﷺ) said:
>"When a man dies, his acts come to an end, but three, recurring charity, or knowledge (by which people) benefit, or a pious child, who prays for him (for the deceased)."
(Sahih Muslim 1631)

Abu Huraira reported Allah's Messenger (ﷺ) as saying:
>"He who called (people) to righteousness, there would be reward (assured) for him like the rewards of those who adhered to it, without their rewards being diminished in any respect. And he who called (people) to error, he shall have to carry (the burden) of its sin, like those who committed it, without their sins being diminished in any respect."
(Sahih Muslim 2674)

---

## ⏾ Highlights
### Features and things to implement

||||
| ------------ | ------------ | ------------ |
| ✓ - Working/Added/Supported | / - Incomplete  | x - Unsupported/Not Added  |

|||
| ------------ | ------------ |
| A command to display Qur'ânic verses. | ✓  |
| Dockerized the application. | ✓  |
| Migrated to uv package manager. | ✓  |
| Chat commands for displaying Qur'ânic verses. | ✓  |
| A command to display prayer times. | ✓  |
| Ability to set Daily verses on a specific channel. | ✓  |
| Custom quote changes to a random quote from a list of quotes periodically. | ✓  |
| A way to test the application using pytest. | /  |
| Qur'ân SQLite database. | x  |
| A command to display Ahadith. | x  |
| A command to display Tafsîr. | x  |

---

## ⏾ Features
- `/help`: A slash command that displays all the available slash commands.
- `/quran`: A slash command that takes two arguments of integer type as input, chapter and verse, it displays a Qur'ânic verse based on the given user input. (Example: `/quran chapter:2 verse:4` will display the contents of Surah Al-Baqarah, ayah number four.)
- `/set-daily-quran`: A slash command that takes a channel as its only argument, when ran it will set a webhook on the selected channel where it will send verses daily. (Example usage: `/set-daily-quran channel:#general`)
- `/prayer-times`: A slash command that shows the obligatory Islamic prayer times of the day based on the geographic location of the given city. (Example usage: `/prayer-times city:Paris`)
- `/status`: Displays system information about the bot.

---

## ⏾ Requirements
To start hosting your own QuranBot, you will need:
- [Docker](https://www.docker.com/get-started/)
- [Python (Preferably version 3.11)](https://www.python.org/downloads/)
>Note: You won't really need Python if you're going to use Docker.

And that's pretty much it.

---

## ⏾ Installation

Before Installation: Make sure you have cloned the repository either via the "<> Code" section as .zip file or via using the `git clone https://github.com/AzuritilDev/QuranBot` command in your terminal.

## 1. Docker Installation:
### Short Instructions
- Create your bot
- Get the auth token
- Make and fill out your .env file
- Run `docker compose up`

That's it.
### Detailed Instructions:
Before we begin, download the source code and extract it to a folder, you can name it something like "quranbot". <br />
First things first, you need to create a new Discord application. <br />
Head to the [Discord Developer Portal](https://discord.com/developers/applications) and create your bot application. <br />
After you have done that, you will need to get its Authorization Token <br />
Head to Applications -> Your Application -> Overview -> Bot <br />
![Token Reset](docs/assets/reset_token_location.png)
Click the "Reset Token" button, it will show you the bot's token, copy the token to your clipboard. <br />
Create an ".env" file, the structure of the .env file should be the way it's instructed in .env.example, <br />
fill out the .env file accordingly to what you have, whether it be bot tokens, PostgreSQL usernames, passwords, etc. <br />
or you can just edit .env.example.clean to your preferences and then name it ".env" <br /> 
After that, open up your terminal, go to the root directory of the project, and run the following: <br />

```bash
docker compose up
```
This will build the application, create a database and run the container. <br />

To safely shut it down, run the following:
```bash
docker compose down
```

If you want to shut down the application and delete its saved data, run:
```bash
docker compose down -v
```
>Note: Please use this command responsibly, this will power down the container AND delete the saved PostgreSQL data.

If you've done everything correctly, you should see the bot's status as online while the container is running. <br />

If you've updated the source code for your custom build make sure to run it using:
```bash
docker compose up --build
```
To keep it up to date with your changes. <br />

If you want to run the container as a background task without logs filling up your terminal, run it with the `-d` flag:
```bash
docker compose up -d
```
## 2. Manual Python Installation:
### Short Instructions:
- Download the repository and extract it into a folder.
- Create your .env file and fill it out.
- Run `uv sync --frozen --no-dev` or `pip install -r requirements.txt` to install all the neccessary dependencies
- Run `python main.py`

And you're done.
### Detailed Instructions:
- Make sure to get your bot's token and store it in a .txt file or somewhere else.
- Install [Python](https://www.python.org/downloads/) version 3.11
- Download the repository, if you downloaded the .zip, extract it into a folder, name the folder something like "quranbot".
- Create an .env file in the folder, fill it out accordingly to .env.example (You can remove Docker related variables and files if you're not going to use Docker).
- Open up your terminal or command prompt, make sure you are in the quranbot folder's directory inside the terminal/command prompt
- Run `uv sync --frozen --no-dev` if you use the uv package manager or run `pip install -r requirements.txt` if you prefer using requirements.txt, make sure pip is installed in your machine (If you want to install the uv package manager, either run `pip install uv` if you have pip or visit [here](https://docs.astral.sh/uv/getting-started/installation/)).
![Example on what it should look like](docs/assets/manual_py_ins.png)
- Run `python main.py` and your bot will start running, press Ctrl+C inside the terminal when you want to stop the bot.

---

## ⏾ Feedback & Collaboration:
Feel free to make discussions in [here](https://github.com/AzuritilDev/QuranBot/discussions) and report any bugs, mistakes etc. in the [issues](https://github.com/AzuritilDev/QuranBot/issues) section of the repository. <br />

Please check the repository's guide on [contributing](CONTRIBUTING.md) and [the code of conduct](CODE_OF_CONDUCT.md).

---

## ⏾ Authors:
[@AzuritilDev](https://github.com/AzuritilDev)


Made with passion & good intentions, <br />
gifted to the Ummah ❤️
## ⏾ License:
Distributed under [MIT](LICENSE.md) license.