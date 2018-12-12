import argparse
import irc.bot
import re


class FishBot(irc.bot.SingleServerIRCBot):
    CMDS = {
        'aftershock' : 'mmmm, Aftershock.',
        'aftershock vinegar' : 'Ah, a true connoisseur!',
        'ag' : 'Ag, ag ag ag ag ag AG AG AG!',
        'ammuu?' : '{you}: fish go m00 oh yes they do!',
        'atlantis' : 'Beware the underwater headquarters of the trout and their bass henchmen. From there they plan their attacks on other continents.',
        'badger badger badger badger badger badger badger badger badger badger badger badger' : 'mushroom mushroom!',
        'bass' : 'Beware of the mutant sea bass and their laser cannons!',
        'bounce' : 'moo',
        'cake' : 'fish',
        'carrots handbags cheese.' : '...toilets russians planets hamsters weddings poets stalin KUALA LUMPUR! pygmys budgies KUALA LUMPUR!',
        'cows go moo' : '{you}: only when they are impersonating fish.',
        'crack' : 'Doh, there goes another bench!',
        'embenzalmine nitrotomine' : 'A pleasant-tasting, thirst-quenching drink, enjoyed by all.',
        'everyone is different' : 'No two people are not on fire.',
        'files don\'t just disappear!' : 'They do if you drop them down an elevator shaft...',
        'fish' : '{you}: fish go m00!',
        'fishbot' : 'Yes?',
        'fishbot created splidge' : 'omg no! Think I could show my face around here if I was responsible for THAT?',
        'fishbot: Muahahaha. Ph33r the dark side. :)' : '{you}: You smell :P.',
        'fishbot owns' : 'Aye, I do.',
        'fishcakes' : 'fish',
        'flibble' : 'plob',
        'hampster' : '{you}: There is no \'p\' in hamster you retard.',
        'hello fishbot' : 'Hi {you}!',
        'herring' : 'herring(n): Useful device for chopping down tall trees. Also moos (see fish).',
        'how much does fishbot cost' : 'Almost a thousand pounds.',
        'If there\'s one thing I know for sure, it\'s that fish don\'t m00.' : '{you}: HERETIC! UNBELIEVER!',
        'I know Kungfu' : 'Show me.',
        'imhotep' : 'Imhotep is invisible.',
        'I want everything' : 'Would that include a bullet from this gun?',
        'just then, he fell into the sea' : 'Ooops!',
        'Kangaroo' : 'The kangaroo is a four winged stinging insect.',
        'martian' : 'Don\'t run! We are your friends!',
        'moo?' : 'To moo, or not to moo, that is the question. Whether \'tis nobler in the mind to suffer the slings and arrows of outrageous fish...',
        'mr. slim' : 'Mr. Slim can be reached on extension 2754.',
        'no it isn\'t' : 'Yes it is!',
        'now there\'s more than one of them?' : 'A lot more.',
        'oh god' : 'fishbot will suffice.',
        'slaps person around a bit with a large trout' : 'trouted!',
        'sledgehammer' : 'sledgehammers go quack!',
        'snake' : 'Ah snake a snake! Snake, a snake! Ooooh, it\'s a snake!',
        'some people are about to be run over' : 'Frankie has about 5 seconds.',
        'some people are being fangoriously devoured by a gelatinous monster' : 'Hillary\'s legs are being digested.',
        'some people have rigged the enemy base with explosives' : 'Albert has.',
        'spoon' : 'There is no spoon.',
        'thanks fishbot' : 'Thishbot.',
        'trout' : 'Trout are freshwater fish and have underwater weapons.',
        'trout go moo' : 'Aye, that\'s cos they\'re fish.',
        'vinegar' : 'Nope, too sober for vinegar. Try later.',
        'vinegar aftershock' : 'Ah, a true connoisseur!',
        'we are getting aggravated' : 'Yes, we are.',
        'wertle' : 'moo',
        'what are birds?' : 'We just don\'t know.',
        'what does maths stand for?' : 'Mathematical Anti Telharsic Harfatum Septomin.',
        'what do you need?' : 'Guns. Lots of guns.',
        'what is the matrix?' : 'No-one can be told what the matrix is. You have to see it for yourself.',
        'where are we?' : 'Last time I looked, we were in {channel}.',
        'where do you want to go today?' : 'anywhere but redmond :(.',
        'why are you here?' : 'Same reason. I love candy.',
        'would you like to play a game?' : 'The only winning move is not to play.',
        'www.outwar.com' : 'would you please GO AWAY with that outwar rubbish!',
        'you can\'t just pick people at random!' : 'I can do anything I like, you, I\'m eccentric! Rrarrrrrgh! Go!',

        # some commands are responded by actions:
        'fish go moo': '*notes that {you} is truly enlightened.',
        'fish go m00': '*notes that {you} is truly enlightened.',
        'how old is fishbot?' : '*is older than time itself.',

        # some commands need further handling. The '*' at the and of the command is used to prevent matching without further processing.
        '!invite fishbot*' : 'Shan\'t.',
        'you know who else*' : '{you}: YA MUM!',
        'fish go*' : '{you} LIES! Fish don\'t go {group}! fish go m00!',
        'fishbot doesnt know about*' : 'Perhaps I\'m just not telling...',
    }

    CMDS_ACTION = {
        'feeds fishbot hundreds and thousands' : 'MEDI.. er.. FISHBOT',
        'has returned from playing counterstrike' : 'like we care fs :(',
        'mafipulates fishbot' : '*changes colour from invisible to brown.',
        'pours water on fishbot' : 'Ruined.',
        'snaffles a cookie off fishbot.' : ':(',
        'strokes fishbot' : '*m00s loudly at {you}.',

        'thinks happy thoughts about pretty*' : '*has plenty of pretty {group}. Would you like one, {you}?',
    }

    # Commands that need further handling due to additional arguments. Currently, re.match.group(2) will be used in the responses. 
    CMD_LIST = ['(!invite fishbot) ([#].+)',
        '(you know who else) (.+)',
        '(fish go) (.+)',
        '(fishbot doesnt know about) (.+)',
    ]
    CMD_ACTION_LIST = [
        '(thinks happy thoughts about pretty) (.+)\.' 
    ]

    def __init__(self, username,channels, host, port=6667, oauth_token=''):
        self.HOST = host
        self.PORT = port
        self.join_channels = channels
        if oauth_token:
            con = (self.HOST, self.PORT, 'oauth:' + oauth_token)
        else:
            con = (self.HOST, self.PORT)
        irc.bot.SingleServerIRCBot.__init__(self, [con], username, username)


    def on_welcome(self, c, e):
        for channel in self.join_channels:
            c.join("#"+channel)

    def on_ctcp(self,c,e):
        if e.arguments[0] == 'ACTION':
            self.do_command(e, e.arguments[1], self.CMDS_ACTION, self.CMD_ACTION_LIST)

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]
        if len(msg) > 1:
            self.do_command(e, msg, self.CMDS, self.CMD_LIST)
        
    def do_command(self, e, cmd, cmd_dict, cmd_list):
        nick = e.source.nick
        c = self.connection

        if not cmd in cmd_dict:
            response = ''
            for item in cmd_list:
                match = re.match(item, cmd)
                if match:
                    response = str(cmd_dict[match.group(1)+'*']).format(you=nick, channel=e.target, group=match.group(2))
                    break
        else:
            response = str(cmd_dict[cmd]).format(you=nick, channel=e.target)
        
        if response:
            if response[0] == '*':
                response = response[1:]
                c.action(e.target, response)
            else:
                c.privmsg(e.target, response)

def main():
    parser = argparse.ArgumentParser(description='Simple reimplementation of Quakenet\'s fishbot.')
    parser.add_argument('host', help='adress of the IRC server to connect to')
    parser.add_argument('-p', help='port of the IRC server ')
    parser.add_argument('nickname', help='nickname used by the bot')
    parser.add_argument('channels', help='list of channels to join without leading #. Example: "channel1,channel2" ')
    parser.add_argument('-o', help='optional OAuth token')

    args = parser.parse_args()

    token = ''
    if args.o:
        token = args.o

    channels = args.channels.split(',')
    port = 6667

    if args.p:
        port = args.p

    bot = FishBot(args.nickname, channels, args.host, port, oauth_token=token)
    bot.start()

if __name__ == "__main__":
    main()



