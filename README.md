# Knowledgebase Bot (kb-bot)

This repository contains code for the Interlock knowledgebase Discord bot. The concept was spawned from the interlock-kb [issue #46](https://github.com/interlock-network/interlock-kb/issues/46). So far, the intended design includes the following aspects:

```
~~ Preliminary design doc ~~

The temptation is to mirror bash, quite painfully so,
using flags to specify correlatives / else. IE:

kb-find <name>   -> return list of all matching files in kb
kb-find --who <name>   -> return list of all matching who files
kb-find --what <name>   -> ...

kb-ls   -> return list of all correlatives
kb-ls --who   -> return "who" correlative files
kb-ls --what   -> ...

kb-grep <string>   -> return all instances of string
kb-grep --who <string>   -> return all instances of string in "who"
kb-grep --what <string>   -> ...

kb-help   -> return basically a simple man page
kb-<command> --help   -> return help for specific command
.
.
.
etc
```
```
INCLUDE THIS FUNCTIONALITY:
kbot scoops up tagged tidbits from RT discord chat
and shoves them onto relevant discussion thread.
```
## Dependencies:

- Python 3.8
- Discord.py
- PyGithub

## Setup:

A detailed overview for setup is [found here](https://realpython.com/how-to-make-a-discord-bot-python/).

Otherwise, the order of operations goes like so:

1. Get Discord acount.
2. Create Discord application to get token which you will paste [here]().
3. Build and deploy the kb-bot to your particular server.
