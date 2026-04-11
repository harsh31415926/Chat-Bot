from __future__ import annotations
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("arith")


def _as_number(x):
    if isinstance(x, (int, float)):
        return float(x)

    if isinstance(x, str):
        return float(x.strip())

    raise TypeError("Expected a number")


@mcp.tool()
def add(a: float, b: float) -> float:
    return _as_number(a) + _as_number(b)


@mcp.tool()
def minus(a: float, b: float) -> float:
    return _as_number(a) - _as_number(b)


@mcp.tool()
def multiply(a: float, b: float) -> float:
    return _as_number(a) * _as_number(b)


@mcp.tool()
def divide(a: float, b: float) -> float:
    return _as_number(a) / _as_number(b)


@mcp.tool()
def power(a: float, b: float) -> float:
    return _as_number(a) ** _as_number(b)


@mcp.tool()
def modulo(a: float, b: float) -> float:
    return _as_number(a) % _as_number(b)


if __name__ == "__main__":
    mcp.run(transport = 'stdio')