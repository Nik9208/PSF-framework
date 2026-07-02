from typing import TypedDict, Literal

class EpistemicScore(TypedDict):
    raw_value: float
    null_mean: float
    null_std: float
    z_score: float
    surrogate_type: Literal["FT", "IAAFT", "WHITE_NOISE"]
