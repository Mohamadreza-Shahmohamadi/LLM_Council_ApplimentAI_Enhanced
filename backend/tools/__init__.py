"""
AI Tools implementation.
Extracted and adapted from Reeteshrajesh/llm-council.
"""

import os
from typing import List, Optional
import math

# Tool import: prefer langchain_core, fall back to langchain.tools
try:
    from langchain_core.tools import Tool
except ImportError:
    from langchain.tools import Tool

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import yfinance as yf

# Optional: Python REPL
try:
    from langchain_experimental.tools import PythonREPLTool
except ImportError:
    PythonREPLTool = None

# Optional: Tavily
try:
    from langchain_community.tools.tavily_search import TavilySearchResults
except Exception:
    TavilySearchResults = None

from ..config import get_tool_config

def calculator_tool() -> Tool:
    """Calculator/REPL tool."""
    if PythonREPLTool is not None:
        repl = PythonREPLTool()
        return Tool(
            name="calculator",
            func=repl.run,
            description="Execute Python code for calculations or quick logic (e.g., '2+2', 'sum([1,2,3])').",
        )

    def _safe_eval(expr: str) -> str:
        try:
            allowed_globals = {"__builtins__": {}}
            allowed_locals = {"math": math}
            result = eval(expr, allowed_globals, allowed_locals)
            return str(result)
        except Exception as exc:
            return f"Error: {exc}"

    return Tool(
        name="calculator",
        func=_safe_eval,
        description="Basic calculator (math.* available) when PythonREPLTool is unavailable.",
    )

def wikipedia_tool() -> Tool:
    """Wikipedia lookup."""
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    return Tool(
        name="wikipedia",
        func=wikipedia.run,
        description="Search Wikipedia for factual information.",
    )

def arxiv_tool() -> Tool:
    """ArXiv search."""
    arxiv = ArxivQueryRun()
    return Tool(
        name="arxiv",
        func=arxiv.run,
        description="Search ArXiv for research papers.",
    )

def yahoo_finance_tool() -> Tool:
    """Yahoo Finance stock data."""
    def get_stock_price(ticker: str) -> str:
        symbol = (ticker or "").strip().split()[0].upper()
        if not symbol:
            return "Error: missing ticker symbol"
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            return f"{symbol}: ${price}" if price else f"{symbol}: Price not found"
        except Exception as exc:
            return f"Error fetching {ticker}: {exc}"

    return Tool(
        name="stock_data",
        func=get_stock_price,
        description="Get stock price via Yahoo Finance (e.g., 'AAPL').",
    )

def tavily_tool(api_key: str) -> Tool:
    """Tavily search."""
    if TavilySearchResults is None:
        return None
    
    search = TavilySearchResults(
        api_key=api_key,
        max_results=3,
        search_depth="advanced",
    )
    return Tool(
        name="tavily_search",
        func=search.invoke,
        description="Advanced web search for current events.",
    )

def get_available_tools() -> List[Tool]:
    """Return enabled tools based on config."""
    config = get_tool_config()
    
    if not config["enable_tools"]:
        return []

    available = config["available_tools"]
    tools = []

    if "calculator" in available:
        tools.append(calculator_tool())
    if "wikipedia" in available:
        tools.append(wikipedia_tool())
    if "arxiv" in available:
        tools.append(arxiv_tool())
    if "finance" in available:
        tools.append(yahoo_finance_tool())
    
    # Tavily is handled via search provider usually, but can be a tool too
    if config["tavily_api_key"]:
        t_tool = tavily_tool(config["tavily_api_key"])
        if t_tool:
            tools.append(t_tool)

    return [t for t in tools if t is not None]
