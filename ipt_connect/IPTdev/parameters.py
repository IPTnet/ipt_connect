# -*- coding: utf-8 -*-

from get_script_dir import get_script_dir

# Here we get the name of the folder in which THIS FILE is located.
# It is probably NOT the current working directory.
# This trick is needed to simplify cloning the tournament,
# and, moreover, will (hopefully!) allow creating two tournaments with common parameters
# but different data by a simple symlink creation
# (don't forget to plug the new application to django).
instance_name = get_script_dir(False)
instance_name = list(reversed(instance_name.rsplit('/' ,1)))[0];
instance_name = list(reversed(instance_name.rsplit('\\',1)))[0];


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
npf = 4                 # Number of selective (qualifying) Physics fights
semifinals_quantity = 2 # Quantity of semifinals. Every semifinal should be a separate fight!
with_final_pf = True    # Is there a Final Fight ?
reject_malus = 0.2      # Malus for too many rejections
npfreject_max = 3       # Maximum number of tactical rejection (per fight)
netreject_max = 1       # Maximum number of eternal rejection

# Should we reset the point sum before semifinals?
# Does not affect reporter's coeff., rejections nor problems forbidden
reset_points_before_semi = False

# The same thing for the final - for the most pathological cases!
reset_points_before_final = True

# The maximum quantity of rounds
# Affects mostly the combobox in round admin interface
# Bonus points are calculated properly
max_rounds_in_pf = 4

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

# Are the bonus points displayed in the fight summary?
display_pf_summary_bonus_points = True


# Do we respect pools?
# If true, then the pool is displayed in ranking table
# and the 'Ranking' menu item leads to poolranking
enable_pools = True

# Are the bonus points entered manually?
# Switch this on in case of problems with bonus points
# If True: both global bonuses (the team form) and local bonuses (the round form) are visible and editable
# If False: both are invisible, global bonuses are not counted to the ranking
# Switching from False to True: local bonuses are preserved as counted, you can edit them manually
# Switching from True to False: local bonuses can be automatically overwritten,
# global bonuses are hidden and ignored so far
manual_bonus_points = False

# Do we display coreporters publicly?
display_coreporters = True

# There are at least 3 tournaments where rounds without a reviewer may (or must) appear:
# 1) Selective (qualifying) fights of virtual IPT 2020 (the main reason to add this option)
# 2) The final fight of Russian National Selection (if this shit can be named a "selection") stage of IYPT.
# 3) Theoretically, at Three Science Tournament, we can encounter such a situation, but that is rather exotic.
# Set this option to True if reviewers may be absent
optional_reviewers = True

# Maybe a Fight should be a separate model in the database
# However, it looks like the fight structure is defined far before the tournament starts,
# so you will have enough time to open this file and edit everything you want.
# If you think that I'm wrong, feel free to fork me!
fights = {
    # Bonus points multipliers
    # You can set it to 2 for semifinals or the last selective PFs to emphase the drama.
    # You can also set it to zero for the final with the same purpose!
    'bonus_multipliers' : [1,1,1,1,2,2,0],

    # Is there challenge procedure at the beginning of each round of the fight?
    # Some tournaments, such as Syberian IYPT, play the last selective PF without the challenge procedure
    # (i.e. like a Final: every team decides what to present)
    # This parameter influences (now) only on visibility of "Forbidden problems" block
    # while rendering the round detail
    'challenge_procedure': [True, True, True, True, True, True, False],

    # A situation when a team chooses a problem without challenge,
    # but there are problems which cannot be chosen, is easy to imagine
    # So, we have a separate setting for forbidden problems!
    'problems_forbidden': [True, True, True, True, True, True, False],

    # And, finally, you can specify names for all the fights to be displayed
    # Sometimes it is useful to name fights like "Day 1 - Fight 2", or "Fight By Choice",
    # or "Semifinal A", or smth another.
    'names': ['Selective Fight 1','Selective Fight 2','Selective Fight 3','Selective Fight 4','Semifinal 1','Semifinal 2',instance_name+' Final']
}
