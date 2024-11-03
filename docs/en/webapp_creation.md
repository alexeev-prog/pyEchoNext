# pyEchoNext / creating a web application

---

Creating an application is not difficult in pyEchoNext. Thanks to its modularity and versatility, you can configure many settings and use different methods for creating web application routes.

> The required module to import can be indicated in parentheses, i.e. where this abstraction is stored. ex. EchoNext (pyechonext.app): from echonext.app import EchoNext

The main one is the EchoNext class (pyechonext.app):

```python

echonext = Echonext(app_name: str,

settings: Settings,

middlewaries: List[BaseMiddleware]

urls: Optional[List[URL]],

application_type: Optional[ApplicationType])

```


noun
    the place or type of surroundings where something is positioned or where an event takes place.
        - "cozy waterfront cottage in a peaceful country setting"
    Synonyms: surroundings, position, situation, environment, background, backdrop, milieu, environs, habitat, spot, place, location, locale, site, scene, context, frame, area, neighborhood, region, district, mise en scène

    a piece of metal in which a precious stone or gem is fixed to form a piece of jewelry.
        - "a garnet in a heavy gold setting"
    Synonyms: mounting, mount, fixture, surround

    a piece of vocal or choral music composed for particular words.
        - "a setting of Yevtushenko's bleak poem"

    short for place setting.

    a speed, height, or temperature at which a machine or device can be adjusted to operate.
        - "if you find the room getting too hot, check the thermostat setting"

Synonyms
    noun
        - locus
        - surroundings, position, situation, environment, background, backdrop, milieu, environs, habitat, spot, place, location, locale, site, scene, context, frame, area, neighborhood, region, district, mise en scène
        - mounting, mount, fixture, surround

See also
    setting

This argument is an instance of the Settings dataclass (pyechonext.config).

```python

@dataclass

class Settings:

"""

This class describes settings.

"""

BASE_DIR: str

TEMPLATES_DIR: str

```

Create an instance:

```python

settings = Settings(

BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"

)

```

BASE_DIR - base directory of the application file, TEMPLATES_DIR - directory of html templates (for the built-in template engine or Jinja2).

Also, from version 0.4.3 you can use a special settings loader. At the moment, it allows you to load settings from three types of files:

+ env file (environment variables)

+ ini file

+ pymodule (python module)

To use it, import:

```python

from pyechonext.config import SettingsLoader, SettingsConfigType

```

SettingsLoader is the loader, and SettingsConfigType is an enum class with types of config files.

SettingsLoader accepts the following arguments: `config_type: SettingsConfigType, filename: str`. To get settings you need to call the `get_settings()` method. It returns an object of the Settings data class, which can be immediately passed to the EchoNext application.

SettingsConfigType contains the following values:

```python

class SettingsConfigType(Enum):

"""

This class describes a settings configuration type.

"""

THIS = 'this'

DOTENV = 'dotenv'

PYMODULE = 'pymodule'

```

Examples of config loading:

### DOTENV

```python

config_loader = SettingsLoader(SettingsConfigType.DOTENV, 'example_env')

settings = config_loader.get_settings()

```

example_env file:

```env

PEN_BASE_DIR=.

PEN_TEMPLATES_DIR=templates

```

### THIS

```python

config_loader = SettingsLoader(SettingsConfigType.INI, 'example_ini.ini')

settings = config_loader.get_settings()

```

File example_ini.ini:

```this


noun
    the place or type of surroundings where something is positioned or where an event takes place.
        - "cozy waterfront cottage in a peaceful country setting"
    Synonyms: surroundings, position, situation, environment, background, backdrop, milieu, environs, habitat, spot, place, location, locale, site, scene, context, frame, area, neighborhood, region, district, mise en scène

    a piece of metal in which a precious stone or gem is fixed to form a piece of jewelry.
        - "a garnet in a heavy gold setting"
    Synonyms: mounting, mount, fixture, surround

    a piece of vocal or choral music composed for particular words.
        - "a setting of Yevtushenko's bleak poem"

    short for place setting.

    a speed, height, or temperature at which a machine or device can be adjusted to operate.
        - "if you find the room getting too hot, check the thermostat setting"

Synonyms
    noun
        - locus
        - surroundings, position, situation, environment, background, backdrop, milieu, environs, habitat, spot, place, location, locale, site, scene, context, frame, area, neighborhood, region, district, mise en scène
        - mounting, mount, fixture, surround

See also
    setting

BASE_DIR=.

TEMPLATES_DIR=templates

```

### PyModule

```python

config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'example_module.py')

settings = config_loader.get_settings()

```

Example_module.py file:

```python

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = 'templates'

```


noun
    software that acts as a bridge between an operating system or database and applications, especially on a network.

Middlewares - "middleware". The BaseMiddleware class looks like this:

```python

class BaseMiddleware(ABC):

"""

This abstract class describes a base middleware.

"""

@abstractmethod

def to_request(self, request: Request):

"""

To request method

:param      request:  The request

:type       request:  Request

"""

raise NotImplementedError

@abstractmethod

def to_response(self, response: Response):

"""

To response method

:param      response:  The response

:type       response:  Response

"""

raise NotImplementedError

```

To create your own Middleware, you need to create a new class based on this class and be sure to implement the to_request and to_response methods. pyEchoNext has a basic Middleware for creating sessions:

```python

class SessionMiddleware(BaseMiddleware):

"""

This class describes a session (cookie) middleware.

"""

def to_request(self, request: Request):

"""

Set to request

:param      request:  The request

:type       request:  Request

"""

cookie = request.environ.get('HTTP_COOKIE', None)



if not cookie:


verb
    come or go back to a place or person.
        - "he returned to Canada in the fall"
    Synonyms: go back, come back, get back, arrive back, arrive home, come home, come again

    give, put, or send (something) back to a place or person.
        - "complete the application form and return it to this address"
    Synonyms: restore, put back, replace, reinstate, reinstall

    yield or make (a profit).
        - "the company returned a profit of 4.3 million dollars"
    Synonyms: yield, bring in, earn, make, realize, secure, net, gross, clear, pay out, fetch, pocket

    (of an electorate) elect (a person or party) to office.
        - "the Democrat was returned in the third district"
    Synonyms: elect, vote in, put in power, choose, opt for, select, pick, adopt

    continue (a wall) in a changed direction, especially at right angles.

noun
    an act of coming or going back to a place or activity.
        - "he celebrated his safe return from the war"
    Synonyms: homecoming, travel back

    a profit from an investment.
        - "product areas are being developed to produce maximum returns"
    Synonyms: yield, profit, returns, gain, income, revenue, interest, dividend, percentage

    an official report or statement submitted in response to a formal demand.
        - "census returns"
    Synonyms: statement, report, submission, account, paper, record, file, dossier, write-up, data, information, log, journal, diary, register, summary, document, form

    election to office.
        - "we campaigned for the return of Young and Elkins"

    a key pressed to move the carriage of an electric typewriter back to a fixed position.

    a part receding from the line of the front, for example the side of a house or of a window opening.

Synonyms
    verb
        - go back, come back, get back, arrive back, arrive home, come home, come again
        - recrudesce
        - happen again, recur, reoccur, occur again, be repeated, repeat (itself), come around (again), reappear, appear again, flare up
        - give back, send back, hand back, take back, carry back, pay back, repay, remit
        - restore, put back, replace, reinstate, reinstall
        - reciprocate, requite, feel/give in return, repay, send/give in response, give back, match, equal, wish someone the same
        - answer, reply, respond, say in response, acknowledge, counter, rejoin, riposte, retort, retaliate, hurl back, fling back, snap back, round on someone, come back
        - hit back, send back, throw back
        - deliver, bring in, hand down, render, submit, announce, pronounce, proclaim
        - yield, bring in, earn, make, realize, secure, net, gross, clear, pay out, fetch, pocket
        - elect, vote in, put in power, choose, opt for, select, pick, adopt

    noun
        - homecoming, travel back
        - recrudescence, renascence
        - recurrence, reoccurrence, repeat, rerun, repetition, reappearance, flare-up, revival, rebirth, renaissance, resurrection, reawakening, re-emergence, resurgence
        - reinstalment
        - giving back, handing back, replacement, restoration, reinstatement, reinstallation, restitution
        - returned item, unsold item, unwanted item/ticket, reject, exchange
        - bunce
        - yield, profit, returns, gain, income, revenue, interest, dividend, percentage
        - statement, report, submission, account, paper, record, file, dossier, write-up, data, information, log, journal, diary, register, summary, document, form

Examples
    - a return flight

    - he celebrated his safe return from the war

    - complete the application form and return it to this address

    - we demand the return of our books and papers

    - the designer advocated a return to elegance

    - we campaigned for the return of Young and Elkins

    - the aim is to make the other side unable to return the ball

session_id = parse_qs(cookie)['session_id'][0]

request.extra['session_id'] = session_id

def to_response(self, response: Response):

"""

Set to response

:param      response:  The response

:type       response:  Response

"""

if not response.request.session_id:

response.add_headers([

("Set-Cookie", f'session_id={uuid4()}'),

])

```

There is also a basic list of `middlewares` in pyechonext.middleware to pass as arguments to EchoNext:

```python

middlewares = [

SessionMiddleware

]

```

This way you can import it and use or add to it.


noun
    the address of a web page.
        - "type a URL into a browser's address bar"

See also
    URL

By default, `urls` is an empty list. urls contains instances of the URL dataclass (pyechonext.urls):

```python

@dataclass

class URL:

url: str

view: Type[View]

```

View is an abstraction of the site route (django-like). It must have two methods: `get` and `post` (to respond to get and post requests). These methods should return:

+ Data, page content. This can be a dictionary or a string.

OR:

+ Response class object (pyechonext.response)

View is an object of the View class (pyechonext.views):

```python

class View(ABC):

"""


noun
    an instance of an internet user visiting a particular page on a website.

"""

@abstractmethod

def get(self, request: Request, response: Response, *args, **kwargs) -> Union[Response, Any]:

"""


verb
    come to have or hold (something); receive.
        - "I got the impression that she wasn't happy"
    Synonyms: retrieve, regain (possession of), win back, recover, take back, recoup, reclaim, repossess, recapture, retake, redeem, find (again), track down, trace, claw back, replevin, replevy

    succeed in attaining, achieving, or experiencing; obtain.
        - "I need all the sleep I can get"

    enter or reach a specified state or condition; become.
        - "it's getting late"
    Synonyms: wax

    come, go, or make progress eventually or with some difficulty.
        - "I got to the airport"
    Synonyms: return, come home, come back, arrive home, arrive back, come again

    see have.

    catch or apprehend (someone).
        - "the police have got him"
    Synonyms: apprehend, catch, arrest, capture, seize, take, take prisoner, take captive, take into custody, detain, put in jail, throw in jail, put behind bars, imprison, incarcerate

    understand (an argument or the person making it).
        - "What do you mean? I don't get it"
    Synonyms: understand, comprehend, grasp, see, take in, fathom, follow, puzzle out, work out, perceive, apprehend, get to the bottom of, unravel, decipher, get the drift of, catch onto, latch onto, make head or tail of, figure out, get the picture, get the message, twig, suss out, suss

    acquire (knowledge) by study; learn.
        - "knowledge which is gotten at school"

noun
    an animal's offspring.
        - "he passes this on to his get"

Synonyms
    verb
        - get one's hands on, get one's mitts on, get hold of, grab, bag, score, swing, nab, collar, cop
        - acquire, obtain, come by, come to have, come into possession of, receive, gain, earn, win, come into, come in for, take possession of, take receipt of, be given, buy, purchase, procure, possess oneself of, secure, gather, collect, pick up, appropriate, amass, build up, hook, net, land, achieve, attain
        - receive, be sent, be in receipt of, accept delivery of, be given
        - retrieve, regain (possession of), win back, recover, take back, recoup, reclaim, repossess, recapture, retake, redeem, find (again), track down, trace, claw back, replevin, replevy
        - experience, suffer, be afflicted with, undergo, sustain, feel, have
        - take ill with, take sick with
        - succumb to, develop, go/come down with, sicken for, fall victim to, be struck down with, be stricken with, be afflicted by/with, be smitten by/with, become infected with/by, catch, contract, become ill/sick with, fall ill/sick with, be taken ill with, show symptoms of, go down with
        - fetch, collect, go for, call for, pick up, bring, carry, deliver, convey, ferry, transport, escort, conduct, lead, usher
        - travel by/on/in, journey by/on/in, take, catch, use, make use of, utilize
        - become, grow, turn, go, come to be, get to be
        - wax
        - persuade, induce, prevail on, influence, talk around, wheedle into, talk into, cajole into, inveigle into, win over, bring around, sway
        - work it, fix it
        - contrive, arrange, find a way, engineer a way, manage, succeed in, organize
        - compass
        - show up, show, roll in, roll up, blow in, show one's face
        - arrive, reach, come, make it, turn up, appear, put in an appearance, make an appearance, come on the scene, come up, approach, enter, present oneself, be along, come along, materialize
        - return, come home, come back, arrive home, arrive back, come again
        - collar, grab, nab, nail, run in, bust, pick up, pull in, haul in, do, feel someone's collar, pinch, nick
        - apprehend, catch, arrest, capture, seize, take, take prisoner, take captive, take into custody, detain, put in jail, throw in jail, put behind bars, imprison, incarcerate
        - take revenge on, be revenged on, exact/wreak revenge on, get one's revenge on, avenge oneself on, take vengeance on, get even with, settle a/the score with, pay back, pay out, retaliate on/against, get back at, take reprisals against, exact retribution on, give someone their just deserts, give someone a dose/taste of their own medicine, give/return like for like, give tit for tat, take an eye for an eye (and a tooth for a tooth), give someone their comeuppance, get one's own back on
        - annoy, irritate, exasperate, anger, irk, vex, inflame, put out, nettle, needle, provoke, incense, infuriate, madden, rub up the wrong way, try someone's patience, make someone's blood boil, ruffle someone's feathers, make someone's hackles rise, get someone's hackles up, rattle someone's cage, aggravate, peeve, miff, rile, get to, hack off, get someone's back up, get on someone's nerves, get under someone's skin, get someone's goat, get someone's dander up, get in someone's hair, be a thorn in someone's flesh, drive mad, drive crazy, drive nuts, make someone see red, wind up, nark, get across, get someone's wick, give someone the hump, get up someone's nose, tee off, tick off, eat, burn up
        - flummox, discombobulate, faze, stump, beat, fox, make someone scratch their head, floor, fog
        - baffle, nonplus, perplex, puzzle, bewilder, mystify, bemuse, confuse, confound, disconcert, throw, set someone thinking
        - wilder, gravel, maze, cause to be at a stand, pose
        - hear, recognize, discern, distinguish, make out, pick out, perceive, follow, keep up with, take in
        - understand, comprehend, grasp, see, take in, fathom, follow, puzzle out, work out, perceive, apprehend, get to the bottom of, unravel, decipher, get the drift of, catch onto, latch onto, make head or tail of, figure out, get the picture, get the message, twig, suss out, suss

:param		request:   The request

:type		request:   Request

:param		response:  The response

:type		response:  Response

:param		args:	   The arguments

:type		args:	   list

:param		kwargs:	   The keywords arguments

:type		kwargs:	   dictionary

"""

raise NotImplementedError

@abstractmethod

def post(self, request: Request, response: Response, *args, **kwargs) -> Union[Response, Any]:

"""


noun
    a long, sturdy piece of timber or metal set upright in the ground and used to support something or as a marker.
        - "follow the blue posts until the track meets a forestry road"
    Synonyms: palisade

    a piece of writing, image, or other item of content published online, typically on a blog or on social media.
        - "in a recent post, he cautioned investors to be wary of these predictions"

    one of a series of couriers who carried mail on horseback between fixed stages.

    a position of paid employment; a job.
        - "he resigned from the post of Foreign Minister"

    a place where someone is on duty or where a particular activity is carried out.
        - "a worker asleep at his post"

    the status or rank of full-grade captain in the Royal Navy.
        - "Captain Miller was made post in 1796"

    work done on a film or recording after filming or recording has taken place.
        - "the rest of the effects were added in post"

verb
    display (a notice) in a public place.
        - "a curt notice had been posted on the door"
    Synonyms: affix, attach, fasten, hang, display, pin (up), put up, stick (up), tack (up), nail (up)

    publish (a piece of writing, image, or other item of content) online, typically on a blog or on social media.
        - "she posted a photo of herself with the singer on Twitter"

    announce or publish (something, especially a financial result).
        - "the company posted a $460,000 loss"
    Synonyms: announce, report, make known, advertise, publish, publicize, circulate, broadcast

    (of a player or team) achieve or record (a particular score or result).
        - "he posted a victory in Japan to lead the series"

    (in bookkeeping) enter (an item) in a ledger.
        - "post the transaction in the second column"
    Synonyms: record, write in, enter, fill in, register, note, list

    travel with relays of horses.
        - "we posted in an open carriage"

    send (someone) to a particular place to take up an appointment.
        - "he was posted to Washington as military attaché"

adverb
    with haste.
        - "come now, come post"

preposition
    subsequent to; after.
        - "American poetry post the 1950s hasn't had the same impact"

prefix
    after in time or order.
        - "postdate"

    behind in position.

Synonyms
    noun
        - puncheon, shore
        - pole, stake, upright, shaft, prop, support, picket, strut, pillar, pale, paling, column, piling, standard, stanchion, pylon, stave, rod, newel, baluster, jamb, bollard, mast, fence post, gatepost, finger post, king post, milepost
        - palisade

    verb
        - affix, attach, fasten, hang, display, pin (up), put up, stick (up), tack (up), nail (up)
        - announce, report, make known, advertise, publish, publicize, circulate, broadcast
        - record, write in, enter, fill in, register, note, list

:param		request:   The request

:type		request:   Request

:param		response:  The response

:type		response:  Response

:param		args:	   The arguments

:type		args:	   list

:param		kwargs:	   The keywords arguments

:type		kwargs:	   dictionary

"""

raise NotImplementedError

```

For example, pyechonext.views has an IndexView, an example View implementation.

```python

class IndexView(View):

def get(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:

"""


verb
    come to have or hold (something); receive.
        - "I got the impression that she wasn't happy"
    Synonyms: retrieve, regain (possession of), win back, recover, take back, recoup, reclaim, repossess, recapture, retake, redeem, find (again), track down, trace, claw back, replevin, replevy

    succeed in attaining, achieving, or experiencing; obtain.
        - "I need all the sleep I can get"

    enter or reach a specified state or condition; become.
        - "it's getting late"
    Synonyms: wax

    come, go, or make progress eventually or with some difficulty.
        - "I got to the airport"
    Synonyms: return, come home, come back, arrive home, arrive back, come again

    see have.

    catch or apprehend (someone).
        - "the police have got him"
    Synonyms: apprehend, catch, arrest, capture, seize, take, take prisoner, take captive, take into custody, detain, put in jail, throw in jail, put behind bars, imprison, incarcerate

    understand (an argument or the person making it).
        - "What do you mean? I don't get it"
    Synonyms: understand, comprehend, grasp, see, take in, fathom, follow, puzzle out, work out, perceive, apprehend, get to the bottom of, unravel, decipher, get the drift of, catch onto, latch onto, make head or tail of, figure out, get the picture, get the message, twig, suss out, suss

    acquire (knowledge) by study; learn.
        - "knowledge which is gotten at school"

noun
    an animal's offspring.
        - "he passes this on to his get"

Synonyms
    verb
        - get one's hands on, get one's mitts on, get hold of, grab, bag, score, swing, nab, collar, cop
        - acquire, obtain, come by, come to have, come into possession of, receive, gain, earn, win, come into, come in for, take possession of, take receipt of, be given, buy, purchase, procure, possess oneself of, secure, gather, collect, pick up, appropriate, amass, build up, hook, net, land, achieve, attain
        - receive, be sent, be in receipt of, accept delivery of, be given
        - retrieve, regain (possession of), win back, recover, take back, recoup, reclaim, repossess, recapture, retake, redeem, find (again), track down, trace, claw back, replevin, replevy
        - experience, suffer, be afflicted with, undergo, sustain, feel, have
        - take ill with, take sick with
        - succumb to, develop, go/come down with, sicken for, fall victim to, be struck down with, be stricken with, be afflicted by/with, be smitten by/with, become infected with/by, catch, contract, become ill/sick with, fall ill/sick with, be taken ill with, show symptoms of, go down with
        - fetch, collect, go for, call for, pick up, bring, carry, deliver, convey, ferry, transport, escort, conduct, lead, usher
        - travel by/on/in, journey by/on/in, take, catch, use, make use of, utilize
        - become, grow, turn, go, come to be, get to be
        - wax
        - persuade, induce, prevail on, influence, talk around, wheedle into, talk into, cajole into, inveigle into, win over, bring around, sway
        - work it, fix it
        - contrive, arrange, find a way, engineer a way, manage, succeed in, organize
        - compass
        - show up, show, roll in, roll up, blow in, show one's face
        - arrive, reach, come, make it, turn up, appear, put in an appearance, make an appearance, come on the scene, come up, approach, enter, present oneself, be along, come along, materialize
        - return, come home, come back, arrive home, arrive back, come again
        - collar, grab, nab, nail, run in, bust, pick up, pull in, haul in, do, feel someone's collar, pinch, nick
        - apprehend, catch, arrest, capture, seize, take, take prisoner, take captive, take into custody, detain, put in jail, throw in jail, put behind bars, imprison, incarcerate
        - take revenge on, be revenged on, exact/wreak revenge on, get one's revenge on, avenge oneself on, take vengeance on, get even with, settle a/the score with, pay back, pay out, retaliate on/against, get back at, take reprisals against, exact retribution on, give someone their just deserts, give someone a dose/taste of their own medicine, give/return like for like, give tit for tat, take an eye for an eye (and a tooth for a tooth), give someone their comeuppance, get one's own back on
        - annoy, irritate, exasperate, anger, irk, vex, inflame, put out, nettle, needle, provoke, incense, infuriate, madden, rub up the wrong way, try someone's patience, make someone's blood boil, ruffle someone's feathers, make someone's hackles rise, get someone's hackles up, rattle someone's cage, aggravate, peeve, miff, rile, get to, hack off, get someone's back up, get on someone's nerves, get under someone's skin, get someone's goat, get someone's dander up, get in someone's hair, be a thorn in someone's flesh, drive mad, drive crazy, drive nuts, make someone see red, wind up, nark, get across, get someone's wick, give someone the hump, get up someone's nose, tee off, tick off, eat, burn up
        - flummox, discombobulate, faze, stump, beat, fox, make someone scratch their head, floor, fog
        - baffle, nonplus, perplex, puzzle, bewilder, mystify, bemuse, confuse, confound, disconcert, throw, set someone thinking
        - wilder, gravel, maze, cause to be at a stand, pose
        - hear, recognize, discern, distinguish, make out, pick out, perceive, follow, keep up with, take in
        - understand, comprehend, grasp, see, take in, fathom, follow, puzzle out, work out, perceive, apprehend, get to the bottom of, unravel, decipher, get the drift of, catch onto, latch onto, make head or tail of, figure out, get the picture, get the message, twig, suss out, suss

:param		request:   The request

:type		request:   Request

:param		response:  The response

:type		response:  Response

:param		args:	   The arguments

:type		args:	   list

:param		kwargs:	   The keywords arguments

:type		kwargs:	   dictionary

"""

return "Hello World!"

def post(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:

"""


noun
    a long, sturdy piece of timber or metal set upright in the ground and used to support something or as a marker.
        - "follow the blue posts until the track meets a forestry road"
    Synonyms: palisade

    a piece of writing, image, or other item of content published online, typically on a blog or on social media.
        - "in a recent post, he cautioned investors to be wary of these predictions"

    one of a series of couriers who carried mail on horseback between fixed stages.

    a position of paid employment; a job.
        - "he resigned from the post of Foreign Minister"

    a place where someone is on duty or where a particular activity is carried out.
        - "a worker asleep at his post"

    the status or rank of full-grade captain in the Royal Navy.
        - "Captain Miller was made post in 1796"

    work done on a film or recording after filming or recording has taken place.
        - "the rest of the effects were added in post"

verb
    display (a notice) in a public place.
        - "a curt notice had been posted on the door"
    Synonyms: affix, attach, fasten, hang, display, pin (up), put up, stick (up), tack (up), nail (up)

    publish (a piece of writing, image, or other item of content) online, typically on a blog or on social media.
        - "she posted a photo of herself with the singer on Twitter"

    announce or publish (something, especially a financial result).
        - "the company posted a $460,000 loss"
    Synonyms: announce, report, make known, advertise, publish, publicize, circulate, broadcast

    (of a player or team) achieve or record (a particular score or result).
        - "he posted a victory in Japan to lead the series"

    (in bookkeeping) enter (an item) in a ledger.
        - "post the transaction in the second column"
    Synonyms: record, write in, enter, fill in, register, note, list

    travel with relays of horses.
        - "we posted in an open carriage"

    send (someone) to a particular place to take up an appointment.
        - "he was posted to Washington as military attaché"

adverb
    with haste.
        - "come now, come post"

preposition
    subsequent to; after.
        - "American poetry post the 1950s hasn't had the same impact"

prefix
    after in time or order.
        - "postdate"

    behind in position.

Synonyms
    noun
        - puncheon, shore
        - pole, stake, upright, shaft, prop, support, picket, strut, pillar, pale, paling, column, piling, standard, stanchion, pylon, stave, rod, newel, baluster, jamb, bollard, mast, fence post, gatepost, finger post, king post, milepost
        - palisade

    verb
        - affix, attach, fasten, hang, display, pin (up), put up, stick (up), tack (up), nail (up)
        - announce, report, make known, advertise, publish, publicize, circulate, broadcast
        - record, write in, enter, fill in, register, note, list

:param		request:   The request

:type		request:   Request

:param		response:  The response

:type		response:  Response

:param		args:	   The arguments

:type		args:	   list

:param		kwargs:	   The keywords arguments

:type		kwargs:	   dictionary

"""

return "Message has accepted!"

```

This implementation returns a string. But you can also return Response:

```python

class IndexView(View):

def get(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:

"""


verb
    come to have or hold (something); receive.
        - "I got the impression that she wasn't happy"
    Synonyms: retrieve, regain (possession of), win back, recover, take back, recoup, reclaim, repossess, recapture, retake, redeem, find (again), track down, trace, claw back, replevin, replevy

    succeed in attaining, achieving, or experiencing; obtain.
        - "I need all the sleep I can get"

    enter or reach a specified state or condition; become.
        - "it's getting late"
    Synonyms: wax

    come, go, or make progress eventually or with some difficulty.
        - "I got to the airport"
    Synonyms: return, come home, come back, arrive home, arrive back, come again

    see have.

    catch or apprehend (someone).
        - "the police have got him"
    Synonyms: apprehend, catch, arrest, capture, seize, take, take prisoner, take captive, take into custody, detain, put in jail, throw in jail, put behind bars, imprison, incarcerate

    understand (an argument or the person making it).
        - "What do you mean? I don't get it"
    Synonyms: understand, comprehend, grasp, see, take in, fathom, follow, puzzle out, work out, perceive, apprehend, get to the bottom of, unravel, decipher, get the drift of, catch onto, latch onto, make head or tail of, figure out, get the picture, get the message, twig, suss out, suss

    acquire (knowledge) by study; learn.
        - "knowledge which is gotten at school"

noun
    an animal's offspring.
        - "he passes this on to his get"

Synonyms
    verb
        - get one's hands on, get one's mitts on, get hold of, grab, bag, score, swing, nab, collar, cop
        - acquire, obtain, come by, come to have, come into possession of, receive, gain, earn, win, come into, come in for, take possession of, take receipt of, be given, buy, purchase, procure, possess oneself of, secure, gather, collect, pick up, appropriate, amass, build up, hook, net, land, achieve, attain
        - receive, be sent, be in receipt of, accept delivery of, be given
        - retrieve, regain (possession of), win back, recover, take back, recoup, reclaim, repossess, recapture, retake, redeem, find (again), track down, trace, claw back, replevin, replevy
        - experience, suffer, be afflicted with, undergo, sustain, feel, have
        - take ill with, take sick with
        - succumb to, develop, go/come down with, sicken for, fall victim to, be struck down with, be stricken with, be afflicted by/with, be smitten by/with, become infected with/by, catch, contract, become ill/sick with, fall ill/sick with, be taken ill with, show symptoms of, go down with
        - fetch, collect, go for, call for, pick up, bring, carry, deliver, convey, ferry, transport, escort, conduct, lead, usher
        - travel by/on/in, journey by/on/in, take, catch, use, make use of, utilize
        - become, grow, turn, go, come to be, get to be
        - wax
        - persuade, induce, prevail on, influence, talk around, wheedle into, talk into, cajole into, inveigle into, win over, bring around, sway
        - work it, fix it
        - contrive, arrange, find a way, engineer a way, manage, succeed in, organize
        - compass
        - show up, show, roll in, roll up, blow in, show one's face
        - arrive, reach, come, make it, turn up, appear, put in an appearance, make an appearance, come on the scene, come up, approach, enter, present oneself, be along, come along, materialize
        - return, come home, come back, arrive home, arrive back, come again
        - collar, grab, nab, nail, run in, bust, pick up, pull in, haul in, do, feel someone's collar, pinch, nick
        - apprehend, catch, arrest, capture, seize, take, take prisoner, take captive, take into custody, detain, put in jail, throw in jail, put behind bars, imprison, incarcerate
        - take revenge on, be revenged on, exact/wreak revenge on, get one's revenge on, avenge oneself on, take vengeance on, get even with, settle a/the score with, pay back, pay out, retaliate on/against, get back at, take reprisals against, exact retribution on, give someone their just deserts, give someone a dose/taste of their own medicine, give/return like for like, give tit for tat, take an eye for an eye (and a tooth for a tooth), give someone their comeuppance, get one's own back on
        - annoy, irritate, exasperate, anger, irk, vex, inflame, put out, nettle, needle, provoke, incense, infuriate, madden, rub up the wrong way, try someone's patience, make someone's blood boil, ruffle someone's feathers, make someone's hackles rise, get someone's hackles up, rattle someone's cage, aggravate, peeve, miff, rile, get to, hack off, get someone's back up, get on someone's nerves, get under someone's skin, get someone's goat, get someone's dander up, get in someone's hair, be a thorn in someone's flesh, drive mad, drive crazy, drive nuts, make someone see red, wind up, nark, get across, get someone's wick, give someone the hump, get up someone's nose, tee off, tick off, eat, burn up
        - flummox, discombobulate, faze, stump, beat, fox, make someone scratch their head, floor, fog
        - baffle, nonplus, perplex, puzzle, bewilder, mystify, bemuse, confuse, confound, disconcert, throw, set someone thinking
        - wilder, gravel, maze, cause to be at a stand, pose
        - hear, recognize, discern, distinguish, make out, pick out, perceive, follow, keep up with, take in
        - understand, comprehend, grasp, see, take in, fathom, follow, puzzle out, work out, perceive, apprehend, get to the bottom of, unravel, decipher, get the drift of, catch onto, latch onto, make head or tail of, figure out, get the picture, get the message, twig, suss out, suss

:param		request:   The request

:type		request:   Request

:param		response:  The response

:type		response:  Response

:param		args:	   The arguments

:type		args:	   list

:param		kwargs:	   The keywords arguments

:type		kwargs:	   dictionary

"""

return Response(request, body='Hello World!')

def post(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:

"""


noun
    a long, sturdy piece of timber or metal set upright in the ground and used to support something or as a marker.
        - "follow the blue posts until the track meets a forestry road"
    Synonyms: palisade

    a piece of writing, image, or other item of content published online, typically on a blog or on social media.
        - "in a recent post, he cautioned investors to be wary of these predictions"

    one of a series of couriers who carried mail on horseback between fixed stages.

    a position of paid employment; a job.
        - "he resigned from the post of Foreign Minister"

    a place where someone is on duty or where a particular activity is carried out.
        - "a worker asleep at his post"

    the status or rank of full-grade captain in the Royal Navy.
        - "Captain Miller was made post in 1796"

    work done on a film or recording after filming or recording has taken place.
        - "the rest of the effects were added in post"

verb
    display (a notice) in a public place.
        - "a curt notice had been posted on the door"
    Synonyms: affix, attach, fasten, hang, display, pin (up), put up, stick (up), tack (up), nail (up)

    publish (a piece of writing, image, or other item of content) online, typically on a blog or on social media.
        - "she posted a photo of herself with the singer on Twitter"

    announce or publish (something, especially a financial result).
        - "the company posted a $460,000 loss"
    Synonyms: announce, report, make known, advertise, publish, publicize, circulate, broadcast

    (of a player or team) achieve or record (a particular score or result).
        - "he posted a victory in Japan to lead the series"

    (in bookkeeping) enter (an item) in a ledger.
        - "post the transaction in the second column"
    Synonyms: record, write in, enter, fill in, register, note, list

    travel with relays of horses.
        - "we posted in an open carriage"

    send (someone) to a particular place to take up an appointment.
        - "he was posted to Washington as military attaché"

adverb
    with haste.
        - "come now, come post"

preposition
    subsequent to; after.
        - "American poetry post the 1950s hasn't had the same impact"

prefix
    after in time or order.
        - "postdate"

    behind in position.

Synonyms
    noun
        - puncheon, shore
        - pole, stake, upright, shaft, prop, support, picket, strut, pillar, pale, paling, column, piling, standard, stanchion, pylon, stave, rod, newel, baluster, jamb, bollard, mast, fence post, gatepost, finger post, king post, milepost
        - palisade

    verb
        - affix, attach, fasten, hang, display, pin (up), put up, stick (up), tack (up), nail (up)
        - announce, report, make known, advertise, publish, publicize, circulate, broadcast
        - record, write in, enter, fill in, register, note, list

:param		request:   The request

:type		request:   Request

:param		response:  The response

:type		response:  Response

:param		args:	   The arguments

:type		args:	   list

:param		kwargs:	   The keywords arguments

:type		kwargs:	   dictionary

"""

return Response(request, body='Message has accepted!')

```

You can combine these two methods. There are the following recommendations for their use:

1. If the method only returns already prepared data, then you should not return Response, return data.

2. If the method works with the response passed to it, then return the data or the response itself passed in the arguments.

3. In other cases, you can create a Response and return it, not data.

4. In the get and post methods, you should use only one method, you should not mix them. But if you cannot do without it, then this recommendation can be violated.

These recommendations may be violated at the request of the developer.

You can also throw WebError exceptions instead of returning a result: URLNotFound and MethodNotAllow. In this case, the application will not stop working, but will display an error on the web page side. If another exception occurs, the application will stop working.

There is also a base list in pyechonext.urls to pass as arguments to EchoNext:

```python

url_patterns = [URL(url="/", view=IndexView)]

```

The IndexView here is the built-in View that you could see above.

## application_type

application_type - application type. The argument takes an ApplicationType enum class:

```python

class ApplicationType(Enum):

"""

This enum class describes an application type.

"""

JSON = "application/json"

HTML = "text/html"

PLAINTEXT = "text/plain"

```

Currently supported: ApplicationType.JSON, ApplicationType.HTML, ApplicationType.PLAINTEXT.

Defaults to ApplicationType.JSON.

---

[Contents](./index.md)
