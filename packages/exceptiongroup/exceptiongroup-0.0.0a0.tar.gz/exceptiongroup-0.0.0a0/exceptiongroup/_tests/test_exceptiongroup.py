import copy
import pytest

from exceptiongroup import ExceptionGroup


def raise_group():
    try:
        1 / 0
    except Exception as e:
        raise ExceptionGroup("ManyError", [e], [str(e)]) from e


def test_exception_group_init():
    memberA = ValueError("A")
    memberB = RuntimeError("B")
    group = ExceptionGroup(
        "many error.", [memberA, memberB], [str(memberA), str(memberB)]
    )
    assert group.exceptions == [memberA, memberB]
    assert group.message == "many error."
    assert group.sources == [str(memberA), str(memberB)]
    assert group.args == (
        "many error.",
        [memberA, memberB],
        [str(memberA), str(memberB)],
    )


def test_exception_group_when_members_are_not_exceptions():
    with pytest.raises(TypeError):
        ExceptionGroup(
            "error",
            [RuntimeError("RuntimeError"), "error2"],
            ["RuntimeError", "error2"],
        )


def test_exception_group_init_when_exceptions_messages_not_equal():
    with pytest.raises(ValueError):
        ExceptionGroup(
            "many error.", [ValueError("A"), RuntimeError("B")], ["A"]
        )


def test_exception_group_str():
    memberA = ValueError("memberA")
    memberB = ValueError("memberB")
    group = ExceptionGroup(
        "many error.", [memberA, memberB], [str(memberA), str(memberB)]
    )
    assert "memberA" in str(group)
    assert "memberB" in str(group)

    assert "ExceptionGroup: " in repr(group)
    assert "memberA" in repr(group)
    assert "memberB" in repr(group)


def test_exception_group_copy():
    try:
        raise_group()  # the exception is raise by `raise...from..`
    except ExceptionGroup as e:
        group = e

    another_group = copy.copy(group)
    assert another_group.message == group.message
    assert another_group.exceptions == group.exceptions
    assert another_group.sources == group.sources
    assert another_group.__traceback__ is group.__traceback__
    assert another_group.__cause__ is group.__cause__
    assert another_group.__context__ is group.__context__
    assert another_group.__suppress_context__ is group.__suppress_context__
    assert another_group.__cause__ is not None
    assert another_group.__context__ is not None
    assert another_group.__suppress_context__ is True

    # doing copy when __suppress_context__ is False
    group.__suppress_context__ = False
    another_group = copy.copy(group)
    assert another_group.__cause__ is group.__cause__
    assert another_group.__context__ is group.__context__
    assert another_group.__suppress_context__ is group.__suppress_context__
    assert another_group.__suppress_context__ is False
