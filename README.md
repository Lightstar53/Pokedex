# PokedexService

Service to run on a server for communication with slack/discord for slash command/bot usage in channels.

Example usage (to be updated):
/dex and /pokedex are equal

/dex 123
> Pokemon #123 - Scyther
> Type(s): Flying, Bug
> Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
> Resistances: Bug, Grass x 1/4, Fighting x 1/4
> Immunities: Ground
> Bulbapedia: http://bulbapedia.bulbagarden.net/wiki/Scyther_(Pok%C3%A9mon)

/dex Scyther
> Pokemon #123 - Scyther
> Type(s): Flying, Bug
> Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
> Resistances: Bug, Grass x 1/4, Fighting x 1/4
> Immunities: Ground
> Bulbapedia: http://bulbapedia.bulbagarden.net/wiki/Scyther_(Pok%C3%A9mon)

/pokedex Scyther
> Pokemon #123 - Scyther
> Type(s): Flying, Bug
> Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
> Resistances: Bug, Grass x 1/4, Fighting x 1/4
> Immunities: Ground
> Bulbapedia: http://bulbapedia.bulbagarden.net/wiki/Scyther_(Pok%C3%A9mon)

/pokedex small 123
> > Pokemon #123 - Scyther
> Type(s): Flying, Bug
