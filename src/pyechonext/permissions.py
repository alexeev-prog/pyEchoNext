from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set, Tuple, Type


class AbstractPermission(ABC):
    """
    This class describes an abstract permission.
    """

    @abstractmethod
    def __str__(self):
        """Returns a string representation of the object.

            Raises:
        NotImplementedError: abstract method
        """
        raise NotImplementedError()


class Permission(AbstractPermission):
    """
    This class describes a permission.
    """

    def __init__(self, name: str):
        """Initialize a permission

            Args:
        name (str): permission name
        """
        self.name: str = name

    def __str__(self) -> str:
        """Returns a string representation of the object.

            Returns:
        str: permission name
        """
        return self.name


class AbstractRole(ABC):
    """
    This class describes an abstract role.
    """

    @abstractmethod
    def has_permission(self, permission: Type[AbstractPermission]) -> bool:
        """Determines if permission

            Args:
        permission (AbstractPermission): permission object

            Raises:
        NotImplementedError: abstract method

            Returns:
        bool: true is has, false otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    def get_permissions(self) -> Set[AbstractPermission]:
        """Get list of permissions

            Raises:
        NotImplementedError: abstract method

            Returns:
        Set[AbstractPermission]: set with abstract permissions
        """
        raise NotImplementedError()

    @abstractmethod
    def get_name(self) -> str:
        """Get the role name

            Raises:
        NotImplementedError: abstract method

            Returns:
        str: role name
        """
        raise NotImplementedError()


class Role(AbstractRole):
    """
    This class describes a role.
    """

    def __init__(self, name: str):
        """Constructs a new instance

            Args:
        name (str): role name
        """
        self.name = name
        self.permissions: Set[AbstractPermission] = set()

    def add_permission(self, permission: AbstractPermission):
        """Add a permission

            Args:
        permission (AbstractPermission): permission object
        """
        self.permissions.add(permission)

    def remove_permission(self, permission: AbstractPermission):
        """Remove a permission

            Args:
        permission (AbstractPermission): permission object
        """
        self.permissions.discard(permission)

    def has_permission(self, permission: AbstractPermission) -> bool:
        """Determines if permission

            Args:
        permission (AbstractPermission): permission object

        bool: true is has, false otherwise
        """
        return permission in self.permissions

    def get_permissions(self) -> Set[AbstractPermission]:
        """Get list of permissions

            Returns:
        Set[AbstractPermission]: set with abstract permissions
        """
        return self.permissions

    def get_name(self) -> str:
        """Get the role name

            Returns:
        str: role name
        """
        return self.name


class User:
    """
    This class describes an user.
    """

    def __init__(self, username: str, attributes: Dict[str, Any] = {}):
        """Constructs a new instance

            Args:
        username (str): name of user
        attributes (Dict[str, Any], optional): attributes for user. Defaults to {}.
        """
        self.username: str = username
        self.roles: Set[AbstractRole] = set()
        self.attributes: Dict[str, Any] = attributes

    def add_role(self, role: AbstractRole):
        """Adds a role

            Args:
        role (AbstractRole): role object
        """
        self.roles.add(role)

    def remove_role(self, role: AbstractRole):
        """Remove a role

            Args:
        role (Type[AbstractRole]): role object
        """
        self.roles.discard(role)

    def has_permission(self, permission: AbstractPermission) -> bool:
        """Determines if permission

            Args:
        permission (Type[AbstractPermission]): permission object

            Returns:
        bool: true is has, false otherwise
        """
        perms = [str(perm) for p in self.roles for perm in p.permissions]
        return str(permission) in perms

    def get_roles(self) -> Set[AbstractRole]:
        """Get roles

            Returns:
        Set[AbstractRole]: roles set
        """
        return self.roles

    def get_username(self) -> str:
        """Get username

            Returns:
        str: username
        """
        return self.username


class Resource:
    """
    This class describes a resource.
    """

    def __init__(self, name: str):
        """Constructs a new resource

            Args:
        name (str): resource name
        """
        self.name = name

    def __str__(self) -> str:
        """Returns a string representation of the object.

            Returns:
        str: resource name
        """
        return self.name


class AccessControlRule:
    """
    This class describes an access control rule.
    """

    def __init__(
        self,
        role: Type[AbstractRole],
        permission: Type[AbstractPermission],
        resource: Type[Resource],
        allowed: bool,
    ):
        """Constructs a new instance

            Args:
        role (Type[AbstractRole]): role object
        permission (Type[AbstractPermission]): permission object
        resource (Type[Resource]): resource object
        allowed (bool): allowed status
        """
        self.role: Type[AbstractRole] = role
        self.permission: Type[AbstractPermission] = permission
        self.resource: Type[Resource] = resource
        self.allowed: bool = allowed

    def applies_to(
        self, user: User, resource: Type[Resource], permission: Type[AbstractPermission]
    ) -> bool:
        """Applies to user

            Args:
        user (User): user
        resource (Type[Resource]): resource
        permission (Type[AbstractPermission]): permissions

            Returns:
        bool: true if is applies, false otherwise
        """
        return (
            self.role in user.get_roles()
            and self.resource == resource
            and str(self.permission) == str(permission)
        )

    def __str__(self):
        """Returns a string representation of the object.

            Returns:
        str: rule name
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
        """Add a new rule

            Args:
        rule (AccessControlRule): new rule
        """
        self.rules.append(rule)

    def evaluate(
        self, user: User, resource: Type[Resource], permission: Type[AbstractPermission]
    ) -> bool:
        """Evaluate policty access

            Args:
        user (User): user object
        resource (Resource): resource
        permission (AbstractPermission): permission

            Returns:
        bool: true is allowed, false otherwise
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
        """Constructs a new instance

            Args:
        conditions (Dict[str, Any]): conditions dictionary
        """
        super().__init__()
        self.conditions = conditions

    def evaluate(
        self, user: User, resource: Type[Resource], permission: Type[AbstractPermission]
    ) -> bool:
        """Evaluate policy access

            Args:
        user (User): user model
        resource (Resource): resource model
        permission (AbstractPermission): permission model

            Returns:
        bool: evaluation status
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
        """Initialize a Age Policy

            Args:
        conditions (Dict[str, Any]): conditions
        rules (List[AccessControlRule]): rules list
        """
        super().__init__()
        self.conditions = conditions
        self.rules += rules

    def evaluate(
        self, user: User, resource: Type[Resource], permission: Type[AbstractPermission]
    ) -> bool:
        """Evaluate policy access

            Args:
        user (User): user object
        resource (Resource): resource object
        permission (AbstractPermission): permission object

            Returns:
        bool: evaluation status
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
        self, user: User, resource: Type[Resource], permission: Type[AbstractPermission]
    ) -> bool:
        """Check permissions for user

            Args:
        user (User): user object
        resource (Resource): resource object
        permission (AbstractPermission): permission object

            Raises:
        NotImplementedError: abstract method

            Returns:
        bool: true is valid, false otherwise
        """
        raise NotImplementedError()


class DefaultPermissionChecker(PermissionChecker):
    """
    This class describes a default permission checker.
    """

    def __init__(self, policy: Policy):
        """Initialize a checker

            Args:
        policy (Policy): policy for checkr
        """
        self.policy: Policy = policy

    def check(
        self, user: User, resource: Type[Resource], permission: Type[AbstractPermission]
    ) -> bool:
        """Check user permissions

            Args:
        user (User): user object
        resource (Resource): resource object
        permission (AbstractPermission): permissions object

            Returns:
        bool: true is valid, false otherwise
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
        """Constructs a new instance

            Args:
        permission_checker (PermissionChecker): permission checker class
        """
        pass

    @abstractmethod
    def check(
        self, current_user: User, resource: Type[Resource], permission: Permission
    ) -> bool:
        """Check permissions for user

            Args:
        current_user (User): user object
        resource (Resource): resource object
        permission (Permission): permission object

            Raises:
        NotImplementedError: abstractmethod

            Returns:
        bool: true is valid, otherwise false
        """
        raise NotImplementedError()


class UserController(AbstractController):
    """
    Controls the data flow into an user object and updates the view whenever data changes.
    """

    def __init__(self, permission_checker: PermissionChecker):
        """Constructs a new instance

            Args:
        permission_checker (PermissionChecker): permission checker class
        """
        self.permission_checker = permission_checker

    def check(
        self, current_user: User, resource: Type[Resource], permission: Permission
    ) -> bool:
        """Check permissions for user

            Args:
        current_user (User): current user object
        resource (Resource): resource object
        permission (Permission): user permission

            Returns:
        bool: True is valid, false otherwise
        """
        return self.permission_checker.check(current_user, resource, permission)

    def view_users(self, current_user: User, resource: Type[Resource]) -> Tuple[str]:
        """View users by current user and resource

            Args:
        current_user (User): current user object
        resource (Resource): resource object

            Returns:
        Tuple[str]: data
        """
        if not self.permission_checker.check(
            current_user, resource, Permission("view_users")
        ):
            return ("403 Forbidden", "You do not have permission to view users.")

        return ("200 OK", "User edit form")

    def edit_users(self, current_user: User, resource: Type[Resource]) -> Tuple[str]:
        """Edit users with current user and resource

            Args:
        current_user (User): user object
        resource (Resource): resource object

            Returns:
        Tuple[str]: data
        """
        if not self.permission_checker.check(
            current_user, resource, Permission("edit_users")
        ):
            return ("403 Forbidden", "You do not have permission to edit users.")

        return ("200 OK", "User edit form")
