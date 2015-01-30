import web
import foosballTrack

urls = (
    '/', 'index'
    )

render = web.template.render('templates/')

name_list = ['none'] + foosballTrack.get_player_list()

input = web.form.Form(
    web.form.Dropdown('Winner 1:', name_list),
    web.form.Dropdown('Winner 2:', name_list),
    web.form.Dropdown('Losser 1:', name_list),
    web.form.Dropdown('Losser 2:', name_list),
    web.form.Button('Add game'),
    )

class index:
    def GET(self):
        f = input()
        rank_list = foosballTrack.get_rank_list()
        return render.index(f, rank_list)

    def POST(self):
        f = input()
        if not f.validates():
            rank_list = foosballTrack.get_rank_list()
            return render.index(f, rank_list)
        else:
            winners = []
            if f['Winner 1:'].value is not 'none':
                winners += [f['Winner 1:'].value]
            if f['Winner 2:'].value is not 'none':
                winners += [f['Winner 2:'].value]

            lossers = []
            if f['Losser 1:'].value is not 'none':
                lossers += [f['Losser 1:'].value]
            if f['Losser 2:'].value is not 'none':
                lossers += [f['Losser 2:'].value]

            rank_list = foosballTrack.add_game(winners, lossers)
            return render.index(f, rank_list)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()