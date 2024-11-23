from abc import ABC, abstractmethod
from typing import Set, List, Dict, Tuple, Any


class AbstractPermission(ABC):
	"""
	This class describes an abstract permission.
	"""

	@abstractmethod
	def __str__(self):
		"""
		Returns a string representation of the object.

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()


class Permission(AbstractPermission):
	"""
	This class describes a permission.
	"""

	def __init__(self, name: str):
		"""
		Constructs a new instance.

		:param		name:  The name
		:type		name:  str
		"""
		self.name: str = name

	def __str__(self) -> str:
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return self.name


class AbstractRole(ABC):
	"""
	This class describes an abstract role.
	"""

	@abstractmethod
	def has_permission(self, permission: AbstractPermission) -> bool:
		"""
		Determines if permission.

		:param		permission:			  The permission
		:type		permission:			  AbstractPermission

		:returns:	True if permission, False otherwise.
		:rtype:		bool

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()

	@abstractmethod
	def get_permissions(self) -> Set[AbstractPermission]:
		"""
		Gets the permissions.

		:returns:	The permissions.
		:rtype:		Set[AbstractPermission]

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()

	@abstractmethod
	def get_name(self) -> str:
		"""
		Gets the name.

		:returns:	The name.
		:rtype:		str

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()


class Role(AbstractRole):
	"""
	This class describes a role.
	"""

	def __init__(self, name: str):
		"""
		Constructs a new instance.

		:param		name:  The name
		:type		name:  str
		"""
		self.name = name
		self.permissions: Set[AbstractPermission] = set()

	def add_permission(self, permission: AbstractPermission):
		"""
		Adds a permission.

		:param		permission:	 The permission
		:type		permission:	 AbstractPermission
		"""
		self.permissions.add(permission)

	def remove_permission(self, permission: AbstractPermission):
		"""
		Removes a permission.

		:param		permission:	 The permission
		:type		permission:	 AbstractPermission
		"""
		self.permissions.discard(permission)

	def has_permission(self, permission: AbstractPermission) -> bool:
		"""
		Determines if permission.

		:param		permission:	 The permission
		:type		permission:	 AbstractPermission

		:returns:	True if permission, False otherwise.
		:rtype:		bool
		"""
		return permission in self.permissions

	def get_permissions(self) -> Set[AbstractPermission]:
		"""
		Gets the permissions.

		:returns:	The permissions.
		:rtype:		Set[AbstractPermission]
		"""
		return self.permissions

	def get_name(self) -> str:
		"""
		Gets the name.

		:returns:	The name.
		:rtype:		str
		"""
		return self.name


class User:
	"""
	This class describes an user.
	"""

	def __init__(self, username: str, attributes: Dict[str, Any] = {}):
		"""
		Constructs a new instance.

		:param		username:	 The username
		:type		username:	 str
		:param		attributes:	 The attributes
		:type		attributes:	 Dict[str, Any]
		"""
		self.username: str = username
		self.roles: Set[AbstractRole] = set()
		self.attributes: Dict[str, Any] = attributes

	def add_role(self, role: AbstractRole):
		"""
		Adds a role.

		:param		role:  The role
		:type		role:  AbstractRole
		"""
		self.roles.add(role)

	def remove_role(self, role: AbstractRole):
		"""
		Removes a role.

		:param		role:  The role
		:type		role:  AbstractRole
		"""
		self.roles.discard(role)

	def has_permission(self, permission: AbstractPermission) -> bool:
		"""
		Determines if permission.

		:param		permission:	 The permission
		:type		permission:	 AbstractPermission

		:returns:	True if permission, False otherwise.
		:rtype:		bool
		"""
		perms = [str(perm) for p in self.roles for perm in p.permissions]
		return str(permission) in perms

	def get_roles(self) -> Set[AbstractRole]:
		"""
		Gets the roles.

		:returns:	The roles.
		:rtype:		Set[AbstractRole]
		"""
		return self.roles

	def get_username(self) -> str:
		"""
		Gets the username.

		:returns:	The username.
		:rtype:		str
		"""
		return self.username


class Resource:
	"""
	This class describes a resource.
	"""

	def __init__(self, name: str):
		"""
		Constructs a new instance.

		:param		name:  The name
		:type		name:  str
		"""
		self.name = name

	def __str__(self) -> str:
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return self.name


class AccessControlRule:
	"""
	This class describes an access control rule.
	"""

	def __init__(
		self,
		role: AbstractRole,
		permission: AbstractPermission,
		resource: Resource,
		allowed: bool,
	):
		"""
		Constructs a new instance.

		:param		role:		 The role
		:type		role:		 AbstractRole
		:param		permission:	 The permission
		:type		permission:	 AbstractPermission
		:param		resource:	 The resource
		:type		resource:	 Resource
		:param		allowed:	 Indicates if allowed
		:type		allowed:	 bool
		"""
		self.role: AbstractRole = role
		self.permission: AbstractPermission = permission
		self.resource: Resource = resource
		self.allowed: bool = allowed

	def applies_to(
		self, user: User, resource: Resource, permission: AbstractPermission
	) -> bool:
		"""
		Applies to access

		:param		user:		 The user
		:type		user:		 User
		:param		resource:	 The resource
		:type		resource:	 Resource
		:param		permission:	 The permission
		:type		permission:	 AbstractPermission

		:returns:	True if applies, False otherwise.
		:rtype:		bool
		"""
		return (
			self.role in user.get_roles()
			and self.resource == resource
			and str(self.permission) == str(permission)
		)

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return f"Rule {self.role} {self.permission} {self.resource} {self.allowed}"


class Policy:
	"""
	This class describes a policy.
	"""

	def __init__(self):
		"""
		Constructs a new instance.
		"""
		self.rules: List[AccessControlRule] = []

	def add_rule(self, rule: AccessControlRule):
		"""
		Adds a rule.

		:param		rule:  The rule
		:type		rule:  AccessControlRule
		"""
		self.rules.append(rule)

	def evaluate(
		self, user: User, resource: Resource, permission: AbstractPermission
	) -> bool:
		"""
		Evaluate policy access

		:param		user:		 The user
		:type		user:		 User
		:param		resource:	 The resource
		:type		resource:	 Resource
		:param		permission:	 The permission
		:type		permission:	 AbstractPermission

		:returns:	True if access, False otherwise.
		:rtype:		bool
		"""
		for rule in self.rules:
			if rule.applies_to(user, resource, permission):
				return rule.allowed

		return False


class AttributeBasedPolicy(Policy):
	"""
	This class describes an attribute based policy.
	"""

	def __init__(self, conditions: Dict[str, Any]):
		"""
		Constructs a new instance.

		:param		conditions:	 The conditions
		:type		conditions:	 Dict[str, Any]
		"""
		super().__init__()
		self.conditions = conditions

	def evaluate(
		self, user: User, resource: Resource, permission: AbstractPermission
	) -> bool:
		"""
		Evaluate policy access

		:param		user:		 The user
		:type		user:		 User
		:param		resource:	 The resource
		:type		resource:	 Resource
		:param		permission:	 The permission
		:type		permission:	 AbstractPermission

		:returns:	True if access, False otherwise.
		:rtype:		bool
		"""
		for condition, value in self.conditions.items():
			if user.attributes.get(condition, None) is None:
				continue

		return super().evaluate(user, resource, permission)


class AgeRestrictionsABP(Policy):
	"""
	This class describes an age restrictions abp.
	"""

	def __init__(self, conditions: Dict[str, Any], rules: List[AccessControlRule]):
		"""
		Constructs a new instance.

		:param		conditions:	 The conditions
		:type		conditions:	 conditions: Dict[str, Any]
		:param		rules:		 The rules
		:type		rules:		 List[AccessControlRule]
		"""
		super().__init__()
		self.conditions = conditions
		self.rules += rules

	def evaluate(
		self, user: User, resource: Resource, permission: AbstractPermission
	) -> bool:
		"""
		Evaluate policy access

		:param		user:		 The user
		:type		user:		 User
		:param		resource:	 The resource
		:type		resource:	 Resource
		:param		permission:	 The permission
		:type		permission:	 AbstractPermission

		:returns:	True if access, False otherwise.
		:rtype:		bool
		"""
		for condition, value in self.conditions.items():
			if user.attributes.get(condition, 0) < value:
				return False

		return super().evaluate(user, resource, permission)


class PermissionChecker(ABC):
	"""
	This class describes a permission checker.
	"""

	@abstractmethod
	def check(
		self, user: User, resource: Resource, permission: AbstractPermission
	) -> bool:
		"""
		Check permission for user

		:param		user:				  The user
		:type		user:				  User
		:param		resource:			  The resource
		:type		resource:			  Resource
		:param		permission:			  The permission
		:type		permission:			  AbstractPermission

		:returns:	True is valid, false otherwise
		:rtype:		bool

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()


class DefaultPermissionChecker(PermissionChecker):
	"""
	This class describes a default permission checker.
	"""

	def __init__(self, policy: Policy):
		"""
		Constructs a new instance.

		:param		policy:	 The policy
		:type		policy:	 Policy
		"""
		self.policy: Policy = policy

	def check(
		self, user: User, resource: Resource, permission: AbstractPermission
	) -> bool:
		"""
		Check permission for user

		:param		user:				  The user
		:type		user:				  User
		:param		resource:			  The resource
		:type		resource:			  Resource
		:param		permission:			  The permission
		:type		permission:			  AbstractPermission

		:returns:	True is valid, false otherwise
		:rtype:		bool
		"""
		if user.has_permission(permission):
			return self.policy.evaluate(user, resource, permission)

		return False


class AbstractController(ABC):
	"""
	This class describes a abstract controller.
	"""

	@abstractmethod
	def __init__(self, permission_checker: PermissionChecker):
		"""
		Constructs a new instance.

		:param		permission_checker:	 The permission checker
		:type		permission_checker:	 PermissionChecker
		"""
		raise NotImplementedError()

	@abstractmethod
	def check(
		self, current_user: User, resource: Resource, permission: Permission
	) -> bool:
		"""
		Check permission for user

		:param		user:				  The user
		:type		user:				  User
		:param		resource:			  The resource
		:type		resource:			  Resource
		:param		permission:			  The permission
		:type		permission:			  AbstractPermission

		:returns:	True is valid, false otherwise
		:rtype:		bool

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()


class UserController(AbstractController):
	"""
	Controls the data flow into an user object and updates the view whenever data changes.
	"""

	def __init__(self, permission_checker: PermissionChecker):
		"""
		Constructs a new instance.

		:param		permission_checker:	 The permission checker
		:type		permission_checker:	 PermissionChecker
		"""
		self.permission_checker = permission_checker

	def check(
		self, current_user: User, resource: Resource, permission: Permission
	) -> bool:
		"""
		Check permission for user

		:param		user:				  The user
		:type		user:				  User
		:param		resource:			  The resource
		:type		resource:			  Resource
		:param		permission:			  The permission
		:type		permission:			  AbstractPermission

		:returns:	True is valid, false otherwise
		:rtype:		bool
		"""
		return self.permission_checker.check(current_user, resource, permission)

	def view_users(self, current_user: User, resource: Resource) -> Tuple[str]:
		"""
		View users

		:param		current_user:  The current user
		:type		current_user:  User
		:param		resource:	   The resource
		:type		resource:	   Resource

		:returns:	response
		:rtype:		Tuple[str]
		"""
		if not self.permission_checker.check(
			current_user, resource, Permission("view_users")
		):
			return ("403 Forbidden", "You do not have permission to view users.")

		return ("200 OK", "User edit form")

	def edit_users(self, current_user: User, resource: Resource) -> Tuple[str]:
		"""
		Edit users

		:param		current_user:  The current user
		:type		current_user:  User
		:param		resource:	   The resource
		:type		resource:	   Resource

		:returns:	response
		:rtype:		Tuple[str]
		"""
		if not self.permission_checker.check(
			current_user, resource, Permission("edit_users")
		):
			return ("403 Forbidden", "You do not have permission to edit users.")

		return ("200 OK", "User edit form")
