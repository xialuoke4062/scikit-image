import numpy as np
from numpy.testing import assert_equal, assert_raises, assert_almost_equal
from skimage.measure import LineModel, CircleModel, EllipseModel


def test_line_model_invalid_input():
    assert_raises(ValueError, LineModel().estimate, np.empty((5, 3)))


def test_line_model_predict():
    model = LineModel()
    model._params = (10, 1)
    x = np.arange(-10, 10)
    y = model.predict_y(x)
    assert_almost_equal(x, model.predict_x(y))


def test_line_model_is_degenerate():
    assert_equal(LineModel().is_degenerate(np.empty((1, 2))), True)


def test_line_model_estimate():
    # generate original data without noise
    model0 = LineModel()
    model0._params = (10, 1)
    x0 = np.arange(-100, 100)
    y0 = model0.predict_y(x0)
    data0 = np.column_stack([x0, y0])

    # add gaussian noise to data
    np.random.seed(1234)
    data = data0 + np.random.normal(size=data0.shape)

    # estimate parameters of noisy data
    model_est = LineModel()
    model_est.estimate(data)

    # test whether estimated parameters almost equals original parameters
    assert_almost_equal(model0._params, model_est._params, 1)


def test_circle_model_invalid_input():
    assert_raises(ValueError, CircleModel().estimate, np.empty((5, 3)))


def test_circle_model_predict():
    model = CircleModel()
    r = 5
    model._params = (0, 0, r)
    t = np.arange(0, 2 * np.pi, np.pi / 2)

    xy = np.array(((5, 0), (0, 5), (-5, 0), (0, -5)))
    assert_almost_equal(xy, model.predict_xy(t))


def test_circle_model_is_degenerate():
    assert_equal(CircleModel().is_degenerate(np.empty((1, 2))), True)


def test_circle_model_estimate():
    # generate original data without noise
    model0 = CircleModel()
    model0._params = (10, 12, 3)
    t = np.linspace(0, 2 * np.pi, 1000)
    data0 = model0.predict_xy(t)

    # add gaussian noise to data
    np.random.seed(1234)
    data = data0 + np.random.normal(size=data0.shape)

    # estimate parameters of noisy data
    model_est = CircleModel()
    model_est.estimate(data)

    # test whether estimated parameters almost equals original parameters
    assert_almost_equal(model0._params, model_est._params, 1)


if __name__ == "__main__":
    np.testing.run_module_suite()
