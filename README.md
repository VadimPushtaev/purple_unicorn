# Purple Unicorn
Simple telegram bot with webhooks. It's good for being deployed on Heroku.

## What it can do (shortly)
* roll dice (such as 1d6, 1d20 and so on) even when they are part of complex expression (e.g. `(2d6 + 5)*3 - 1d20`). Or much more complex expression: `(3d10H2)d(5d20L1 + 10)`
* roll dice for group of characters and sort results (e.g. when everyone should roll initiative or make save throws)
* ask dndbeyond.com for information about spells, abilities and monsters
* send random messages or stickers with purple unicorn ( https://tlgrm.ru/stickers/UnicornStella ) if you want to speak with it
* just be cool

## What it can do (in details)
### Roll dice
1. Simple expressions:
  * `2d6` - roll 1d6 die 2 times
  * `(1d20 + 10)/2` - you can also use dice-rolls as part of any simple arithmetic expression
  * `(50+38.5+49)/3` - you even can use this  bot as arithmometer without rolling any dice
2. Complex expressions:
  * `5d10H2` - `'H<number>'` suffix means that you roll whatever is in front of it and then take and summarize only <number> highest results.
    Example: `5d10H2`. `5d10` produces `[4, 2, 2, 3, 1]`. According to `H2` we take 2 highest results from this set: `4` and `3`. Answer is `4+3=7`
  * `4d20L3` - `'L<number>'` suffix do the same but take only <number> of the lowest results.
    Example: `4d20L3`. `4d20` produces `[20, 6, 3, 9]`. According to `L3` we take 3 lowest results from this set: `6`, `3` and `9`. Answer is `6+3+9=18`
3. Very complex expressions:
  * `(7d10H4)d(5d20L1+10)H(1d5)` - expression may consists of any complex parts. Each of them will be counted to number which will be used in the next level of expression.
    Example: `(7d10H4)d(5d20L1+10)H(1d5)`. Result for `(7d10H4)` is `R1`, for `(5d20L1+10)` is `R2` and for `(1d5)` is `R3`. After counting those expressions we can use their results in the main part: `(7d10H4)d(5d20L1+10)H(1d5) = (R1)d(R2)H(R3)` - is the same as 'roll 1d(R2) die (R1) times and take (R3) highest results'.

## Used libs
* python-telegram-bot 5.3.0 - nice API for telegram
* dice-parser 0.6 - special parser for dice rolling by V.Pushtaev ( https://github.com/VadimPushtaev/dice_parser )
