from typing import Dict, Any, Set, Optional, Iterator, Generic, TypeVar, Iterable

from countertype.counter_type_registration import CounterTypeRegistration

T = TypeVar("T")
EMPTY_SET: Set[Any] = set()


class CounterType(Generic[T]):
    def __init__(self) -> None:
        # for each tag we create a reverse index
        self._indexes: Dict[str, Dict[Any, Set[CounterTypeRegistration[T]]]] = dict()

    def put(self, item: T, **tags) -> None:
        """
        Put an item into the collection, indexed by tags.
        :param tags:
        :param item:
        :return:
        """
        if not tags or "id" not in tags:
            raise Exception(
                "You need to pass in some tags, and the tags must contain "
                "at least the `id` key."
            )

        registration = CounterTypeRegistration(
            item=item,
            tags=tags,
        )

        for tag_name, tag_value in tags.items():
            try:
                reverse_index = self._indexes[tag_name]
            except KeyError:
                reverse_index = dict()
                self._indexes[tag_name] = reverse_index

            try:
                set_items = reverse_index[tag_value]
            except KeyError:
                set_items = set()
                reverse_index[tag_value] = set_items

            set_items.add(registration)

    def find(self, **kw) -> Optional[T]:
        """
        Finds the first item matching the tags.
        :param kw:
        :return:
        """
        r = self.find_all(**kw)

        if not r:
            return None

        for f in r:
            return f

        return None

    def find_all(self, **kw) -> Set[T]:
        """
        Find all the items matching the tags.
        :param kw:
        :return:
        """
        _it = kw.items().__iter__()

        tag_pair = _it.__next__()
        tag_name = tag_pair[0]
        tag_value = tag_pair[1]

        if tag_name not in self._indexes or tag_value not in self._indexes[tag_name]:
            return EMPTY_SET

        try:
            result_set = set(self._indexes[tag_name][tag_value])
        except KeyError:
            return EMPTY_SET

        try:
            while result_set:
                tag_pair = _it.__next__()
                tag_name = tag_pair[0]
                tag_value = tag_pair[1]

                try:
                    result_set.intersection_update(self._indexes[tag_name][tag_value])
                except KeyError:
                    return EMPTY_SET
        except StopIteration:
            pass

        return set(map(lambda it: it.item, result_set))

    def remove(self, *, id: str) -> Optional[T]:
        """
        Remove an item from the collections if it exists. Returns
        the item if it exists.
        :param id:
        :return:
        """
        try:
            registration_set = self._indexes["id"][id]
        except KeyError:
            return None

        registration = registration_set.__iter__().__next__()

        for tag_name, tag_value in registration.tags.items():
            self._remove_tag_value(registration, tag_name, tag_value)

        return registration.item

    def update(self, *, id: str, **kw):
        """
        Update the tags for a given item.
        :param id:
        :param kw:
        :return:
        """
        registration_set = self._indexes["id"][id]
        registration = registration_set.__iter__().__next__()

        for tag_name, tag_value in kw.items():
            if tag_name in registration.tags:
                self._remove_tag_value(
                    registration, tag_name, registration.tags[tag_name]
                )

            reverse_index = self._indexes[tag_name]
            try:
                set_items = reverse_index[tag_value]
            except KeyError:
                set_items = set()
                reverse_index[tag_value] = set_items

            set_items.add(registration)
            registration.tags[tag_name] = tag_value

    def _remove_tag_value(
        self, registration: CounterTypeRegistration[T], tag_name: str, tag_value: Any
    ) -> None:
        value_set = self._indexes[tag_name][tag_value]

        value_set.remove(registration)

        if not value_set:
            self._indexes[tag_name].pop(tag_value)

        if not self._indexes[tag_name]:
            self._indexes.pop(tag_name)
