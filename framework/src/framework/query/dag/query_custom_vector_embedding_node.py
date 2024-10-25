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

from __future__ import annotations

from beartype.typing import Sequence

from superlinked.framework.common.dag.custom_node import CustomVectorEmbeddingNode
from superlinked.framework.common.data_types import Vector
from superlinked.framework.query.dag.query_embedding_node import QueryEmbeddingNode
from superlinked.framework.query.dag.query_node import QueryNode


class QueryCustomVectorEmbeddingNode(QueryEmbeddingNode[Vector, Vector]):
    def __init__(
        self, node: CustomVectorEmbeddingNode, parents: Sequence[QueryNode]
    ) -> None:
        super().__init__(node, parents, Vector)