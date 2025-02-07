
# WIN

- mostly just read the code

Widgets were explained in widgets.md
So we'll go over other individual important parts that are not widgets

## FILE_HANDLER

`handlers.py` `FILE_HANDLER`
`WIN.file_handler` is responsbile for handling `BUFFER`s and `BUFFER_TAB`s as well as creating them, loading them and generally managing their existence, `BUFFER`s specifically `TEXT`s are tied to files so `WIN.file_handler` is also responsible for opening, creating, deleting files. So anything pertaining to files (except for commands) should be located there


## COMMAND_PARSER

`command_parser.py`, `PARSER`
`WIN.parser` is responsible for managing and executing commands inputted through `WIN.command_entry`.
All commands should be there.
What happens generally is a command goes through `WIN.command_entry` -> `WIN.parser.parse_argument(arg=[input command])`
Which parses the command splits it into command and it's arguments and looks up the command in `PARSER.commands` and passes the arguments into the corresponding function (if there is one)
