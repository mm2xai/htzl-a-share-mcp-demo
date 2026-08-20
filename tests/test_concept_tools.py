"""tools/concept_tools.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from htzl_a_share_mcp.tools.concept_tools import (
    get_concept_board, get_dragon_tiger_board,
    get_northbound_flow, get_hot_money,
)


class TestConceptTools:
    """题材/龙虎榜/北向/游资 工具测试"""

    def test_get_concept_board(self):
        result = get_concept_board()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert "code" in result[0]
        assert "name" in result[0]

    def test_get_dragon_tiger_board(self):
        result = get_dragon_tiger_board()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert "symbol" in result[0]
        assert "buy_seats" in result[0]

    def test_get_northbound_flow(self):
        result = get_northbound_flow(days=30)
        assert isinstance(result, list)
        assert len(result) >= 1
        assert "date" in result[0]
        assert "total_net" in result[0]

    def test_get_hot_money(self):
        result = get_hot_money()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert "hot_money_seats" in result[0]


def test_all():
    total, passed = 0, 0
    for cls in [TestConceptTools]:
        for method in dir(cls):
            if method.startswith("test_"):
                total += 1
                try:
                    getattr(cls(), method)()
                    passed += 1
                    print(f"  ✓ {cls.__name__}.{method}")
                except Exception as e:
                    print(f"  ✗ {cls.__name__}.{method}: {e}")
    print(f"\n{passed}/{total} tests passed")
    assert passed == total


if __name__ == "__main__":
    test_all()
