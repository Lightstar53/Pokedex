### Purpose and Usage

Service to run on a server using Flask with python and nginx for communication with a slack/discord bot for slash commands in channels.

for testing purposes functionality for /isitup that queries isitup.org's API has also been added.
example command (/isitup google.com):
* Yay, google.com appears to be up!
* Nope, google.com appears to be down!

example command (/isitup google)
* Whoops, isitup does not think google is a valid website, supply both domainname *AND* suffix (i.e amazon.com)

!['/isitup' example](http://puu.sh/nIXP1/677cbcbfe9.png)

-- Considering adding automagical .com if left out to try anyway, but not a priority.

Example usage (to be updated):
/dex help
!['/dex help' example](http://puu.sh/nPiJV/c327257428.png)

/dex and /pokedex are equal

/dex 123
* Pokemon #123 - Scyther
* Type(s): Flying, Bug
* Weaknesses: Electric, Fire, Flying, Ice, Rock x 4
* Resistances: Bug, Grass x 1/4, Fighting x 1/4
* Immunities: Ground


/dex litleo

An example pokemon query, '/pokedex pokemon LITLEO' would produce the same result. 
!['/dex litleo' example](http://puu.sh/nPhoX/ab68da452a.png)

/pokedex small 123
* Pokemon #123 - Scyther
* Type(s): Flying, Bug

/dex type grass silent
* The silent flag makes it private, neither the query or the response is shown to other users. 

!['/dex type grass silent' example](http://puu.sh/nPiu2/1e52a2abd4.png)

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
|  1  | normal | {grass, poison}    | {none}       | {electric} | {water}      | {psychic}   | 2016-03-12  |
|  2  | grass  | {normal, electric} | {normal}     | {water}    | {poison}     | {steel}     | 2016-03-17  |

###### Pokemon Table (WIP)
```
CREATE TABLE pokemon (
id int,
name text,
sprite text,
types text[],
weaknesses text[],
immunities text[],
resistances text[],
hiddens text[],
abilities text[],
updateTime date);
```

Example content (not accurate):

| id  | name   | sprite | types | weaknesses | resistances  | immunities | hiddens |  abilities | updateTime  |
| --- | ------ | ------ | ----- | ---------- | ------------ | ---------- | ------- | ---------- | ----------- |
| 1 | bulbasaur | http://example.com | {poison, grass} | {normal, dark} | {psychic, water} | {electric} | {chlorophyll} | {overgrow} | 2016-03-12 |
| 25 | pikachu | http://example.com| {electric} |{normal, electric} | {normal} | {water} | {lightning-rod} | {static} | 2016-03-17 |
