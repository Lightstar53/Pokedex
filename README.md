### Purpose and Usage

Service intended to run on a server running Flask (uWSGI), communicating with a slack/discord server as a bot for slash commands in channels. 

Future ideas include Who's that pokemon trivia game, and various other tidbits of pokemon information. See issues for more detail. Pull requests and collaborators are encouraged. 

Functionality for /isitup that queries isitup.org's API has also been added. (To check for slack connectivity early on. We won't remove it because why not.)
example command (/isitup google.com):
* Yay, google.com appears to be up!
* Nope, google.com appears to be down!

### Example usage (to be updated):
Full list of current commands are:
* /dex [pokemon]
* /dex type [type]
* /dex ability [ability}
* /dex move [move]
* /dex help

where all [] are either the name, or id, i.e bulbasaur/1, or grass/12 etc. **All** commands can be made silent (only visible to the querying user) by adding a silent flag at the end.
* /dex bulbasaur silent
* /dex type grass silent
* /dex ability own-tempo


![alt tag](http://puu.sh/nPhoX/ab68da452a.png)
![alt tag](https://puu.sh/sC5hM/b9be0707ba.png)

/dex and /pokedex are equal

/dex 123
* Pokemon #123 - Scyther
* Type(s): Flying, Bug
* Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
* Resistances: Bug, Grass x 1/4, Fighting x 1/4
* Immunities: Ground

/dex Scyther
* Pokemon #123 - Scyther
* Type(s): Flying, Bug
* Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
* Resistances: Bug, Grass x 1/4, Fighting x 1/4
* Immunities: Ground

/dex ability own-tempo
* Ability #20 - Own Tempo
* This Pokémon cannot be confused. If a Pokémon is confused and acquires this ability, its confusion will immediately be healed.
* Data was last updated: 2016-12-02. 

/dex type grass
* Type #12:
* Grass
* *Weaknesses*: Bug, Fire, Flying, Ice, Poison.
* *Resistances*: Electric, Grass, Ground, Water.
* *Immunities*: None.
* *Resisted by*: Bug, Dragon, Fire, Flying, Grass, Poison, Steel.
* *Ineffective against*: None.

Data was last updated: 2016-11-28 


### Installation / Requirements
* Web server capable of handling python
* postgresql database running locally (unless you change the code, it looks for access information in dbInfo.secret currently)
* python3(.5) with dependencies from requirements.txt
* Slack server with development access to enable integration with private tokens.

run $ pip3 install -r requirements.txt to automagically install dependencies. 

The program looks for a validTokens.secret, and a dbInfo.secret that are outside of version control to get DB login information and what slack tokens are valid for security reasons. These files should be located next to the code files, in /classes. 

### Database Structure and Setup
See (or run) createTables.sql for table structure details. 

###### Type Table
Example content (not accurate): 

| id  | name   | immunities         | resistances  | weaknesses | halfDamageTo | noDamageTo  | updateTime  |
| --- | ------ | ------------------ | ------------ | ---------- | ------------ | ----------- | ----------- |
|  1  | normal | {grass, poison}    | {none}       | {electric} | {water}      | {psychic}   | 2016-03-12  |
|  2  | grass  | {normal, electric} | {normal}     | {water}    | {poison}     | {steel}     | 2016-03-17  |

###### Pokemon Table (WIP)

Example content (not factually accurate):

| id  | name   | sprite | types | weaknesses | resistances  | immunities | hiddens |  abilities | updateTime  |
| --- | ------ | ------ | ----- | ---------- | ------------ | ---------- | ------- | ---------- | ----------- |
| 1 | bulbasaur | http://example.com | {poison, grass} | {normal, dark} | {psychic, water} | {electric} | {chlorophyll} | {overgrow} | 2016-03-12 |
| 25 | pikachu | http://example.com| {electric} |{normal, electric} | {normal} | {water} | {lightning-rod} | {static} | 2016-03-17 |
