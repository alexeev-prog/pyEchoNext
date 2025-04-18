import os

from sqlsymphony_orm.datatypes.fields import IntegerField, RealField, TextField
from sqlsymphony_orm.models.session_models import SessionModel, SQLiteSession

from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from pyechonext.middleware import middlewares

settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(
	__name__, settings, middlewares, application_type=ApplicationType.HTML
)
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
