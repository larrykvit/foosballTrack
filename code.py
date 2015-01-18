import web
import foosballTrack

urls = (
    '/', 'index'
    )

render = web.template.render('templates/')

input = web.form.Form(
    web.form.Textbox('winners', web.form.notnull),
    web.form.Textbox('losers', web.form.notnull),
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
            winners = f['winners'].value.split(',')
            lossers = f['losers'].value.split(',')
            rank_list = foosballTrack.add_game(winners, lossers)
            return render.index(f, rank_list)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()