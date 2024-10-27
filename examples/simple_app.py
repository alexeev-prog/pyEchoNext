from pyechonext.app import ApplicationType, EchoNext
from sqlsymphony_orm.datatypes.fields import IntegerField, RealField, TextField
from sqlsymphony_orm.models.session_models import SessionModel
from sqlsymphony_orm.models.session_models import SQLiteSession
from sqlsymphony_orm.queries import QueryBuilder


echonext = EchoNext(__name__, application_type=ApplicationType.HTML)
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
	user = User(name='John', cash=100.0)
	session.add(user)
	session.commit()
	response.body = "Hello from the HOME page"


@echonext.route_page("/users")
def about(request, response):
	users = session.get_all_by_model(User)
	
	response.body = f"Users: {[f'{user.name}: {user.cash}$' for user in users]}"
