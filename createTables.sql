CREATE TABLE types (
	id int,
	name text,
	immunities text[],
	resistances text[],
	weaknesses text[],
	halfDamageTo text[],
	noDamageTo text[],
	updateTime date
);

CREATE TABLE IF NOT EXISTS pokemon (
	id int,
	name text,
	sprite text,
	types text[],
	weaknesses text[],
	immunities text[],
	resistances text[],
	hiddens text[],
	abilities text[],
	updateTime date
);

CREATE TABLE IF NOT EXISTS moves (
	id int,
	name text,
	type text,
	target text,
	power int,
	accuracy int,
	basePP int,
	critRate int,
	flavorText text,
	updateTime date
);

CREATE TABLE IF NOT EXISTS abilities (
	id int,
	name text,
	flavorText text,
	updateTime date
);
