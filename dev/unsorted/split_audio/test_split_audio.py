import pytest
from dev.wip.split_audio.split_audio import pick_optimal_segment_duration_ffmpeg


@pytest.mark.parametrize(
    "duration, min_segment, max_segment, min_chunk, max_chunk, expected",
    [
        (60, None, None, None, None, pytest.raises(ValueError)),
        (60, 10, 5, None, None, pytest.raises(ValueError)),
        (60, None, 10, None, 5, pytest.raises(ValueError)),
        (60, 5, None, 10, 5, pytest.raises(ValueError)),
        (60, None, 10, 10, 5, pytest.raises(ValueError)),
        (60, 5, 10, None, 5, pytest.raises(ValueError)),
        (60, 5, 10, 10, 5, pytest.raises(ValueError)),
    ],
)
def test_invalid_arguments(
    duration, min_segment, max_segment, min_chunk, max_chunk, expected
):
    with expected:
        pick_optimal_segment_duration_ffmpeg(
            duration, min_segment, max_segment, min_chunk, max_chunk
        )


@pytest.mark.parametrize(
    "duration, min_segment, max_segment, min_chunk, max_chunk, expected",
    [
        # Single values filled
        (60, None, 10, 10, None, 6),
        (60, 5, None, None, 5, 12),
        (60, 10, None, None, None, 10),
        (60, None, 10, None, None, 10),
        (60, None, None, None, 5, 12),
        (60, None, None, 10, None, 6),
        # Two values filled
        (60, 5, 10, None, None, 5),
        (60, 5, None, None, 5, 12),
        (60, None, 10, 10, None, 6),
        (60, 10, None, None, 5, 12),
        (60, None, 10, None, 10, 6),
        # Three values filled
        (60, 5, 10, 10, None, 5),
        # Four values filled
        (60, 5, 10, 10, 24, 5),
        (
            60,
            5,
            10,
            6,
            10,
            6,
        ),  # max chunk duration 10 -> 6 chunks - not 5 which is min.
    ],
)
def test_valid_arguments(
    duration, min_segment, max_segment, min_chunk, max_chunk, expected
):
    assert (
        pick_optimal_segment_duration_ffmpeg(
            duration, min_segment, max_segment, min_chunk, max_chunk
        )
        == expected
    )
