# Factorio Link Mod Bot
[![Travis](https://img.shields.io/travis/Sparta142/factorio-link-mod-bot.svg)](https://travis-ci.org/Sparta142/factorio-link-mod-bot)
[![Coveralls github](https://img.shields.io/coveralls/github/Sparta142/factorio-link-mod-bot.svg)](https://coveralls.io/github/Sparta142/factorio-link-mod-bot)
[![Requires.io](https://img.shields.io/requires/github/Sparta142/factorio-link-mod-bot.svg)](https://requires.io/github/Sparta142/factorio-link-mod-bot/requirements/)

Reddit bot that links [Factorio mods](https://mods.factorio.com/) on request.

This project is a complete rewrite of the project fork at
[michael-3-141/FactorioModPortalBot](https://github.com/michael-3-141/FactorioModPortalBot).

## Usage (for Redditors)
* To link a single mod: `linkmod: Squeak Through`
* To link a list of mods (max 20): `linkmods: Bobingabout`

**Note:** You can use more than one command at once, but the response will 
always be capped at 20 results.  
**Note 2:** The bot will only respond to comments, not submissions 
(i.e., self posts).

## Installation
Run this in your favorite shell to install directly from GitHub:
```
$ pip install -e git+https://github.com/Sparta142/factorio-link-mod-bot.git#egg=factorio_link_mod_bot
```

### Configuration
This project only uses environment variables for configuration.
This makes it ideal for deployment to Heroku or other similar PaaS.

* `REDDIT_CLIENT_ID` - The Reddit application ID.
* `REDDIT_CLIENT_SECRET` - The Reddit application secret.
* `REDDIT_USERNAME` - The Reddit username to sign in with.
* `REDDIT_PASSWORD` - The Reddit password to sign in with.
* `REDDIT_USER_AGENT` - The user agent reported to Reddit.
* `REDDIT_SUBREDDITS` - Comma-separated list of subreddits to monitor for commands.
* `FACTORIO_USER_AGENT` - The user agent reported to the Factorio mod portal.
