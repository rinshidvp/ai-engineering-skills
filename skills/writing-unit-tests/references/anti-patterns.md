# Unit Test Anti-Patterns

Read only when writing or reviewing tests. Bad vs good side by side.

## Testing nothing

```python
# BAD: framework mechanics
assert [].get("key") is None

# BAD: construction
obj = MyClass(x=1)
assert obj.x == 1

# BAD: getter roundtrip
obj.value = 10
assert obj.value == 10
```

Delete all three. Test business logic, not language.

## Mocking your own code

```python
# BAD: mock internals
obj._internal = Stub()
obj.process()
# You bypassed the code you claim to test.

# GOOD: use real code, mock boundary only
service = Service(api=mock_external_api)
result = service.process(real_input)
assert result.status == "completed"
```

## Circular tests (testing the mock)

```python
# BAD: stub returns X, assert X — proves stub works
mock.get_data.return_value = {"key": "value"}
assert processor.process(mock) == {"key": "value"}

# GOOD: real data + real assertion
result = processor.process(real_data)
assert result.transformed_key == expected
```

## Silent fakes hide behavior

```python
# BAD: stop() is no-op on idle, test still passes if you delete stop() calls
agent = FakeAgent.idle()
handler.cleanup(agents)
assert agents.is_empty()

# GOOD: observable fake proves it happened
runtime = FakeRuntime()  # tracks stop_count
handler.cleanup(handles, runtime)
assert runtime.stop_count == 3
assert handles.is_empty()
```

## Over-mocking

- 5+ mocks in one test = function does too much, reduce coupling
- `stub.log.assert_called_exactly(3)` = fragile, breaks on unrelated change
- Unrealistic stub `returns "string"` when real API returns map = hides mismatch

## Stats padding

```
BAD:  "24/24 existing pass, no regressions"
GOOD: "New test_synonyms_in_prompt passes - proves feature works"
```

You need both, but only the second declares the feature done.
