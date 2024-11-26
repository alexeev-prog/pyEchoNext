# pyEchoNext / Разрешения и права

---

в pyEchoNext вы можете создать дополнительный слой абстракции, в виде политик, разрешений, ролей. Например, так можно создавать роли пользователей, администраторов, вводить ограничения и многое другое.

За это отвечает модуль `pyechonext.permissions`. Он имеет следующие классы:

 + Permission - разрешение,
 + Role - роль,
 + Resource - ресурс,
 + AccessControlRule - правило контроля доступа,
 + Policy - политика,
 + AttributeBasedPolicy - политика ограничения по атрибутам,
 + AgeRestrictionsABP - политика ограничения по атрибуту возраста,
 + User - пользователь,
 + DefaultPermissionChecker - класс проверки прав,
 + UserController - контроллер пользователей

Пример использования:

```python
from pyechonext.permissions import (
	Permission,
	Role,
	Resource,
	AccessControlRule,
	Policy,
	AgeRestrictionsABP,
	User,
	DefaultPermissionChecker,
	UserController,
)

view_users_perm = Permission("view_users")
edit_users_perm = Permission("edit_users")

admin_role = Role("admin")
admin_role.add_permission(view_users_perm)
admin_role.add_permission(edit_users_perm)

user_role = Role("user")
user_role.add_permission(view_users_perm)

user_resource = Resource("UserResource")

policy = Policy()
policy.add_rule(AccessControlRule(admin_role, view_users_perm, user_resource, True))
policy.add_rule(AccessControlRule(admin_role, edit_users_perm, user_resource, True))
policy.add_rule(AccessControlRule(user_role, view_users_perm, user_resource, True))
policy.add_rule(AccessControlRule(user_role, edit_users_perm, user_resource, False))

age_policy = AgeRestrictionsABP(conditions={"age": 18}, rules=policy.rules)
age_policy.add_rule(AccessControlRule(user_role, view_users_perm, user_resource, True))

admin_user = User("admin", attributes={"age": 30})
admin_user.add_role(admin_role)

young_user = User("john_doe", attributes={"age": 17})
young_user.add_role(user_role)

permission_checker = DefaultPermissionChecker(policy)
user_controller = UserController(permission_checker)


def test_controller():
	"""Test Controller"""
	assert user_controller.view_users(admin_user, user_resource) == (
		"200 OK",
		"User edit form",
	)
	assert user_controller.edit_users(admin_user, user_resource) == (
		"200 OK",
		"User edit form",
	)
	assert user_controller.edit_users(young_user, user_resource) == (
		"403 Forbidden",
		"You do not have permission to edit users.",
	)


def test_age_policy():
	"""Test Age Policy"""
	assert age_policy.evaluate(young_user, user_resource, view_users_perm) == False
	assert age_policy.evaluate(admin_user, user_resource, view_users_perm) == True


test_controller()
test_age_policy()
```

---

[Содержание](./index.md)



