from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
from loguru import logger


class ChangeObserver(ABC):
	"""
	Interface to be notified of a change changes.
	"""

	@abstractmethod
	def on_change(self, audit_entry: "AuditEntry"):
		"""
		Called on change.

		:param		audit_entry:		  The audit entry
		:type		audit_entry:		  AuditEntry

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()


class BasicChangeObserver(ChangeObserver):
	"""
	Interface to be notified of a basic change changes.
	"""

	def on_change(self, audit_entry: "AuditEntry"):
		"""
		Called on change.

		:param		audit_entry:  The audit entry
		:type		audit_entry:  AuditEntry
		"""
		logger.debug(
			f"{audit_entry.timestamp} [{audit_entry.model_name} {audit_entry.table_name} {audit_entry.object_id}] {audit_entry.field_name}: {audit_entry.old_value} -> {audit_entry.new_value}"
		)


@dataclass
class AuditEntry:
	"""
	This dataclass describes an audit entry.
	"""

	model_name: str
	table_name: str
	object_id: str
	field_name: str
	old_value: Optional[str]
	new_value: Optional[str]
	timestamp: datetime


class AuditSubject(ABC):
	"""
	This class describes an audit subject.
	"""

	@abstractmethod
	def attach(self, observer: ChangeObserver):
		"""
		Attach observer

		:param		observer:			  The observer
		:type		observer:			  ChangeObserver

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()

	@abstractmethod
	def detach(self, observer: ChangeObserver):
		"""
		Detach observer

		:param		observer:			  The observer
		:type		observer:			  ChangeObserver

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()

	@abstractmethod
	def notify_observers(self, audit_entry: AuditEntry):
		"""
		Notifies observers.

		:param		audit_entry:		  The audit entry
		:type		audit_entry:		  AuditEntry

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()


class AuditStorage(ABC):
	"""
	This class describes an audit storage.
	"""

	@abstractmethod
	def save_audit_entry(self, audit_entry: AuditEntry):
		"""
		Saves an audit entry.

		:param		audit_entry:		  The audit entry
		:type		audit_entry:		  AuditEntry

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()

	@abstractmethod
	def get_audit_history(
		self, model_name: str, table_name: str, object_id: str
	) -> List[AuditEntry]:
		"""
		Gets the audit history.

		:param		model_name:			  The model name
		:type		model_name:			  str
		:param		table_name:			  The table name
		:type		table_name:			  str
		:param		object_id:			  The object identifier
		:type		object_id:			  str

		:returns:	The audit history.
		:rtype:		List[AuditEntry]

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()

	@abstractmethod
	def revert_changes(
		self,
		model_name: str,
		table_name: str,
		object_id: str,
		field_name: str,
		timestamp: datetime,
	) -> Tuple[Optional[str], Optional[str]]:
		"""
		Revert changes

		:param		model_name:			  The model name
		:type		model_name:			  str
		:param		table_name:			  The table name
		:type		table_name:			  str
		:param		object_id:			  The object identifier
		:type		object_id:			  str
		:param		field_name:			  The field name
		:type		field_name:			  str
		:param		timestamp:			  The timestamp
		:type		timestamp:			  datetime

		:returns:	reverted changes
		:rtype:		Tuple[Optional[str], Optional[str]]

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()


class InMemoryAuditStorage(AuditStorage):
	"""
	This class describes in memory audit storage.
	"""

	def __init__(self):
		"""
		Constructs a new instance.
		"""
		self.audit_entries: List[AuditEntry] = []

	def save_audit_entry(self, audit_entry: AuditEntry):
		"""
		Saves an audit entry.

		:param		audit_entry:  The audit entry
		:type		audit_entry:  AuditEntry
		"""
		self.audit_entries.append(audit_entry)

	def get_audit_history(
		self, model_name: str, table_name: str, object_id: str
	) -> List[AuditEntry]:
		"""
		Gets the audit history.

		:param		model_name:	 The model name
		:type		model_name:	 str
		:param		table_name:	 The table name
		:type		table_name:	 str
		:param		object_id:	 The object identifier
		:type		object_id:	 str

		:returns:	The audit history.
		:rtype:		List[AuditEntry]
		"""
		return [
			entry
			for entry in self.audit_entries
			if entry.model_name == model_name
			and entry.object_id == object_id
			and entry.table_name == table_name
		]

	def revert_changes(
		self,
		model_name: str,
		table_name: str,
		object_id: str,
		field_name: str,
		timestamp: datetime,
	) -> Tuple[Optional[str], Optional[str]]:
		"""
		Revert (rollback) changes

		:param		model_name:	 The model name
		:type		model_name:	 str
		:param		table_name:	 The table name
		:type		table_name:	 str
		:param		object_id:	 The object identifier
		:type		object_id:	 str
		:param		field_name:	 The field name
		:type		field_name:	 str
		:param		timestamp:	 The timestamp
		:type		timestamp:	 datetime

		:returns:	reverted changes
		:rtype:		Tuple[Optional[str], Optional[str]]
		"""
		relevant_entries = [
			entry
			for entry in self.audit_entries
			if entry.model_name == model_name
			and entry.table_name == table_name
			and entry.object_id == object_id
			and entry.field_name == field_name
			and entry.timestamp <= timestamp
		]

		if relevant_entries:
			latest_entry = max(relevant_entries, key=lambda e: e.timestamp)
			return latest_entry.old_value, latest_entry.new_value

		return None, None


class AuditManager(AuditSubject):
	"""
	This class describes an audit manager.
	"""

	def __init__(self, audit_storage: AuditStorage):
		"""
		Constructs a new instance.

		:param		audit_storage:	The audit storage
		:type		audit_storage:	AuditStorage
		"""
		self.audit_storage = audit_storage
		self.observers: List[ChangeObserver] = []

	def attach(self, observer: ChangeObserver):
		"""
		Attach observer

		:param		observer:  The observer
		:type		observer:  ChangeObserver
		"""
		self.observers.append(observer)

	def detach(self, observer: ChangeObserver):
		"""
		Detach observer

		:param		observer:  The observer
		:type		observer:  ChangeObserver
		"""
		self.observers.remove(observer)

	def notify_observers(self, audit_entry: AuditEntry):
		"""
		Notifies observers.

		:param		audit_entry:  The audit entry
		:type		audit_entry:  AuditEntry
		"""
		for observer in self.observers:
			observer.on_change(audit_entry)

	def track_changes(
		self,
		model_name: str,
		table_name: str,
		object_id: str,
		field_name: str,
		old_value: Optional[str],
		new_value: Optional[str],
	):
		"""
		Track changes

		:param		model_name:	 The model name
		:type		model_name:	 str
		:param		table_name:	 The table name
		:type		table_name:	 str
		:param		object_id:	 The object identifier
		:type		object_id:	 str
		:param		field_name:	 The field name
		:type		field_name:	 str
		:param		old_value:	 The old value
		:type		old_value:	 Optional[str]
		:param		new_value:	 The new value
		:type		new_value:	 Optional[str]
		"""
		audit_entry = AuditEntry(
			model_name=model_name,
			table_name=table_name,
			object_id=object_id,
			field_name=field_name,
			old_value=old_value,
			new_value=new_value,
			timestamp=datetime.now(),
		)
		self.audit_storage.save_audit_entry(audit_entry)
		self.notify_observers(audit_entry)

	def get_audit_history(
		self, model_name: str, table_name: str, object_id: str
	) -> List[AuditEntry]:
		"""
		Gets the audit history.

		:param		model_name:	 The model name
		:type		model_name:	 str
		:param		table_name:	 The table name
		:type		table_name:	 str
		:param		object_id:	 The object identifier
		:type		object_id:	 str

		:returns:	The audit history.
		:rtype:		List[AuditEntry]
		"""
		return self.audit_storage.get_audit_history(model_name, table_name, object_id)

	def revert_changes(
		self,
		model_name: str,
		table_name: str,
		object_id: str,
		field_name: str,
		timestamp: datetime,
	) -> Tuple[Optional[str], Optional[str]]:
		"""
		Revert changes

		:param		model_name:	 The model name
		:type		model_name:	 str
		:param		table_name:	 The table name
		:type		table_name:	 str
		:param		object_id:	 The object identifier
		:type		object_id:	 str
		:param		field_name:	 The field name
		:type		field_name:	 str
		:param		timestamp:	 The timestamp
		:type		timestamp:	 datetime

		:returns:	reverted changes
		:rtype:		Tuple[Optional[str], Optional[str]]
		"""
		old_value, new_value = self.audit_storage.revert_changes(
			model_name, table_name, object_id, field_name, timestamp
		)

		self.track_changes(
			model_name,
			table_name,
			object_id,
			field_name,
			new_value,
			f"<REVERTED {old_value}>",
		)

		return (old_value, new_value)
