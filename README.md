# Purple Unicorn
Simple telegram bot with webhooks. It's good for being deployed on Heroku.

## What it can do (shortly)
* roll dice (such as 1d6, 1d20 and so on) even when they are part of complex expression (e.g. `(2d6 + 5)*3 - 1d20`). Or much more complex expression: `(3d10H2)d(5d20L1 + 10)`
* roll dice for group of characters and sort results (e.g. when everyone should roll initiative or make save throws)
* flip a coin
* ask https://www.dndbeyond.com/ for information about spells, abilities and monsters
* send random messages or stickers with purple unicorn ( https://tlgrm.ru/stickers/UnicornStella ) if you want to speak with it
* just be cool

## What it can do (in details)
### Roll dice
#### Simple expressions:
* `2d6` - roll 1d6 die 2 times
* `(1d20 + 10)/2` - you can also use dice-rolls as part of any simple arithmetic expression
* `(50+38.5+49)/3` - you even can use this  bot as arithmometer without rolling any dice
#### Complex expressions:
* `5d10H2` - `'H<number>'` suffix means that you roll whatever is in front of it and then take and summarize only `<number>` highest results.
  
  *Example*: `5d10H2`. `5d10` produces `[4, 2, 2, 3, 1]`. According to `H2` we take 2 highest results from this set: `4` and `3`. Answer is `4+3=7`
* `4d20L3` - `'L<number>'` suffix do the same but take only `<number>` of the lowest results.
  
  *Example*: `4d20L3`. `4d20` produces `[20, 6, 3, 9]`. According to `L3` we take 3 lowest results from this set: `6`, `3` and `9`. Answer is `6+3+9=18`
#### Very complex expressions:
* `(7d10H4)d(5d20L1+10)H(1d5)` - expression may consists of any complex parts. Each of them will be counted to number which will be used in the next level of expression.
  
  *Example*: `(7d10H4)d(5d20L1+10)H(1d5)`. Result for `(7d10H4)` is `R1`, for `(5d20L1+10)` is `R2` and for `(1d5)` is `R3`. After counting those expressions we can use their results in the main part: `(7d10H4)d(5d20L1+10)H(1d5) = (R1)d(R2)H(R3)` - is the same as 'roll 1d(R2) die (R1) times and take (R3) highest results'.
### Group results
It is good for rolling 1d20 for a group of characters with personal bonuses and then sort results.

For example, we have a group consists of barbarian (with initiative bonus +2) and cleric (initiative -1) who meet orcs (initiative 2 and 1). So that's time for rolling initiative:

```/init barbarian=2 cleric=-1 orc1=1 orc2=1```

```Results:
barbarian : 15 (13 2 [1])
cleric    : 12 (13 -1 [4])
orc1      : 11 (10 1 [1])
orc2      : 5 (4 1 [10])
```

Results are already sorted. The main number for us is one from the second column (first column is for names) - this is result of `1d20 + bonus`, which are in the third and the fourth columns, accordingly. And the last one (in square bracers) is additional roll that would be used in conflicts (if there are all the same values in previous columns).

### Flip a coin
Just as it is named. Result is either 'heads' or 'tails'.

### Search information
Web-site https://dndbeyond.com/ has no normal API but it has a lot of information on D&D universe. Bot goes to that site, takes results of web-search, parse them, throws away results from forum ('cause they are almost irrelevant and stupid) and then shows what left. First result has its snippet, the rest have only title and breadcrumbs.

### Random talking
#### Say 'hello!'
Every time you greet bot, it will send you random message (they are supposed to be funny, or at least known for fans of computer RPG's or users who have seen a lot of memes in Internet) or a random sticker from 'Purple Unicorn' set.

#### Helping hand
Bot can give you information about all its commands as well as every command separately.

## Used libs
* python-telegram-bot 5.3.0 - nice API for telegram
* dice-parser 0.7 - special parser for dice rolling by V.Pushtaev ( https://github.com/VadimPushtaev/dice_parser )
* dndbeyond_websearch 0.2 - lib that allows to use web-search from dndbeyond.com. By V.Pushtaev, either ( https://github.com/VadimPushtaev/dndbeyond_websearch )

## Current states
Master: [![Build Status](https://semaphoreci.com/api/v1/graukin/purple_unicorn/branches/master/badge.svg)](https://semaphoreci.com/graukin/purple_unicorn)

Develop: [![Build Status](https://semaphoreci.com/api/v1/graukin/purple_unicorn/branches/develop/badge.svg)](https://semaphoreci.com/graukin/purple_unicorn)

Stable release: tag v4.4 (ba71dcd)
