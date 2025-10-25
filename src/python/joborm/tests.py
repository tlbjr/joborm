#!/usr/bin/env python3
"""Tests for Job Opportunity Relationship Management"""

from pydantic import ValidationError
import pytest

from schemas import ProcessItem, ProcessItemType

from sample_data import opportunities

# TODO Move to pytest format and code coverage

if __name__ == "__main__":
    for i, opportunity in enumerate(opportunities):
        if i == 0:
            # Mocked 0 index is None
            continue
        print(f"#{i + 1} {opportunity}")
        if opportunity and opportunity.process and opportunity.process.items:
            for j, item in enumerate(opportunity.process.items):
                print(f"  Step {j + 1}: {item}")

    assert opportunities[1]
    assert opportunities[1].process.items[3].type_ == ProcessItemType.TECHNICAL_CODING
    assert opportunities[3]
    assert opportunities[3].process.items[3].type_ == ProcessItemType.TECHNICAL_TAKE_HOME

    with pytest.raises(ValidationError):
        ProcessItem(type_=ProcessItemType.UNKNOWN, location="inperson", with_="unknown")  # type: ignore
