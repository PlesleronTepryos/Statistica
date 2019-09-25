"""Grammar spec for Statistica's commands"""

GRAMMAR = r"""
# Start symbol for the grammar
START: statement;
statement: {generate_stmt userstats_stmt statestats_stmt runstats_stmt madlibs_stmt help_stmt about_stmt invite_stmt ignore_stmt blacklist_stmt quit_stmt restart_stmt recompile_stmt config_stmt forget_stmt dumplogs_stmt};

# Interaction commands
generate_stmt: generate {state len users}*;
userstats_stmt: userstats users;
statestats_stmt: statestats {phrase STRING} users?;
runstats_stmt: runstats {phrase STRING} users?;
madlibs_stmt: madlibs {phrase STRING} users?;

# Information commands
help_stmt: help {name setting}?;
about_stmt: about;
invite_stmt: invite;

# Permissioned commands
ignore_stmt: ignore {'add' 'remove'} {user_mention channel_mention 'me'};
blacklist_stmt: blacklist {'add' 'remove'} {user_mention channel_mention};

# Hidden commands
quit_stmt: quit;
restart_stmt: restart;
recompile_stmt: recompile;
config_stmt: config setting {STRING NUMBER}*;
forget_stmt: forget users;
dumplogs_stmt: dumplogs (NUMBER (NUMBER NUMBER?)?)?; 

# Publicly accessible command names
name: {generate userstats statestats runstats madlibs help about invite forget ignore blacklist};

# Command name aliases
generate: {'generate' 'g'};
userstats: {'userstats' 'u'};
statestats: {'statestats' 's'};
runstats: {'runstats' 'r'};
madlibs: {'madlibs' 'm'};

help: {'help' 'h'};
about: {'about' 'a'};
invite: {'invite' 'i'};

ignore: 'ignore';
blacklist: 'blacklist';

quit: {'quit' 'q'};
restart: 'restart';
recompile: {'recompile' 'recomp'};
config: {'config' 'cfg'};
forget: 'forget';
dumplogs: {'dumplogs' 'dl'};

# Argument symbols
len: 'l=' NUMBER;
state: 's=' STRING;
users: 'u=' {STRING expr};
phrase: 'p=' STRING;
user_mention: '<@!' NUMBER '>';
channel_mention: '<#!' NUMBER '>';
setting: {'state_size' 'owners' 'output_color' 'error_color' 'logging_level' 'filter'};

# Expression syntax
expr: '(' or_expr ')';
or_expr: and_expr ('OR' and_expr)*;
and_expr: not_expr ('AND' not_expr)*;
not_expr: {('NOT' {not_expr expr atom}) expr atom};
atom: {NUMBER STRING};

# Regex-based terminal symbols
STRING: '"(?:\\.|[^"\\])*"'$;
NUMBER: '\d*\.?\d+'$;
"""
