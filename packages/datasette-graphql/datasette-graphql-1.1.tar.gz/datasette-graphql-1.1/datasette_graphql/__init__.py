from click import ClickException
from datasette import hookimpl
from datasette.utils.asgi import Response, NotFound
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphql.error import format_error
from graphql import graphql, print_schema
import json
from .utils import schema_for_database_via_cache
import time

DEFAULT_TIME_LIMIT_MS = 1000
DEFAULT_NUM_QUERIES_LIMIT = 100


async def post_body(request):
    body = b""
    more_body = True
    while more_body:
        message = await request.receive()
        assert message["type"] == "http.request", message
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    return body


async def view_graphql_schema(request, datasette):
    database = request.url_vars.get("database")
    try:
        datasette.get_database(database)
    except KeyError:
        raise NotFound("Database does not exist")
    schema = await schema_for_database_via_cache(datasette, database=database)
    return Response.text(print_schema(schema))


CORS_HEADERS = {
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Allow-Method": "POST",
    "Access-Control-Allow-Origin": "*",
    "Vary": "accept",
}


async def view_graphql(request, datasette):
    if request.method == "OPTIONS":
        return Response.text("ok", headers=CORS_HEADERS if datasette.cors else {})

    body = await post_body(request)
    database = request.url_vars.get("database")

    try:
        datasette.get_database(database)
    except KeyError:
        raise NotFound("Database does not exist")

    if not body and "text/html" in request.headers.get("accept", ""):
        return Response.html(
            await datasette.render_template(
                "graphiql.html",
                {
                    "database": database,
                },
                request=request,
            ),
            headers=CORS_HEADERS if datasette.cors else {},
        )

    schema = await schema_for_database_via_cache(datasette, database=database)

    if request.args.get("schema"):
        return Response.text(print_schema(schema))

    incoming = {}
    if body:
        incoming = json.loads(body)
        query = incoming.get("query")
        variables = incoming.get("variables")
        operation_name = incoming.get("operationName")
    else:
        query = request.args.get("query")
        variables = request.args.get("variables", "")
        if variables:
            variables = json.loads(variables)
        operation_name = request.args.get("operationName")

    if not query:
        return Response.json(
            {"error": "Missing query"},
            status=400,
            headers=CORS_HEADERS if datasette.cors else {},
        )

    config = datasette.plugin_config("datasette-graphql") or {}
    context = {
        "time_started": time.monotonic(),
        "time_limit_ms": config.get("time_limit_ms") or DEFAULT_TIME_LIMIT_MS,
        "num_queries_executed": 0,
        "num_queries_limit": config.get("num_queries_limit")
        or DEFAULT_NUM_QUERIES_LIMIT,
    }

    result = await graphql(
        schema,
        query,
        operation_name=operation_name,
        variable_values=variables,
        context_value=context,
        executor=AsyncioExecutor(),
        return_promise=True,
    )
    response = {"data": result.data}
    if result.errors:
        response["errors"] = [format_error(error) for error in result.errors]

    return Response.json(
        response,
        status=200 if not result.errors else 500,
        headers=CORS_HEADERS if datasette.cors else {},
    )


@hookimpl
def menu_links(datasette, actor):
    return [
        {"href": datasette.urls.path("/graphql"), "label": "GraphQL API"},
    ]


@hookimpl
def register_routes():
    return [
        (r"^/graphql/(?P<database>[^/]+)\.graphql$", view_graphql_schema),
        (r"^/graphql/(?P<database>[^/]+)$", view_graphql),
        (r"^/graphql$", view_graphql),
    ]


@hookimpl
def extra_template_vars(datasette):
    async def graphql_template_tag(query, database=None, variables=None):
        schema = await schema_for_database_via_cache(datasette, database=database)
        result = await graphql(
            schema,
            query,
            executor=AsyncioExecutor(),
            return_promise=True,
            variable_values=variables or {},
        )
        if result.errors:
            raise Exception(result.errors)
        else:
            return result.data

    return {
        "graphql": graphql_template_tag,
    }


@hookimpl
def startup(datasette):
    # Validate configuration
    config = datasette.plugin_config("datasette-graphql") or {}
    if "databases" in config:
        for database_name in config["databases"].keys():
            try:
                datasette.get_database(database_name)
            except KeyError:
                raise ClickException(
                    "datasette-graphql config error: '{}' is not a connected database".format(
                        database_name
                    )
                )
