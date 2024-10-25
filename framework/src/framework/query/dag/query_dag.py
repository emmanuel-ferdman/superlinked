# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from beartype.typing import Mapping, Sequence

from superlinked.framework.common.dag.context import ExecutionContext
from superlinked.framework.common.dag.exception import LeafNodeCountException
from superlinked.framework.common.data_types import Vector
from superlinked.framework.query.dag.query_index_node import QueryIndexNode
from superlinked.framework.query.dag.query_node import QueryNode
from superlinked.framework.query.query_node_input import QueryNodeInput


class QueryDag:
    def __init__(self, nodes: Sequence[QueryNode]) -> None:
        self.__nodes = nodes
        self.__leaf_node = self.__validate_and_get_leaf_node(self.__nodes)

    @property
    def leaf_node(self) -> QueryIndexNode:
        return self.__leaf_node

    def evaluate(
        self,
        inputs: Mapping[str, Sequence[QueryNodeInput]],
        context: ExecutionContext,
    ) -> Vector:
        return self.leaf_node.evaluate_with_validation(inputs, context)

    def __validate_and_get_leaf_node(
        self, nodes: Sequence[QueryNode]
    ) -> QueryIndexNode:
        class_name = type(self).__name__
        index_nodes = [node for node in nodes if isinstance(node, QueryIndexNode)]
        if len(index_nodes) != 1:
            raise LeafNodeCountException(
                f"{class_name} must have exactly one {QueryIndexNode.__name__}."
            )
        return index_nodes[0]