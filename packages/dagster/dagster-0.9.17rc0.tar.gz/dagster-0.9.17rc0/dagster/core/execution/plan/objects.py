from collections import namedtuple
from enum import Enum

from dagster import check
from dagster.core.definitions import AssetMaterialization, Materialization, Solid, SolidHandle
from dagster.core.definitions.events import EventMetadataEntry
from dagster.core.types.dagster_type import DagsterType
from dagster.serdes import whitelist_for_serdes
from dagster.utils import merge_dicts
from dagster.utils.error import SerializableErrorInfo


@whitelist_for_serdes
class StepOutputHandle(namedtuple("_StepOutputHandle", "step_key output_name")):
    @staticmethod
    def from_step(step, output_name="result"):
        check.inst_param(step, "step", ExecutionStep)

        return StepOutputHandle(step.key, output_name)

    def __new__(cls, step_key, output_name="result"):
        return super(StepOutputHandle, cls).__new__(
            cls,
            step_key=check.str_param(step_key, "step_key"),
            output_name=check.str_param(output_name, "output_name"),
        )


@whitelist_for_serdes
class StepInputData(namedtuple("_StepInputData", "input_name type_check_data")):
    def __new__(cls, input_name, type_check_data):
        return super(StepInputData, cls).__new__(
            cls,
            input_name=check.str_param(input_name, "input_name"),
            type_check_data=check.opt_inst_param(type_check_data, "type_check_data", TypeCheckData),
        )


@whitelist_for_serdes
class TypeCheckData(namedtuple("_TypeCheckData", "success label description metadata_entries")):
    def __new__(cls, success, label, description=None, metadata_entries=None):
        return super(TypeCheckData, cls).__new__(
            cls,
            success=check.bool_param(success, "success"),
            label=check.str_param(label, "label"),
            description=check.opt_str_param(description, "description"),
            metadata_entries=check.opt_list_param(
                metadata_entries, metadata_entries, of_type=EventMetadataEntry
            ),
        )


@whitelist_for_serdes
class UserFailureData(namedtuple("_UserFailureData", "label description metadata_entries")):
    def __new__(cls, label, description=None, metadata_entries=None):
        return super(UserFailureData, cls).__new__(
            cls,
            label=check.str_param(label, "label"),
            description=check.opt_str_param(description, "description"),
            metadata_entries=check.opt_list_param(
                metadata_entries, metadata_entries, of_type=EventMetadataEntry
            ),
        )


@whitelist_for_serdes
class StepOutputData(
    namedtuple(
        "_StepOutputData",
        "step_output_handle intermediate_materialization type_check_data version",
    )
):
    def __new__(
        cls,
        step_output_handle,
        intermediate_materialization=None,
        type_check_data=None,
        version=None,
    ):
        return super(StepOutputData, cls).__new__(
            cls,
            step_output_handle=check.inst_param(
                step_output_handle, "step_output_handle", StepOutputHandle
            ),
            intermediate_materialization=check.opt_inst_param(
                intermediate_materialization,
                "intermediate_materialization",
                (AssetMaterialization, Materialization),
            ),
            type_check_data=check.opt_inst_param(type_check_data, "type_check_data", TypeCheckData),
            version=check.opt_str_param(version, "version"),
        )

    @property
    def output_name(self):
        return self.step_output_handle.output_name


@whitelist_for_serdes
class StepFailureData(namedtuple("_StepFailureData", "error user_failure_data")):
    def __new__(cls, error, user_failure_data):
        return super(StepFailureData, cls).__new__(
            cls,
            error=check.opt_inst_param(error, "error", SerializableErrorInfo),
            user_failure_data=check.opt_inst_param(
                user_failure_data, "user_failure_data", UserFailureData
            ),
        )


@whitelist_for_serdes
class StepRetryData(namedtuple("_StepRetryData", "error seconds_to_wait")):
    def __new__(cls, error, seconds_to_wait=None):
        return super(StepRetryData, cls).__new__(
            cls,
            error=check.opt_inst_param(error, "error", SerializableErrorInfo),
            seconds_to_wait=check.opt_int_param(seconds_to_wait, "seconds_to_wait"),
        )


@whitelist_for_serdes
class StepSuccessData(namedtuple("_StepSuccessData", "duration_ms")):
    def __new__(cls, duration_ms):
        return super(StepSuccessData, cls).__new__(
            cls, duration_ms=check.float_param(duration_ms, "duration_ms")
        )


@whitelist_for_serdes
class StepKind(Enum):
    COMPUTE = "COMPUTE"


class StepInputSourceType(Enum):
    SINGLE_OUTPUT = "SINGLE_OUTPUT"
    MULTIPLE_OUTPUTS = "MULTIPLE_OUTPUTS"
    CONFIG = "CONFIG"
    DEFAULT_VALUE = "DEFAULT_VALUE"
    CACHED_OUTPUT = "CACHED_OUTPUT"


class StepInput(
    namedtuple("_StepInput", "name dagster_type source_type source_handles config_data addresses")
):
    def __new__(
        cls,
        name,
        dagster_type=None,
        source_type=None,
        source_handles=None,
        config_data=None,
        addresses=None,
    ):
        return super(StepInput, cls).__new__(
            cls,
            name=check.str_param(name, "name"),
            dagster_type=check.inst_param(dagster_type, "dagster_type", DagsterType),
            source_type=check.inst_param(source_type, "source_type", StepInputSourceType),
            source_handles=check.opt_list_param(
                source_handles, "source_handles", of_type=StepOutputHandle
            ),
            config_data=config_data,  # can be any type
            addresses=check.opt_dict_param(
                addresses, "addresses", key_type=StepOutputHandle, value_type=str
            ),
        )

    @property
    def is_from_output(self):
        return (
            self.source_type == StepInputSourceType.SINGLE_OUTPUT
            or self.source_type == StepInputSourceType.MULTIPLE_OUTPUTS
        )

    @property
    def is_from_single_output(self):
        return self.source_type == StepInputSourceType.SINGLE_OUTPUT

    @property
    def is_from_config(self):
        return self.source_type == StepInputSourceType.CONFIG

    @property
    def is_from_default_value(self):
        return self.source_type == StepInputSourceType.DEFAULT_VALUE

    @property
    def is_from_multiple_outputs(self):
        return self.source_type == StepInputSourceType.MULTIPLE_OUTPUTS

    @property
    def is_from_cached_output(self):
        return self.source_type == StepInputSourceType.CACHED_OUTPUT and self.addresses is not None

    @property
    def dependency_keys(self):
        return {handle.step_key for handle in self.source_handles}


class StepOutput(
    namedtuple("_StepOutput", "name dagster_type optional should_materialize asset_store_handle")
):
    def __new__(
        cls,
        name,
        dagster_type=None,
        optional=None,
        should_materialize=None,
        asset_store_handle=None,
    ):
        from dagster.core.storage.asset_store import AssetStoreHandle

        return super(StepOutput, cls).__new__(
            cls,
            name=check.str_param(name, "name"),
            optional=check.bool_param(optional, "optional"),
            should_materialize=check.bool_param(should_materialize, "should_materialize"),
            dagster_type=check.inst_param(dagster_type, "dagster_type", DagsterType),
            asset_store_handle=check.opt_inst_param(
                asset_store_handle, "asset_store_handle", AssetStoreHandle
            ),
        )


class ExecutionStep(
    namedtuple(
        "_ExecutionStep",
        (
            "pipeline_name key_suffix step_inputs step_input_dict step_outputs step_output_dict "
            "compute_fn kind solid_handle solid logging_tags tags hook_defs"
        ),
    )
):
    def __new__(
        cls,
        pipeline_name,
        key_suffix,
        step_inputs,
        step_outputs,
        compute_fn,
        kind,
        solid_handle,
        solid,
        logging_tags=None,
    ):

        return super(ExecutionStep, cls).__new__(
            cls,
            pipeline_name=check.str_param(pipeline_name, "pipeline_name"),
            key_suffix=check.str_param(key_suffix, "key_suffix"),
            step_inputs=check.list_param(step_inputs, "step_inputs", of_type=StepInput),
            step_input_dict={si.name: si for si in step_inputs},
            step_outputs=check.list_param(step_outputs, "step_outputs", of_type=StepOutput),
            step_output_dict={so.name: so for so in step_outputs},
            compute_fn=check.callable_param(
                compute_fn, "compute_fn"
            ),  # Compute_fn is the compute function for the step.
            #     Not to be confused with the compute_fn of the passed in solid.
            kind=check.inst_param(kind, "kind", StepKind),
            solid_handle=check.inst_param(solid_handle, "solid_handle", SolidHandle),
            solid=check.inst_param(solid, "solid", Solid),
            logging_tags=merge_dicts(
                {
                    "step_key": str(solid_handle) + "." + key_suffix,
                    "pipeline": pipeline_name,
                    "solid": solid_handle.name,
                    "solid_definition": solid.definition.name,
                },
                check.opt_dict_param(logging_tags, "logging_tags"),
            ),
            tags=solid.tags,
            hook_defs=solid.hook_defs,
        )

    @property
    def key(self):
        return str(self.solid_handle) + "." + self.key_suffix

    @property
    def solid_name(self):
        return self.solid_handle.name

    def has_step_output(self, name):
        check.str_param(name, "name")
        return name in self.step_output_dict

    def step_output_named(self, name):
        check.str_param(name, "name")
        return self.step_output_dict[name]

    def has_step_input(self, name):
        check.str_param(name, "name")
        return name in self.step_input_dict

    def step_input_named(self, name):
        check.str_param(name, "name")
        return self.step_input_dict[name]
