import trueskill
import ConfigParser

rank_file = 'rank.config'


def get_player_list():
    parser = ConfigParser.SafeConfigParser()
    parser.read(rank_file)

    return parser.sections()

def add_player(name):
    name = name.lower().strip()
    parser = ConfigParser.SafeConfigParser()
    parser.read(rank_file)

    r = trueskill.Rating()

    parser.add_section(name.lower())
    parser.set(name, 'mu', str(r.mu))
    parser.set(name, 'sigma', str(r.sigma))
    parser.set(name, 'games', str(0))
    parser.set(name, 'wins', str(0))
    parser.set(name, 'losses', str(0))

    with open(rank_file, 'w') as f:
        parser.write(f)

    return r


def get_player_rank(name):
    name = name.lower().strip()
    parser = ConfigParser.SafeConfigParser()
    parser.read(rank_file)

    try:
        r = trueskill.Rating(
                mu=    parser.getfloat(name, 'mu'),
                sigma= parser.getfloat(name, 'sigma'))
    except ConfigParser.NoSectionError:
        return add_player(name)

    return r


def set_player_rank(name, rank, extra=None):
    name = name.lower().strip()
    parser = ConfigParser.SafeConfigParser()
    parser.read(rank_file)

    parser.set(name, 'mu', str(rank.mu))
    parser.set(name, 'sigma', str(rank.sigma))

    if extra:
        g = parser.getint(name, 'games') + extra['games']
        w = parser.getint(name,'wins') + extra['wins']
        l = parser.getint(name,'losses') + extra['losses']
        parser.set(name, 'games', str(g))
        parser.set(name, 'wins', str(w))
        parser.set(name, 'losses', str(l))

    with open(rank_file, 'w') as f:
        parser.write(f)


def get_rank_list():
    parser = ConfigParser.ConfigParser()
    parser.read(rank_file)

    rank_list = []

    players = parser._sections
    for name in players:
        temp = []
        section = players[name]
        temp.append(name)
        temp.append(float(section['mu']))
        temp.append(float(section['sigma']))
        temp.append(int(section['games']))
        temp.append(int(section['wins']))
        temp.append(int(section['losses']))
        rank_list.append(temp)

    rank_list.sort(key=lambda x:x[1], reverse=True)
    return rank_list

def add_game(winners, lossers):
    t_win = []
    t_loss = []

    for winner in winners:
        t_win.append(get_player_rank(winner))

    for losser in lossers:
        t_loss.append(get_player_rank(losser))

    t_win, t_loss = trueskill.rate([t_win, t_loss], ranks=[0, 1])

    for index, winner in enumerate(winners):
        set_player_rank(winner, t_win[index], extra={'games':1,'wins':1,'losses':0})

    for index, losser in enumerate(lossers):
        set_player_rank(losser, t_loss[index], extra={'games':1,'wins':0,'losses':1})

    return get_rank_list()
