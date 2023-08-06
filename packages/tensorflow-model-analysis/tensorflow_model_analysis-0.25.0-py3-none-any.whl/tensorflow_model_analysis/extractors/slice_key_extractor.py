# Lint as: python3
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Public API for extracting slice keys."""

from __future__ import absolute_import
from __future__ import division
# Standard __future__ imports
from __future__ import print_function

import copy

from typing import List, Optional

import apache_beam as beam

from tensorflow_model_analysis import config
from tensorflow_model_analysis import constants
from tensorflow_model_analysis import types
from tensorflow_model_analysis import util
from tensorflow_model_analysis.extractors import extractor
from tensorflow_model_analysis.slicer import slicer_lib as slicer

SLICE_KEY_EXTRACTOR_STAGE_NAME = 'ExtractSliceKeys'


def SliceKeyExtractor(
    slice_spec: Optional[List[slicer.SingleSliceSpec]] = None,
    eval_config: Optional[config.EvalConfig] = None,
    materialize: Optional[bool] = True) -> extractor.Extractor:
  """Creates an extractor for extracting slice keys.

  The incoming Extracts must contain a FeaturesPredictionsLabels extract keyed
  by tfma.FEATURES_PREDICTIONS_LABELS_KEY. Typically this will be obtained by
  calling the PredictExtractor.

  The extractor's PTransform yields a copy of the Extracts input with an
  additional extract pointing at the list of SliceKeyType values keyed by
  tfma.SLICE_KEY_TYPES_KEY. If materialize is True then a materialized version
  of the slice keys will be added under the key tfma.MATERIALZED_SLICE_KEYS_KEY.

  Args:
    slice_spec: Deprecated (use EvalConfig).
    eval_config: Optional EvalConfig containing slicing_specs specifying the
      slices to slice the data into. If slicing_specs are empty, defaults to
      overall slice.
    materialize: True to add MaterializedColumn entries for the slice keys.

  Returns:
    Extractor for slice keys.
  """
  if slice_spec and eval_config:
    raise ValueError('slice_spec is deprecated, only use eval_config')
  if eval_config:
    slice_spec = [
        slicer.SingleSliceSpec(spec=spec) for spec in eval_config.slicing_specs
    ]
  if not slice_spec:
    slice_spec = [slicer.SingleSliceSpec()]
  return extractor.Extractor(
      stage_name=SLICE_KEY_EXTRACTOR_STAGE_NAME,
      ptransform=ExtractSliceKeys(slice_spec, materialize))


@beam.typehints.with_input_types(types.Extracts)
@beam.typehints.with_output_types(types.Extracts)
class ExtractSliceKeysFn(beam.DoFn):
  """A DoFn that extracts slice keys that apply per example."""

  def __init__(self, slice_spec: List[slicer.SingleSliceSpec],
               materialize: bool):
    self._slice_spec = slice_spec
    self._materialize = materialize

  def process(self, element: types.Extracts) -> List[types.Extracts]:
    features = util.get_features_from_extracts(element)
    slices = list(
        slicer.get_slices_for_features_dict(features, self._slice_spec))

    # Make a a shallow copy, so we don't mutate the original.
    element_copy = copy.copy(element)

    element_copy[constants.SLICE_KEY_TYPES_KEY] = slices
    # Add a list of stringified slice keys to be materialized to output table.
    if self._materialize:
      element_copy[constants.SLICE_KEYS_KEY] = types.MaterializedColumn(
          name=constants.SLICE_KEYS_KEY,
          value=(list(
              slicer.stringify_slice_key(x).encode('utf-8') for x in slices)))
    return [element_copy]


@beam.ptransform_fn
@beam.typehints.with_input_types(types.Extracts)
@beam.typehints.with_output_types(types.Extracts)
def ExtractSliceKeys(extracts: beam.pvalue.PCollection,
                     slice_spec: List[slicer.SingleSliceSpec],
                     materialize: bool = True) -> beam.pvalue.PCollection:
  return extracts | beam.ParDo(ExtractSliceKeysFn(slice_spec, materialize))
