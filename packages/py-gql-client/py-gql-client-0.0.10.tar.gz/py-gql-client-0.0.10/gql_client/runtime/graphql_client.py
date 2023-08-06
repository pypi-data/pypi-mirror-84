#!/usr/bin/env python3

from typing import Any, Dict

from gql import gql, Client
from .reporter import DUMMY_REPORTER, Reporter


class GraphqlClient:
    def __init__(
        self,
        client: Client,
        reporter: Reporter = DUMMY_REPORTER,
    ) -> None:

        """This is the class to use for working with graphql server

        Args:
            client (Client): Graphql client
            reporter (Reporter, optional): Use reporter.InventoryReporter to
                       store reports on all successful and failed mutations
                       in inventory. The default is DummyReporter that
                       discards reports

        """

        self.client = client
        self.reporter = reporter

    def call(self, query: str, variables: Dict[str, Any]) -> str:
        return self.client.execute(gql(query), variable_values=variables)
