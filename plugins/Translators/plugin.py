# coding: utf-8
import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import re
from random import randint, randrange
import supybot.utils.web as web
import BeautifulSoup as BS
from urllib import urlencode
from os.path import join, dirname, abspath

HEADERS = dict(ua = 'Zoia/1.0 (Supybot/0.83; Sing Plugin; http://code4lib.org/irc)')
STOPWORDS = open(join(dirname(abspath(__file__)), 'stopwords.txt')).read().split()
        
class Translators(callbacks.Privmsg):
    def canuck(self, irc, msg, args):
        """ string
        Translates text into a Canadian dialect
        """
        text = ' '.join(args).strip()
        text = re.sub(r'z', 'zed', text)
        text = re.sub(r'(\w)or', '\1our', text)
        text = re.sub(r'gray', 'gray', text)
        text = re.sub(r'catalog(?![ui])', 'catalogue\1', text)
        # commenting these out for now since they make output from Weather ugly
        #text = re.sub(r'(24|twenty.four)', 'two-four', text)
        #text = re.sub(r'(6|six)', 'six-pack', text)
        text = re.sub(r'out', 'oat', text)
        text = re.sub(r'ouch', 'oach', text)
        text = re.sub(r'ache', 'awchee', text)
        matches = re.findall(r'((-?\d+)(\.\d+)?.F)', text)
        for match in matches:
            ftemp = float(match[1] + match[2])
            celsius = (ftemp - 32) * 5 / 9
            text = re.sub(match[0], "%-3.1fC" % celsius, text)
        irc.reply(text + ", eh?", prefixNick=True)

    def aussie(self, irc, msg, args):
        """ string
        Translates string into Australian English Vernacular
        """
        irc.reply("SHRIMP ON THE BARBIE, MATES!", prefixNick=True)

    def viking(self, irc, msg, args):
        """ string
        Translates string into Viking
        """
        irc.reply("SKÅL!", prefixNick=True)

    def ircnickize(self, irc, msg, args):
        """ string
        Normalizes a string per irc nick rules
        """
        nick = ''
        for arg in args:
            for s in arg.split():
                nick += s
        # strip out all non-word characters to make freenode happy
        nick = re.compile(r'\W', re.I).sub('', nick)        
        # string slice used because freenode restricts >16-char nicks
        irc.reply(nick[0:15], prefixNick=False)

    def mccainize(self, irc, msg, args):
        """
        Translates text into McCain speechifyin'
        """
        prefix = "My friends, " if randint(0,2) else "My fellow prisoners, "
        irc.reply(prefix + ' '.join(args), prefixNick=True)

    def dick(self, irc, msg, args):
        """
        Disclaims your desire to be a dick
        """
        irc.reply("I don't mean to be a dick, but " + ' '.join(args), prefixNick=True)
        
    def edsu(self, irc, msg, args):
        """
        States edsu's attitude on selfsame plugin command
        """
        irc.reply("let me remind you people, " + ' '.join(args), prefixNick=True)

    def kgs(self, irc, msg, args):
        """
        bad kgs imitation
        """
        irc.reply("nosrsly, " + ' '.join(args), prefixNick=True)


    def obamit(self, irc, msg, args):
        """
        Garners attention for your statements in a folksy way
        """
        look = "Look, " if randint(0,1) else "Look, here's what I'm saying... "
        irc.reply(look + ' '.join(args))

    def mjg(self, irc, msg, args):
        """
        Truncates and refocuses your statement
        """
        s = ' '.join(args)
        high = len(s)
        low = min(7, high-1)
        irc.reply("%s... OMG! Bacon!" % s[0:randint(low,high)])

    def embed(self, irc, msg, args):
        """
        Adds "in bed" to the end of a phrase.
        """
        s = ' '.join(args).strip(".")

        motivate = re.match(r'^(.*) - (.*)$', s)
        quote = re.match(r'^Quote #(\d+): "(.*)" \((.*)\)$', s)
        if motivate:
            msg = "%s ... in bed - %s" % (motivate.group(1), motivate.group(2))
        elif quote:
            msg = 'Quote #%sa "%s ... in bed" - (%s)' % quote.groups()
        else:
            msg = "%s ... in bed." % s

        irc.reply(msg)

    def scalia(self, irc, msg, args):
        """<string>
        random 'scare' quote insertion"""
        if len(args) == 0:
            irc.reply("try providing some text, morno")
            return
        words = []
        token_positions = []
        i = 0
        for arg in args:
            for s in arg.split():
                words.append(s)
                if s.strip(r'`!()-{}[]<>"\':;.,?').lower() not in STOPWORDS:
                    token_positions.append(i)
                i += 1
        try:
            randidx = randrange(len(token_positions))
            words[token_positions[randidx]] = "'%s'" % words[token_positions[randidx]]
        except:
            # all stopwords
            pass
        irc.reply(' '.join(words))

    def chef(self, irc, msg, args):
        """BORK! BORK! BORK!"""
        self._chefjivevalleypig(irc, 'chef', ' '.join(args))

    def jive(self, irc, msg, args):
        """Like, yeah..."""
        self._chefjivevalleypig(irc, 'jive', ' '.join(args))

    def valley(self, irc, msg, args):
        """Fer sure!"""
        self._chefjivevalleypig(irc, 'valspeak', ' '.join(args))

    def igpay(self, irc, msg, args):
        """Ustjay utwhay ouyay inkthay"""
        self._chefjivevalleypig(irc, 'piglatin', ' '.join(args))

    def _chefjivevalleypig(self, irc, type, s):
        params = urlencode(dict(input=s,type=type))
        url = 'http://www.cs.utexas.edu/users/jbc/bork/bork.cgi?' + params
        resp = web.getUrl(url, headers=HEADERS)
        resp = re.sub('\n', ' ', resp)
        irc.reply(resp.encode('utf-8', 'ignore').strip())


    def sabram(self, irc, msg, args):
        """ [<text>]
        Get @sabram to falsely attribute a quote to Cliff!
        """
        template = '<sabram> Cliff said: "%s"'
        if args:
            irc.reply(template % ' '.join(args))
            return
        url = "http://www.ivyjoy.com/quote.shtml"
        try:
            resp = web.getUrl(url, headers={'User-agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13'})
            soup = BS.BeautifulSoup(resp)
            quotation = soup.find('font').contents[0].strip()
        except:
            irc.reply(template % "Some stupid error occurred")
        irc.reply(template % quotation, prefixNick=False)
    
    def drunk(self, irc, msg, s):
        params = urlencode(dict(text=s,voice='drunk'))
        url = 'http://www.thevoicesofmany.com/text.php?' + params
        resp = web.getUrl(url, headers=HEADERS)
        soup = BS.BeautifulSoup(resp)
        try:
            translated = soup.find('td', id='top').blockquote.string
        except:
            irc.reply("oops, didn't work")
        irc.reply(resp.encode('utf-8', 'ignore').strip())
    
    def takify(self, irc, msg, args):
        """ĆẪṖĨṰĄŁȊȤḖŜ ĀÑƊ ȂḒƉŜ ȒẬÑḊỎḾ ḒÎḀĊṘĨŤİČṦ ƮǬ Ȁ ŞƮṞƗṆƓ Ȭℱ ƮỆẊṮ"""
        variants = {
            'A' : u'ÀÁÂÃĀĂȦÄẢÅǍȀȂĄẠḀẦẤẪẨẰẮẴẲǠǞǺẬẶ',
            'B' : u'ḂƁḄḆℬ',
            'C' : u'ĆĈĊČƇÇḈ©',
            'D' : u'ḊƊḌḎḐḒĎĐƉↁ',
            'E' : u'ÈÉÊẼĒĔĖËẺĚȄȆẸȨĘḘḚỀẾỄỂḔḖỆḜℰℇƎ',
            'F' : u'ḞƑℱℲ',
            'G' : u'ǴĜḠĞĠǦƓĢǤ',
            'H' : u'ĤḢḦȞǶḤḨḪĦℋℍ',
            'I' : u'ÌÍÎĨĪĬİÏỈǏỊĮȈȊḬƗḮ',
            'J' : u'Ĵ',
            'K' : u'ḰǨḴƘḲĶK',
            'L' : u'ĹḺḶĻḼĽĿŁḸℒ',
            'M' : u'ḾṀṂℳ',
            'N' : u'ǸŃÑṄŇŊƝṆŅṊṈ',
            'O' : u'ÒÓÔÕŌŎȮÖỎŐǑȌȎƠǪỌƟØỒỐỖỔȰȪȬṌṎṐṒỜỚỠỞỢǬỘǾ',
            'P' : u'ṔṖƤ℗ℙ',
            'Q' : u'Ԛ℺ℚ',
            'R' : u'ŔṘŘȐȒṚŖṞṜƦ®ℝℛℜ℟',
            'S' : u'ŚŜṠŠṢȘŞṤṦṨ',
            'T' : u'ṪŤƬƮṬȚŢṰṮŦ',
            'U' : u'ÙÚÛŨŪŬÜỦŮŰǓȔȖƯỤṲŲṶṴṸṺǛǗǕǙỪỨỮỬỰ',
            'V' : u'ṼṾ℣',
            'W' : u'ẀẂŴẆẄẈ',
            'X' : u'ẊẌ',
            'Y' : u'ỲÝŶỸȲẎŸỶƳỴ',
            'Z' : u'ŹẐŻŽȤẒẔƵ'
        }

        source = ' '.join(args).upper()
        result = []
        for letter in source:
            try:
                possibles = variants[letter]
            except KeyError:
                possibles = [letter]
            result.append(possibles[randrange(len(possibles))])
        response = u' '.join(result)
        irc.reply(response.encode('utf8', 'ignore'), prefixNick=False)
    
    def foxnews(self, irc, msg, args, text):
        """ <text>
        Use nebulous sources to present your own screwed-up viewpoint!
        """
        variants = [ 
            'Sources claim',
            'In fact, some have said',
            'Can you deny the rumors',
            'Official sources have yet to deny',
            ]
        variant = variants[randrange(len(variants))]
        irc.reply('%s that %s' % (variant, text), prefixNick=False)
        
    foxnews = wrap(foxnews, ['text'])

    def snowman(self, irc, msg, args):
        """ <text>
        UNICODE SNOWMAN ALL UP IN YA TEXT BRAW
        """
        text = u' '.join([arg.decode('utf8') for arg in args])
        response = u'☃'.join(list(text))
        irc.reply(response.encode('utf8', 'ignore'), prefixNick=False)
        
Class = Translators

