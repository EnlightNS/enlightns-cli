#
# Bash auto-completion functionality.
# To install the bash completion execute the two following command lines:
#
# enlightns-cli bash >> ~/.bashrc
# source ~/.bashrc
#

#
# GENERATING THIS FILE
# _ENLIGHTNS_CLI_COMPLETE=source enlightns-cli > bash-complete.sh
#

# enlightns-cli bash completion
_enlightns_cli_completion()
{
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _ENLIGHTNS_CLI_COMPLETE=complete $1 ) )
    return 0
}

complete -F _enlightns_cli_completion -o default enlightns-cli;
# enlightns-cli bash completion end
