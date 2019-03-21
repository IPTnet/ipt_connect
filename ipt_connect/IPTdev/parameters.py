# -*- coding: utf-8 -*-

# Views parameters
app_version = "IPTdev"[3:]     # keyword for url parsing
# TODO:
# The construction `"IPTdev"[3:]` above is a dirty hack.
# We need to mention `IPTdev` to enable automated cloning,
# but we have to set version to `dev` to satisfy some pieces of code.
# No idea how is it handled for FPT.
# To be refactored:
# grep "app_version"


NAME = {
    'short': 'IPT dev',
    'full': 'International Physicists\' Tournament - Development Instance',
    # ... and the name used in tournament overview
    'front': '11th International Physicists\' Tournament',
}

poster_url = 'https://hsto.org/webt/zu/4_/cw/zu4_cwveq1izw4jst5yugtxng5q.png'

website_url = 'http://dev.iptnet.info'

repo_url = 'https://github.com/IPTnet/ipt_connect'

# Models parameters
npf = 4                 # Number of Physics fights
with_final_pf = True    # Is there a Final Fight ?
reject_malus = 0.2      # Malus for too many rejections
npfreject_max = 3       # Maximum number of tactical rejection (per fight)
netreject_max = 1       # Maximum number of eternal rejection


# The maximum quantity of rounds
# Affects mostly the combobox in round admin interface
# If you change it, make sure that bonus points are calculated properly!
# (spoiler: they are not, so switch them to be manual below)
max_rounds_in_pf = 3

# Personal ranking
personal_ranking = {
    'active': False,
    'rep_threshold': 5,
    'opp_threshold': 5,
    'rev_threshold': 5,
    'rep_coeff': 3,
    'opp_coeff': 2,
    'rev_coeff': 1
}

# Calculating the mean
mean = 'ipt_mean'  # String with name of function for calculating mean (ipt_mean or iypt_mean)

# Is the fight status displayed?
# Looks like there are some problems with it, so making it switchable
display_pf_status = True

# Is the fight summary displayed?
# Turn it off in case of any problems
display_pf_summary = True


# Do we respect pools?
# If true, then the pool is displayed in ranking table
# and the 'Ranking' menu item leads to poolranking
enable_pools = True


# Are the bonus points entered manually?
# Switch this on in case of problems with bonus points,
# which may especially occur for 4-round fights
# As for now, you MUST turn it to True if you have 4-round PFs !!!
# If True: both global bonuses (the team form) and local bonuses (the round form) are visible and editable
# If False: both are invisible, global bonuses are not counted to the ranking
# Switching from False to True: local bonuses are preserved as counted, you can edit them manually
# Switching from True to False: local bonuses are overwritten, global bonuses are hidden and ignored so far
manual_bonus_points = False

# Do we display coreporters publicly?
display_coreporters = True
