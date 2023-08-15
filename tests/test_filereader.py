import numpy as np
import pytest
from ovito.io import import_file


@pytest.fixture
def default_pipeline():
    pipe = import_file("examples/example_01/lmp.h5")
    yield pipe


def test_default_settings(default_pipeline):
    pipe = default_pipeline
    data = pipe.compute()
    expected = np.array(
        [
            [3.64500000e01, 0.00000000e00, 0.00000000e00, 0.00000000e00],
            [2.23191879e-15, 3.64500000e01, 0.00000000e00, 0.00000000e00],
            [2.23191879e-15, 2.23191879e-15, 3.64500000e01, 0.00000000e00],
        ]
    )
    assert np.allclose(data.cell, expected)


def test_round_cell():
    pipe = import_file(
        "examples/example_01/lmp.h5",
        roundCell=True,
    )
    data = pipe.compute()
    expected = np.array(
        [[[36.45, 0.0, 0.0, 0.0], [0.0, 36.45, 0.0, 0.0], [0.0, 0.0, 36.45, 0.0]]]
    )
    assert np.allclose(data.cell, expected)


def test_file_does_not_exist():
    with pytest.raises(RuntimeError) as excinfo:
        _ = import_file(
            "examples/example_01/lmp_no_file.h5",
        )
    assert (
        str(excinfo.value).replace("\n", " ")
        == "File does not exist: examples/example_01/lmp_no_file.h5"
    )


def test_trajectory_length(default_pipeline):
    pipe = default_pipeline
    assert pipe.source.num_frames == 101


def test_first_frame_content(default_pipeline):
    pipe = default_pipeline
    data = pipe.compute(0)
    assert data.particles.count == 2916
    assert data.attributes["SourceFrame"] == 0
    assert data.attributes["Temperature"] == 1000
    assert data.attributes["Timestep"] == 0
    assert np.isclose(data.attributes["Total energy"], -9420.97)


def test_last_frame_content(default_pipeline):
    pipe = default_pipeline
    data = pipe.compute(pipe.source.num_frames)
    assert data.particles.count == 2916
    assert data.attributes["SourceFrame"] == 100
    assert np.isclose(data.attributes["Temperature"], 498.03)
    assert data.attributes["Timestep"] == 1000
    assert np.isclose(data.attributes["Total energy"], -9403.94)
