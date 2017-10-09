import json
import operator
import urllib2

qtrdict = {'1':1, '2':2, '3':3, '4':4, '5':5, 'Final':6}

def makeTicker(clock, qtr, down, togo, yl):
    gameover = False
    if qtrdict[qtr] == 5:
        qtr = 'OT'
    elif qtrdict[qtr] == 6:
        qtr = 'Final'
        gameover = True
    else:
        qtr = 'Q' + qtr
    
    downdict = {1:'1st', 2:'2nd', 3:'3rd', 4:'4th'}

    if gameover:
        tickerstr = '**Final**'
    else:
        tickerstr = '**{} {}** | {} & {} on {}'.format(clock, qtr, 
                downdict[down], str(togo), yl)

    return tickerstr

def makeBoxscore(sdaway, sdhome, teamaway, teamhome, teampos, qtr):
    gameover = False
    overtime = False
    scoredict = ['1', '2', '3', '4', '5', 'T']

    if qtrdict[qtr] == 6:
        gameover = True
        topstr = '|| 1st | 2nd | 3rd | 4th | FT\n-|:-:|:-:|:-:|:-:|:-:'
    elif qtrdict[qtr] == 5:
        topstr = '|| 1st | 2nd | 3rd | 4th | OT | T\n-|:-:|:-:|:-:|:-:|:-:|:-:'
        overtime = True
    else:
        topstr = '|| 1st | 2nd | 3rd | 4th | T\n-|:-:|:-:|:-:|:-:|:-:'

    scraway, scrhome = ['-']*6, ['-']*6

    for i in range(qtrdict[qtr]):
        tempaway = str(sdaway[scoredict[i]])
        temphome = str(sdhome[scoredict[i]])
        scraway[i] = tempaway
        scrhome[i] = temphome
    
    scraway[5] = sdaway[scoredict[5]]
    scrhome[5] = sdhome[scoredict[5]]

    if not overtime:
        del scraway[4]
        del scrhome[4]

    if teampos == teamaway:
        teamaway+=' *'
    else:
        teamhome+=' *'

    awaystr = '{} | {} | {} | {} | {} | {}'.format(teamaway, *scraway)
    homestr = '{} | {} | {} | {} | {} | {}'.format(teamhome, *scrhome)

    bsstr = '{}\n{}\n{}'.format(topstr, awaystr, homestr)

    return bsstr

def makePassing(passaway, passhome):
    topstr = 'Passing | Cmp/Att | Yds | TDs | Ints\n-|:-:|:-:|:-:|:-:'

    spa = sorted(passaway.values(), key = operator.itemgetter('yds','tds'),
            reverse = True)
    sph = sorted(passhome.values(), key = operator.itemgetter('yds','tds'),
            reverse = True)
    
    passawaystr = '{} | {}/{} | {} | {} | {}'.format(spa[0]['name'], spa[0]['cmp'],
            spa[0]['att'], spa[0]['yds'], spa[0]['tds'], spa[0]['ints'])
    passhomestr = '{} | {}/{} | {} | {} | {}'.format(sph[0]['name'], sph[0]['cmp'],
            sph[0]['att'], sph[0]['yds'], sph[0]['tds'], sph[0]['ints'])

    passstr = '{}\n{}\n{}'.format(topstr, passawaystr, passhomestr)

    return passstr

def makeRushing(rushaway, rushhome):
    topstr = 'Rushing | Att | Yds | Long | TDs\n-|:-:|:-:|:-:|:-:'

    sra = sorted(rushaway.values(), key = operator.itemgetter('yds','tds'),
            reverse = True)
    srh = sorted(rushhome.values(), key = operator.itemgetter('yds','tds'),
            reverse = True)
    
    rushawaystr0 = '{} | {} | {} | {} | {}'.format(sra[0]['name'], sra[0]['att'],
            sra[0]['yds'], sra[0]['lng'], sra[0]['tds'])
    rushawaystr1 = '{} | {} | {} | {} | {}'.format(sra[1]['name'], sra[1]['att'],
            sra[1]['yds'], sra[1]['lng'], sra[1]['tds'])

    rushhomestr0 = '{} | {} | {} | {} | {}'.format(srh[0]['name'], srh[0]['att'],
            srh[0]['yds'], srh[0]['lng'], srh[0]['tds'])
    rushhomestr1 = '{} | {} | {} | {} | {}'.format(srh[1]['name'], srh[1]['att'],
            srh[1]['yds'], srh[1]['lng'], srh[1]['tds'])

    rushstr = '{}\n{}\n{}\n{}\n{}'.format(topstr, rushawaystr0, rushawaystr1,
            rushhomestr0, rushhomestr1)

    return rushstr

def makeReceiving(recaway, rechome):
    topstr = 'Receiving | Catches | Yds | Long | TDs\n-|:-:|:-:|:-:|:-:'

    sra = sorted(recaway.values(), key = operator.itemgetter('yds','tds'),
            reverse = True)
    srh = sorted(rechome.values(), key = operator.itemgetter('yds','tds'),
            reverse = True)
    
    recawaystr0 = '{} | {} | {} | {} | {}'.format(sra[0]['name'], sra[0]['rec'],
            sra[0]['yds'], sra[0]['lng'], sra[0]['tds'])
    recawaystr1 = '{} | {} | {} | {} | {}'.format(sra[1]['name'], sra[1]['rec'],
            sra[1]['yds'], sra[1]['lng'], sra[1]['tds'])

    rechomestr0 = '{} | {} | {} | {} | {}'.format(srh[0]['name'], srh[0]['rec'],
            srh[0]['yds'], srh[0]['lng'], srh[0]['tds'])
    rechomestr1 = '{} | {} | {} | {} | {}'.format(srh[1]['name'], srh[1]['rec'],
            srh[1]['yds'], srh[1]['lng'], srh[1]['tds'])

    recstr = '{}\n{}\n{}\n{}\n{}'.format(topstr, recawaystr0, recawaystr1,
            rechomestr0, rechomestr1)

    return recstr
    
if __name__ == '__main__':
    #These will change from week to week. Right now they'd have to be entered by
    #hand, but it is possible to figure them out ahead of time and automate it.
    gameurl = 'http://www.nfl.com/liveupdate/game-center/2017100811/2017100811_gtd.json'
    gameid = '2017100811'

    response = urllib2.urlopen(gameurl)
    rawdata = json.loads(response.read())

    game = rawdata[gameid]

    #clock
    clock = game['clock']

    #quarter
    qtr = game['qtr']

    #down
    down = game['down']

    #togo
    togo = game['togo']

    #yardline
    yl = game['yl']

    #possession
    posteam = game['posteam']

    #score
    scorehome = game['home']['score']
    scoreaway = game['away']['score']

    #teams
    teamaway = game['away']['abbr']
    teamhome = game['home']['abbr']

    #stats
    paway = game['away']['stats']['passing']
    phome = game['home']['stats']['passing']
    ruaway = game['away']['stats']['rushing']
    ruhome = game['home']['stats']['rushing']
    reaway = game['away']['stats']['receiving']
    rehome = game['home']['stats']['receiving']

    ticker = makeTicker(clock, qtr, down, togo, yl)

    boxscore = makeBoxscore(scoreaway, scorehome, teamaway, teamhome, posteam, qtr)

    passing = makePassing(paway, phome)

    rushing = makeRushing(ruaway, ruhome)

    receiving = makeReceiving(reaway, rehome)

    gamestr = '{}\n\n{}\n\n{}\n\n{}\n\n{}'.format(ticker, boxscore, passing, rushing, receiving)

    print gamestr
