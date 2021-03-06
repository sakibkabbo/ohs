from typing import Generic, TypeVar

import attr
from graphene import Schema
from option import Result

from core.gql.graphql_request import GraphqlRequest

Context = TypeVar("Context")


@attr.s(slots=True, auto_attribs=True)
class GraphqlController(Generic[Context]):
    schema: Schema

    def execute(
        self, gql_request: GraphqlRequest, context: Context
    ) -> Result[dict, dict]:
        result = self.schema.execute(
            gql_request.query, variables=gql_request.variables, context=context
        )
        json = result.to_dict()
        if result.errors:
            return Result.Err(json)
        else:
            return Result.Ok(json)

    def introspect(self) -> Result[dict, dict]:
        try:
            result = self.schema.introspect()
        except Exception as e:
            return Result.Err({"errors": [str(e)]})
        else:
            return Result.Ok(result)
