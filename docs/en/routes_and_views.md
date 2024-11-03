# pyEchoNext / Creating routes (routes&views)

---

Routes are the basis of a web application.

pyEchoNext has two methods for creating web page routes:

+ Django-like: creating a descendant of the View class, placing it in a URL dataclass and passing it as a urls argument to the EchoNext main application class object

+ Flask-like: creating functions with the EchoNext.route_page decorator.

Flask-like example:

```python

import os

from pyechonext.app import ApplicationType, EchoNext

from pyechonext.config import Settings

from sqlsymphony_orm.datatypes.fields import IntegerField, RealField, TextField

from sqlsymphony_orm.models.session_models import SessionModel

from sqlsymphony_orm.models.session_models import SQLiteSession

from pyechonext.middleware import middlewares

settings = Settings(

BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"

)

echonext = EchoNext(__name__, settings, middlewares, application_type=ApplicationType.HTML)

session = SQLiteSession("echonext.db")

class User(SessionModel):

__tablename__ = "Users"

id = IntegerField(primary_key=True)

name = TextField(null=False)

cash = RealField(null=False, default=0.0)

def __repr__(self):

return f"<User {self.pk}>"

@echonext.route_page("/")

def home(request, response):

user = User(name="John", cash=100.0)

session.add(user)

session.commit()

return "Hello from the HOME page"

@echonext.route_page("/users")

def about(request, response):

users = session.get_all_by_model(User)

return f"Users: {[f'{user.name}: {user.cash}$' for user in users]}"

```

Example django-like and flask-like:

```python

import os

from pyechonext.utils.exceptions import MethodNotAllow

from pyechonext.app import ApplicationType, EchoNext

from pyechonext.views import View

from pyechonext.urls import URL, IndexView

from pyechonext.config import Settings

from pyechonext.template_engine.jinja import render_template

from pyechonext.middleware import middlewares

class UsersView(View):

def get(self, request, response, **kwargs):

return render_template(

request, "index.html", user_name="User", session_id=request.session_id, friends=["Bob", "Anna", "John"]

)

def post(self, request, response, **kwargs):

raise MethodNotAllow(f'Request {request.path}: method not allow')

url_patterns = [URL(url="/", view=IndexView), URL(url="/users", view=UsersView)]

settings = Settings(

BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"

)

echonext = EchoNext(

__name__, settings, middlewares, urls=url_patterns, application_type=ApplicationType.HTML

)

@echonext.route_page("/book")

class BooksResource(View):

def get(self, request, response, **kwargs):

return f"GET Params: {request.GET}"

def post(self, request, response, **kwargs):

return f"POST Params: {request.POST}"

```

Both methods can be mixed, but we recommend using only one per web application.


noun
    the ability to see something or to be seen from a particular place.
        - "the end of the tunnel came into view"
    Synonyms: sight, perspective, field of vision, range of vision, vision, visibility, eyeshot

    a sight or prospect, typically of attractive natural scenery, that can be taken in by the eye from a particular place.
        - "a fine view of the castle"
    Synonyms: outlook, prospect, panorama, vista, scene, aspect, perspective, spectacle, sight, scenery, landscape, seascape, riverscape, cityscape, townscape, snowscape

    a particular way of considering or regarding something; an attitude or opinion.
        - "strong political views"
    Synonyms: opinion, point of view, viewpoint, belief, judgment, reckoning, way of thinking, thinking, thought, notion, idea, conviction, persuasion, attitude, feeling, sentiment, impression, concept, conception, hypothesis, theory, thesis, estimate, estimation, conclusion, verdict, statement, observation, remark, point, angle, slant, stance, posture, standpoint, approach

verb
    look at or inspect (something).
        - "the public can view the famous hall with its unique staircase"
    Synonyms: get a load of, gawp at, rubberneck at, give something a/the once-over, have a look-see at, have/take a gander at, have a squint at, clap eyes on, have/take a dekko at, have/take a butcher's at, take a shufti at, clock, eyeball

    regard in a particular light or with a particular attitude.
        - "farmers are viewing the rise in rabbit numbers with concern"
    Synonyms: consider, regard, look on, see, perceive, judge, adjudge, estimate, deem, reckon, think of, treat

Synonyms
    noun
        - sight, perspective, field of vision, range of vision, vision, visibility, eyeshot
        - lookout
        - outlook, prospect, panorama, vista, scene, aspect, perspective, spectacle, sight, scenery, landscape, seascape, riverscape, cityscape, townscape, snowscape
        - opinion, point of view, viewpoint, belief, judgment, reckoning, way of thinking, thinking, thought, notion, idea, conviction, persuasion, attitude, feeling, sentiment, impression, concept, conception, hypothesis, theory, thesis, estimate, estimation, conclusion, verdict, statement, observation, remark, point, angle, slant, stance, posture, standpoint, approach

    verb
        - espy, behold, descry
        - look at, gaze at, stare at, peer at, eye, observe, ogle, contemplate, regard, scan, survey, watch, look over, see over, be shown over, examine, inspect, scrutinize, catch sight of, glimpse, lay eyes on, spy, spot, check something out
        - get a load of, gawp at, rubberneck at, give something a/the once-over, have a look-see at, have/take a gander at, have a squint at, clap eyes on, have/take a dekko at, have/take a butcher's at, take a shufti at, clock, eyeball
        - consider, regard, look on, see, perceive, judge, adjudge, estimate, deem, reckon, think of, treat

See also
    view

Views - “views”, a special class for displaying site pages. Inspired by Django style.

```python

class View(ABC):

"""


noun
    an instance of an internet user visiting a particular page on a website.

"""

@abstractmethod

def get(

self, request: Request, response: Response, *args, **kwargs

) -> Union[Response, Any]:

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

:param    request:   The request

:type   request:   Request

:param    response:  The response

:type   response:  Response

:param    args:    The arguments

:type   args:    list

:param    kwargs:    The keywords arguments

:type   kwargs:    dictionary

"""

raise NotImplementedError

@abstractmethod

def post(

self, request: Request, response: Response, *args, **kwargs

) -> Union[Response, Any]:

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

:param    request:   The request

:type   request:   Request

:param    response:  The response

:type   response:  Response

:param    args:    The arguments

:type   args:    list

:param    kwargs:    The keywords arguments

:type   kwargs:    dictionary

"""

raise NotImplementedError

```

To pass them to the EchoNext application, you need to combine Views into a URL:

```python

@dataclass

class URL:

"""

This dataclass describes an url.

"""

url: str

view: Type[View]

url_patterns = [URL(url="/", view=<ВАШ View>)]

```

Example:

```python

class IndexView(View):

def get(

self, request: Request, response: Response, **kwargs

) -> Union[Response, Any]:

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

:param    request:   The request

:type   request:   Request

:param    response:  The response

:type   response:  Response

:param    args:    The arguments

:type   args:    list

:param    kwargs:    The keywords arguments

:type   kwargs:    dictionary

"""

return "Hello World!"

def post(

self, request: Request, response: Response, **kwargs

) -> Union[Response, Any]:

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

:param    request:   The request

:type   request:   Request

:param    response:  The response

:type   response:  Response

:param    args:    The arguments

:type   args:    list

:param    kwargs:    The keywords arguments

:type   kwargs:    dictionary

"""

return "Message has accepted!"

url_patterns = [URL(url="/", view=IndexView)]

```


noun
    a way or course taken in getting from a starting point to a destination.
        - "the most direct route is via Los Angeles"

verb
    send or direct along a specified course.
        - "all lines of communication were routed through Atlanta"
    Synonyms: direct, send, convey, dispatch, forward

Synonyms
    verb
        - direct, send, convey, dispatch, forward

See also
    route

Routes inspired by flask/fastapi:

```python

import os

from pyechonext.app import ApplicationType, EchoNext

from pyechonext.config import Settings

from pyechonext.middleware import middlewares

settings = Settings(

BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"

)

echonext = EchoNext(

__name__, settings, middlewares, application_type=ApplicationType.HTML

)

@echonext.route_page("/")

def home(request, response):

return "Hello from the HOME page"

@echonext.route_page("/book")

class BooksResource(View):

def get(self, request, response, **kwargs):

return f"GET Params: {request.GET}"

def post(self, request, response, **kwargs):

return f"POST Params: {request.POST}"

```

You can also route Views without passing them to parameters, but by creating a class with a page routing decorator.

---

[Contents](./index.md)
