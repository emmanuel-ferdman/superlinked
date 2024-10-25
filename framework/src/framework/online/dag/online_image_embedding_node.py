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
from typing_extensions import override

from superlinked.framework.common.dag.context import ExecutionContext
from superlinked.framework.common.dag.image_embedding_node import ImageEmbeddingNode
from superlinked.framework.common.data_types import Vector
from superlinked.framework.common.interface.has_length import HasLength
from superlinked.framework.common.parser.parsed_schema import ParsedSchema
from superlinked.framework.common.schema.image_data import ImageData
from superlinked.framework.common.storage_manager.storage_manager import StorageManager
from superlinked.framework.common.transform.transform import Step
from superlinked.framework.common.transform.transformation_factory import (
    TransformationFactory,
)
from superlinked.framework.online.dag.default_online_node import DefaultOnlineNode
from superlinked.framework.online.dag.evaluation_result import (
    EvaluationResult,
    SingleEvaluationResult,
)
from superlinked.framework.online.dag.online_node import OnlineNode


class OnlineImageEmbeddingNode(
    DefaultOnlineNode[ImageEmbeddingNode, Vector], HasLength
):
    def __init__(
        self,
        node: ImageEmbeddingNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(node, parents, storage_manager)
        self._embedding_transformation = self._init_embedding_transformation()

    def _init_embedding_transformation(self) -> Step[Sequence[ImageData], list[Vector]]:
        return TransformationFactory.create_multi_embedding_transformation(
            self.node.transformation_config
        )

    @property
    @override
    def length(self) -> int:
        return self.node.length

    @property
    def embedding_transformation(self) -> Step[Sequence[ImageData], list[Vector]]:
        return self._embedding_transformation

    @override
    def evaluate_self(
        self,
        parsed_schemas: list[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector]]:
        if context.should_load_default_node_input:
            result = EvaluationResult(
                self._get_single_evaluation_result(
                    self.node.transformation_config.embedding_config.default_vector
                )
            )
            return [result] * len(parsed_schemas)
        return super().evaluate_self(parsed_schemas, context)

    @override
    def _evaluate_singles(
        self,
        parent_results: list[dict[OnlineNode, SingleEvaluationResult[ImageData]]],
        context: ExecutionContext,
    ) -> Sequence[Vector | None]:
        image_data_list = [
            list(parent_result.values())[0].value for parent_result in parent_results
        ]
        embedded_images = self.embedding_transformation.transform(
            image_data_list, context
        )
        return embedded_images