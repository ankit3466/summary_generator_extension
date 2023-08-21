from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Choice:
    finish_reason: str
    index: int
    logprobs: None
    text: str

    def __init__(self, finish_reason: str, index: int, logprobs: None, text: str) -> None:
        self.finish_reason = finish_reason
        self.index = index
        self.logprobs = logprobs
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'Choice':
        assert isinstance(obj, dict)
        finish_reason = from_str(obj.get("finish_reason"))
        index = from_int(obj.get("index"))
        logprobs = from_none(obj.get("logprobs"))
        text = from_str(obj.get("text"))
        return Choice(finish_reason, index, logprobs, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["finish_reason"] = from_str(self.finish_reason)
        result["index"] = from_int(self.index)
        result["logprobs"] = from_none(self.logprobs)
        result["text"] = from_str(self.text)
        return result


class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

    def __init__(self, completion_tokens: int, prompt_tokens: int, total_tokens: int) -> None:
        self.completion_tokens = completion_tokens
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens

    @staticmethod
    def from_dict(obj: Any) -> 'Usage':
        assert isinstance(obj, dict)
        completion_tokens = from_int(obj.get("completion_tokens"))
        prompt_tokens = from_int(obj.get("prompt_tokens"))
        total_tokens = from_int(obj.get("total_tokens"))
        return Usage(completion_tokens, prompt_tokens, total_tokens)

    def to_dict(self) -> dict:
        result: dict = {}
        result["completion_tokens"] = from_int(self.completion_tokens)
        result["prompt_tokens"] = from_int(self.prompt_tokens)
        result["total_tokens"] = from_int(self.total_tokens)
        return result


class ResponseModel:
    choices: List[Choice]
    created: int
    id: str
    model: str
    object: str
    usage: Usage
    warning: str

    def __init__(self, choices: List[Choice], created: int, id: str, model: str, object: str, usage: Usage, warning: str) -> None:
        self.choices = choices
        self.created = created
        self.id = id
        self.model = model
        self.object = object
        self.usage = usage
        self.warning = warning

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseModel':
        assert isinstance(obj, dict)
        choices = from_list(Choice.from_dict, obj.get("choices"))
        created = from_int(obj.get("created"))
        id = from_str(obj.get("id"))
        model = from_str(obj.get("model"))
        object = from_str(obj.get("object"))
        usage = Usage.from_dict(obj.get("usage"))
        warning = from_str(obj.get("warning"))
        return ResponseModel(choices, created, id, model, object, usage, warning)

    def to_dict(self) -> dict:
        result: dict = {}
        result["choices"] = from_list(lambda x: to_class(Choice, x), self.choices)
        result["created"] = from_int(self.created)
        result["id"] = from_str(self.id)
        result["model"] = from_str(self.model)
        result["object"] = from_str(self.object)
        result["usage"] = to_class(Usage, self.usage)
        result["warning"] = from_str(self.warning)
        return result


def response_model_from_dict(s: Any) -> ResponseModel:
    return ResponseModel.from_dict(s)


def response_model_to_dict(x: ResponseModel) -> Any:
    return to_class(ResponseModel, x)