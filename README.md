# PokedexService

Service to run on a server for communication with slack/discord for slash command/bot usage in channels.

for testing purposes functionality for /isitup that queries isitup.org's API has also been added.
example command:
* /isitup google.com
Results can be:
* Yay, google.com appears to be up!
* Nope, google.com appears to be down!
* Whoops, isitup does not think google is a valid website, supply both domainname *AND* suffix (i.e amazon.com)

Intended usage when finished (to be updated):
/dex and /pokedex are equal

/dex 123
* Pokemon #123 - Scyther
* Type(s): Flying, Bug
* Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
* Resistances: Bug, Grass x 1/4, Fighting x 1/4
* Immunities: Ground
* Bulbapedia: http://bulbapedia.bulbagarden.net/wiki/Scyther_(Pok%C3%A9mon)

/dex Scyther
* Pokemon #123 - Scyther
* Type(s): Flying, Bug
* Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
* Resistances: Bug, Grass x 1/4, Fighting x 1/4
* Immunities: Ground
* Bulbapedia: http://bulbapedia.bulbagarden.net/wiki/Scyther_(Pok%C3%A9mon)

/pokedex Scyther
* Pokemon #123 - Scyther
* Type(s): Flying, Bug
* Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
* Resistances: Bug, Grass x 1/4, Fighting x 1/4
* Immunities: Ground
* Bulbapedia: http://bulbapedia.bulbagarden.net/wiki/Scyther_(Pok%C3%A9mon)

/pokedex small 123
* Pokemon #123 - Scyther
* Type(s): Flying, Bug
