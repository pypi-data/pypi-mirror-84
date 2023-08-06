import unittest

from countertype import CounterType


class CounterTypeTest(unittest.TestCase):
    @unittest.expectedFailure
    def test_tags_must_contain_id(self) -> None:
        ct: CounterType[str] = CounterType()

        ct.put(
            "ev1",
            _state="RUNNING",
        )

    def test_simple_find(self):
        ct = create_counter_type()

        # Finding by a specific tag should work
        self.assertEqual(
            {"ev1"},
            set(ct.find_all(state="RUNNING")),
        )
        self.assertEqual(
            {"ev2"},
            set(ct.find_all(state="STOPPED")),
        )

        # Finding with None values should work as well
        self.assertEqual(
            {"ev1"},
            set(ct.find_all(parent_id="123")),
        )
        self.assertEqual(
            {"ev2"},
            set(ct.find_all(parent_id=None)),
        )

        # Finding multiple matches should also get us results
        self.assertEqual(
            {"ev1", "ev2"},
            set(ct.find_all(deduplication_id="a")),
        )

    def test_missing_keys_should_not_fail(self):
        ct = create_counter_type()

        self.assertFalse(ct.find_all(not_existing=3))

        self.assertFalse(ct.find_all(deduplication_id=None))

    def test_removing_keys_should_clear_collection(self):
        ct = create_counter_type()
        ct.remove(id="ev1")
        ct.remove(id="ev2")

        self.assertEqual(0, len(ct._indexes))

    def test_updating_tags_should_allow_finding(self):
        ct = create_counter_type()
        ct.update(id="ev1", state="PROCESSING")

        self.assertFalse(
            ct.find_all(state="RUNNING"),
        )
        self.assertEqual(
            {"ev1"},
            set(ct.find_all(state="PROCESSING")),
        )

        ct.remove(id="ev1")
        ct.remove(id="ev2")

        self.assertEqual(0, len(ct._indexes))


def create_counter_type():
    ct = CounterType()

    ct.put(
        "ev1",
        id="ev1",
        state="RUNNING",
        parent_id="123",
        deduplication_id="a",
    )

    ct.put(
        "ev2",
        id="ev2",
        state="STOPPED",
        parent_id=None,
        deduplication_id="a",
    )

    return ct
