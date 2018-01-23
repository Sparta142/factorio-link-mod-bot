# Factorio Link Mod Bot
[![Travis](https://img.shields.io/travis/Sparta142/factorio-link-mod-bot.svg)](https://travis-ci.org/Sparta142/factorio-link-mod-bot)
[![Coveralls github](https://img.shields.io/coveralls/github/Sparta142/factorio-link-mod-bot.svg)](https://coveralls.io/github/Sparta142/factorio-link-mod-bot)
[![Requires.io](https://img.shields.io/requires/github/Sparta142/factorio-link-mod-bot.svg)](https://requires.io/github/Sparta142/factorio-link-mod-bot/requirements/)

Reddit bot that links [Factorio mods](https://mods.factorio.com/) on request.

This project is a complete rewrite of the project fork at
[michael-3-141/FactorioModPortalBot](https://github.com/michael-3-141/FactorioModPortalBot).

## Usage (for Redditors)
* To link a single mod: `!linkmod Squeak Through`
* To link a list of mods (max 20): `!linkmods Bobingabout`

**Note:** The bot will only respond to the first command in each comment/submission.

## Installation
Run this in your favorite shell to install directly from GitHub:
```
$ pip install -e git+https://github.com/Sparta142/factorio-link-mod-bot.git#egg=factorio_link_mod_bot
```
