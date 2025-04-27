from mcp.server.fastmcp import FastMCP
from tools import get_all_cars, filter_cars, create_car, update_car, delete_car, count_cars_by_attribute

server = FastMCP(
    "ServerCarroQuery",
    port=80,
    host="0.0.0.0"
)

# Register tools
server.tool()(get_all_cars)
server.tool()(filter_cars)
server.tool()(create_car)
server.tool()(update_car)
server.tool()(delete_car)
server.tool()(count_cars_by_attribute)

if __name__ == "__main__":
    server.run(transport="sse")
