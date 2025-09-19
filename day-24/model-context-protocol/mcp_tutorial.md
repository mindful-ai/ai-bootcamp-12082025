# Model Context Protocol (MCP) Tutorial

## Introduction

Model Context Protocol (MCP) is an open-standard protocol introduced by
Anthropic to allow large language models (LLMs) and AI agents to
interact with external tools, data sources, and workflows in a
standardized way.

------------------------------------------------------------------------

## Core Components

-   **MCP Host**: Environment containing the LLM/agent that uses
    context.
-   **MCP Client**: Library that communicates with MCP servers via
    JSON-RPC.
-   **MCP Server**: Provides tools, resources, and prompts to the
    client.
-   **Transport**: Supports stdio, HTTP/SSE for communication.

------------------------------------------------------------------------

## Applications

-   Assistants with live data (calendar, Slack, Notion, etc.).
-   IDE/code assistants for code search, linting, building, etc.
-   Workflow automation (databases, reports, emailing).
-   RAG + action-taking (retrieving context and performing updates).

------------------------------------------------------------------------

## Security Concerns

-   Tool poisoning, malicious servers.
-   Permissions and least privilege access.
-   Authentication and data privacy.
-   Prompt injection and misuse.

------------------------------------------------------------------------

## Workflow

1.  Client discovers available tools from server.
2.  User input triggers tool call.
3.  Server executes and responds with results.
4.  Client integrates results into LLM output.

------------------------------------------------------------------------

## Sample Code

### Python MCP Server

``` python
from mcp.python_sdk import MCPServer, ToolDef

def get_weather(city: str) -> dict:
    return {"city": city, "temperature_c": 25, "condition": "Sunny"}

async def main():
    server = MCPServer()
    server.register_tool(
        ToolDef(name="get_weather", description="Get weather", parameters={"city": "string"}),
        get_weather
    )
    await server.serve_via_stdio()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Python MCP Client

``` python
from mcp.python_sdk import MCPClient

async def main():
    client = MCPClient()
    await client.connect_http("http://localhost:8000/mcp")
    tools = await client.list_tools()
    print("Available tools:", tools)
    resp = await client.call_tool("get_weather", {"city": "Bengaluru"})
    print("Weather:", resp)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

------------------------------------------------------------------------

## Example JSON-RPC Messages

### List Tools

``` json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "ListTools",
  "params": {}
}
```

### Tool Invocation

``` json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "CallTool",
  "params": {
    "tool": "get_weather",
    "arguments": { "city": "Bengaluru" }
  }
}
```

------------------------------------------------------------------------

## Best Practices

-   Define clear tool schemas.
-   Apply versioning for tools/resources.
-   Validate inputs strictly.
-   Secure transport and enforce authentication.
-   Log actions and handle failures gracefully.

------------------------------------------------------------------------

## Conclusion

MCP is a powerful way to extend LLMs with external context, actions, and
workflows, providing a standardized interface that reduces integration
complexity while improving modularity and reusability.
