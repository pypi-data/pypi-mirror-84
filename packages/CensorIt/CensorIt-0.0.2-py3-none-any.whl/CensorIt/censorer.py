swears=['anus', 'arse', 'arsehole', 'ass', 'ass hat', 'ass jabber', 'ass pirate', 'ass hat', 'ass jabber', 'ass pirate', 'assbag', 'assbandit', 'assbanger', 'assbite', 'assclown', 'asscock', 'asscracker', 'asses', 'assface', 'assfuck', 'assfucker', 'assgoblin', 'asshat', 'asshead', 'asshole', 'asshopper', 'assjacker', 'asslick', 'asslicker', 'assmonkey', 'assmunch', 'assmuncher', 'assnigger', 'asspirate', 'assshit', 'assshole', 'asssucker', 'asswad', 'asswipe', 'axwound', 'fuck', 'shit', 'sex', 'porn', 'dick', 'penis', 'vagina', 'pussy', 'cum', 'cock', 'bampot', 'bastard', 'beaner', 'bitch', 'bitchass', 'bitches', 'bitchtits', 'bitchy', 'blow-job', 'blowjob', 'bollocks', 'bollox', 'boner', 'brotherfucker', 'bullshit', 'bumblefuck', 'butt plug', 'butt-pirate', 'buttfucka', 'buttfucker', 'fu', 'anal', 'anus', 'arse', 'ass', 'ass-fuck', 'ass-hole', 'assfucker', 'asshole', 'assshole', 'bastard', 'bitch', 'black-cock', 'bloody-hell', 'boong', 'cock', 'cockfucker', 'cocksuck', 'cocksucker', 'coon', 'coonnass', 'crap', 'cunt', 'cyberfuck', 'damn', 'darn', 'dick', 'dirty', 'douche', 'dummy', 'erect', 'erection', 'erotic', 'escort', 'fag', 'faggot', 'fuck', 'fuck-off', 'fuck-you', 'fuckass', 'fuckhole', 'god-damn', 'gook', 'hard-core', 'hardcore', 'homoerotic', 'hore', 'lesbian', 'lesbians', 'mother fucker', 'motherfuck', 'motherfucker', 'negro', 'nigger', 'orgasim', 'orgasm', 'penis', 'penisfucker', 'piss', 'piss-off', 'porn', 'porno', 'pornography', 'pussy', 'retard', 'sadist', 'sex', 'sexy', 'shit', 'slut', 'son-of-a-bitch', 'suck', 'tits', 'viagra', 'whore', 'xxx', 'fuck', 'blowjob', 'cum', 'jizz', 'boner', 'clit', 'handjob', 'poontang', 'queef', 'dildo', 'rimjob', 'feltch', 'minge', 'spooge', 'smegma', 'pecker', 'pussy', 'cock', 'boobs', 'piss', 'cunt', 'tits', 'dick', 'balls', 'twat', 'taint', 'pubes', 'prick', 'hard-on', 'turd', 'nuts', 'nutsack', 'motherfucker', 'asshole', 'bullshit', 'shitfaced', 'cocksucker', 'buttcrack', 'clusterfuck', 'douchebag', 'dickhead', 'dumbass', 'fuckface', 'shithead', 'buttfuck', 'dipshit', 'asshat', 'bumblefuck', 'shit', 'goddamn', 'jesus-christ', 'screw', 'crap', 'slut', 'hell', 'jagoff', 'vag', 'wank', 'arse', 'bugger', 'cameltoe', 'bollocks', 'choad', 'cabron', 'testicle']
def censor(inp):
    out=""
    inp2=inp
    for c in swears:
        hashes = ""
        for h in range(len(c)):
            hashes = hashes + "*"
        inp2=inp2.replace(c,hashes)
    words = inp2.split()
    for a in words:
        if a.lower() in swears:
            hashes=""
            for b in range(len(a)):
                hashes=hashes+"*"
            out = out+" "+hashes
        else:
            out= out+" "+a
    return out
def check(inp):
    inp1=inp.replace('*','')
    out=""
    inp2=inp1
    for c in swears:
        hashes = ""
        for h in range(len(c)):
            hashes = hashes + "*"
        inp2=inp2.replace(c,hashes)
    words = inp2.split()
    for a in words:
        if a.lower() in swears:
            hashes=""
            for b in range(len(a)):
                hashes=hashes+"*"
            out = out+" "+hashes
        else:
            out= out+" "+a
    if '*' in out:
        cursefound=True
    else:
        cursefound=False
    return cursefound