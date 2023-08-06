from typing import Optional, List
from datetime import datetime
from typing_extensions import Literal, Final

class ExeScriptCommandResult(object):
    index: int  # readonly: False
    result: Literal["Ok","Error"]  # readonly: False
    stdout: Optional[str]  # readonly: False
    stderr: Optional[str]  # readonly: False
    message: Optional[str]  # readonly: False
    is_batch_finished: Optional[bool]  # readonly: False

    def __init__(self,
        index: int,
        result: Literal["Ok","Error"],
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
        message: Optional[str] = None,
        is_batch_finished: Optional[bool] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class ProviderEvent(object):
    event_type: str  # readonly: False
    activity_id: str  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str
    ) -> None: ...
    def to_dict(self) -> dict: ...


class Credentials(object):
    sgx: SgxCredentials  # readonly: False

    def __init__(self,
        sgx: SgxCredentials
    ) -> None: ...
    def to_dict(self) -> dict: ...


class SgxCredentials(object):
    enclave_pub_key: str  # readonly: False
    requestor_pub_key: str  # readonly: False
    payload_hash: str  # readonly: False
    ias_report: str  # readonly: False
    ias_sig: str  # readonly: False

    def __init__(self,
        enclave_pub_key: str,
        requestor_pub_key: str,
        payload_hash: str,
        ias_report: str,
        ias_sig: str
    ) -> None: ...
    def to_dict(self) -> dict: ...


class ErrorMessage(object):
    message: Optional[str]  # readonly: False

    def __init__(self,
        message: Optional[str] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class CreateActivityRequest(object):
    agreement_id: str  # readonly: False
    requestor_pub_key: Optional[str]  # readonly: False

    def __init__(self,
        agreement_id: str,
        requestor_pub_key: Optional[str] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class ActivityState(object):
    state: list  # readonly: False
    reason: Optional[str]  # readonly: False
    error_message: Optional[str]  # readonly: False

    def __init__(self,
        state: list,
        reason: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class ActivityUsage(object):
    current_usage: Optional[list]  # readonly: False
    timestamp: Optional[int]  # readonly: False

    def __init__(self,
        current_usage: Optional[list] = None,
        timestamp: Optional[int] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class CreateActivityResult(object):
    activity_id: str  # readonly: False
    credentials: Credentials  # readonly: False

    def __init__(self,
        activity_id: str,
        credentials: Credentials = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class ExeScriptRequest(object):
    text: str  # readonly: False

    def __init__(self,
        text: str
    ) -> None: ...
    def to_dict(self) -> dict: ...


class ExeScriptCommandState(object):
    command: str  # readonly: False
    progress: Optional[str]  # readonly: False
    params: Optional[list]  # readonly: False

    def __init__(self,
        command: str,
        progress: Optional[str] = None,
        params: Optional[list] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class DestroyActivity(ProviderEvent):
    agreement_id: Optional[str]  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str,
        agreement_id: Optional[str] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class DestroyActivityAllOf(ProviderEvent):
    agreement_id: Optional[str]  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str,
        agreement_id: Optional[str] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class CreateActivity(ProviderEvent):
    agreement_id: Optional[str]  # readonly: False
    requestor_pub_key: Optional[str]  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str,
        agreement_id: Optional[str] = None,
        requestor_pub_key: Optional[str] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


class CreateActivityAllOf(ProviderEvent):
    agreement_id: Optional[str]  # readonly: False
    requestor_pub_key: Optional[str]  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str,
        agreement_id: Optional[str] = None,
        requestor_pub_key: Optional[str] = None
    ) -> None: ...
    def to_dict(self) -> dict: ...


