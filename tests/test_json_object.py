from unittest.mock import ANY

from faker import Faker

from pydevtools.http import JsonObject


def test_should_not_drop_anything(faker: Faker) -> None:
    key = faker.word()

    updated = JsonObject({key: ANY}).drop()

    assert dict(updated) == {key: ANY}


def test_should_drop_a_key(faker: Faker) -> None:
    key = faker.word()

    updated = JsonObject({key: ANY}).drop(key)

    assert dict(updated) == {}


def test_should_drop_many_keys(faker: Faker) -> None:
    key1 = faker.word()
    key2 = faker.word()

    updated = JsonObject({key1: ANY, key2: ANY}).drop(key1, key2)

    assert dict(updated) == {}


def test_should_not_drop_a_key(faker: Faker) -> None:
    key1 = faker.word()
    key2 = faker.word()

    updated = JsonObject({key1: ANY, key2: ANY}).drop(key2)

    assert dict(updated) == {key1: ANY}


def test_should_not_drop_many_keys(faker: Faker) -> None:
    key1 = faker.word()
    key2 = faker.word()
    key3 = faker.word()

    updated = JsonObject({key1: ANY, key2: ANY, key3: ANY}).drop(key3)

    assert dict(updated) == {key1: ANY, key2: ANY}


def test_should_not_select_anything(faker: Faker) -> None:
    key = faker.word()

    updated = JsonObject({key: ANY}).select()

    assert dict(updated) == {}


def test_should_select_a_key(faker: Faker) -> None:
    key = faker.word()

    updated = JsonObject({key: ANY}).select(key)

    assert dict(updated) == {key: ANY}


def test_should_select_many_keys(faker: Faker) -> None:
    key1 = faker.word()
    key2 = faker.word()

    updated = JsonObject({key1: ANY, key2: ANY}).select(key1, key2)

    assert dict(updated) == {key1: ANY, key2: ANY}


def test_should_not_select_a_key(faker: Faker) -> None:
    key1 = faker.word()
    key2 = faker.word()

    updated = JsonObject({key1: ANY, key2: ANY}).select(key1)

    assert dict(updated) == {key1: ANY}


def test_should_not_select_many_keys(faker: Faker) -> None:
    key1 = faker.word()
    key2 = faker.word()
    key3 = faker.word()

    updated = JsonObject({key1: ANY, key2: ANY, key3: ANY}).select(key1)

    assert dict(updated) == {key1: ANY}


def test_should_add_a_key(faker: Faker) -> None:
    key = faker.word()
    value = faker.word()

    updated: JsonObject[str] = JsonObject({}).with_a(**{key: value})

    assert dict(updated) == {key: value}


def test_should_merge_json_objects_no_overlap(faker: Faker) -> None:
    # Given: Two JsonObjects with no overlapping keys
    obj1 = JsonObject({faker.word(): faker.word(), faker.word(): faker.word()})
    obj2 = JsonObject({faker.word(): faker.word(), faker.word(): faker.word()})

    # When: We merge the two JsonObjects
    result = obj1.merge(obj2)

    # Then: The result should contain all keys from both JsonObjects
    assert len(dict(result)) == 4


def test_should_merge_json_objects_with_overlap(faker: Faker) -> None:
    # Given: Two JsonObjects with one overlapping key
    common_key = faker.word()
    obj1 = JsonObject({common_key: faker.word(), faker.word(): faker.word()})
    obj2 = JsonObject({common_key: faker.word(), faker.word(): faker.word()})

    # When: We merge the two JsonObjects
    result = obj1.merge(obj2)

    # Then: The result should have keys from both objects,
    # value from the second JsonObject for the common key
    assert len(dict(result)) == 3


def test_should_merge_json_object_with_empty(faker: Faker) -> None:
    # Given: A JsonObject and an empty JsonObject
    obj1 = JsonObject({faker.word(): faker.word(), faker.word(): faker.word()})
    obj2 = JsonObject({})

    # When: We merge the JsonObject with an empty JsonObject
    result = obj1.merge(obj2)

    # Then: The result should be the same as the original JsonObject
    assert dict(result) == dict(obj1)


def test_should_merge_empty_json_objects(faker: Faker) -> None:
    # Given: Two empty JsonObjects
    obj1 = JsonObject({})
    obj2 = JsonObject({})

    # When: We merge the two empty JsonObjects
    result = obj1.merge(obj2)

    # Then: The result should be an empty JsonObject
    assert dict(result) == {}
