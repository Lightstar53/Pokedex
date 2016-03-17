### Purpose and Usage

Service to run on a server using Flask with python and nginx for communication with a slack/discord bot for slash commands in channels.

for testing purposes functionality for /isitup that queries isitup.org's API has also been added.
example command (/isitup google.com):
* Yay, google.com appears to be up!
* Nope, google.com appears to be down!

example command (/isitup google)
* Whoops, isitup does not think google is a valid website, supply both domainname *AND* suffix (i.e amazon.com)

![alt tag](http://puu.sh/nIXP1/677cbcbfe9.png)

-- Considering adding automagical .com if left out to try anyway, but not a priority.

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

### Installation / Requirements
* Web server capable of handling python
* python3(.5) with dependencies from requirements.txt
* Slack server with development access to enable integration with private tokens.

run $ pip3 install -r requirements.txt to automagically install dependencies. 

### Database Structure and Setup

###### Type Table
```
CREATE TABLE types (
id int,
name text,
immunities text[],
resistances text[],
weaknesses text[],
halfDamageTo text[],
noDamageTo text[],
updateTime date);
```
Example content (not accurate): 

| id  | name   | immunities         | resistances  | weaknesses | halfDamageTo | noDamageTo  | updateTime  |
| --- | ------ | ------------------ | ------------ | ---------- | ------------ | ----------- | ----------- |
|  1  | normal | [grass, poison}    | [none}       | [electric} | [water}      | [psychic}   | 2016-03-12  |
|  2  | grass  | [normal, electric} | [normal}     | [water}    | [poison}     | [steel}     | 2016-03-17  |

###### Pokemon Table (WIP)
```
CREATE TABLE pokemon (
id int,
name text,
immunities text[],
resistances text[],
weaknesses text[],
updateTime date);
```
Example content (not accurate):
To come...
