from ExoticEngine.Solvers import ImpliedVol as IV
from ExoticEngine.Solvers import solvers
from ExoticEngine import MonteCarloPricer as Pricer
import numpy as np


def test_bisection_solver(tolerance=1e-7):
    linear_f = lambda x: 2 * x + 6
    quadratic_f = lambda x: 3 * x ** 2 + 6 + x + 1
    exp_f = lambda x: 2. * np.exp(0.5 * x) - 100
    functions = [linear_f, quadratic_f, exp_f]
    function_objs = [IV.InvertFunction(f_i) for f_i in functions]
    inputs = [-2000.1, 5.2, -0.5]
    targets = [functions[i](x) for i, x in enumerate(inputs)]
    bounds = [[-3000, 0], [0, 50], [-10, 100]]
    solver_tolerance = tolerance * 0.9
    assert tolerance > solver_tolerance >= 1e-10
    for i, f in enumerate(function_objs):
        bisection_solver = solvers.Bisection(func_obj=f,
                                             target=targets[i],
                                             start=bounds[i],
                                             tolerance=solver_tolerance,
                                             max_iteration=35)
        solver_result = bisection_solver.solver()
        assert abs(solver_result - inputs[i]) < tolerance


def test_newton_raphson_solver(tolerance=1e-7):
    function_objs = [IV.Polynomial([-24, 4]), IV.Polynomial([-12, 0, 1.2]), IV.Exponential(12, 0.2, -104)]
    inputs = [-2000.1, 5.2, -0.5]
    targets = [function_objs[i].f(x) for i, x in enumerate(inputs)]
    initial_guesses = [[-5123.42], [212.1], [3.2]]
    solver_tolerance = tolerance * 0.9
    assert tolerance > solver_tolerance >= 1e-10
    for i, f in enumerate(function_objs):
        NR_solver = solvers.NewtonRaphson(func_obj=f,
                                          target=targets[i],
                                          start=initial_guesses[i],
                                          tolerance=solver_tolerance,
                                          max_iteration=10)
        solver_result = NR_solver.solver()
        assert abs(solver_result - inputs[i]) < tolerance


def test_implied_vol_bisection_solver(tolerance=1e-8):
    S, K, T, r, vol = 100, 102, 3., 0.02, 0.45
    BS = [IV.BSModel(put_call_flag="CALL", spot=S, strike=K, rate=r, maturity=T), \
          IV.BSModel(put_call_flag="PUT", spot=S, strike=K, rate=r, maturity=T)]
    targets = [Pricer.BS_CALL(S, K, T, r, vol), Pricer.BS_PUT(S, K, T, r, vol)]
    bounds = [1e-5, 3.]
    solver_tolerance = tolerance * 0.9
    assert tolerance > solver_tolerance >= 1e-10
    for i, model in enumerate(BS):
        bisection_solver = solvers.Bisection(model,
                                             targets[i],
                                             start=bounds,
                                             tolerance=solver_tolerance,
                                             max_iteration=50)
        IV_result = bisection_solver.solver()
        assert abs(IV_result - vol) < tolerance


def test_implied_vol_NR_solver(tolerance=1e-8):
    S, K, T, r, vol = 100., 92., 6., 0.031, 0.41
    BS = [IV.BSModel(put_call_flag="CALL", spot=S, strike=K, rate=r, maturity=T), \
          IV.BSModel(put_call_flag="PUT", spot=S, strike=K, rate=r, maturity=T)]
    targets = [Pricer.BS_CALL(S, K, T, r, vol), Pricer.BS_PUT(S, K, T, r, vol)]
    start = [0.1]
    solver_tolerance = tolerance * 0.9
    assert tolerance > solver_tolerance >= 1e-10
    for i, model in enumerate(BS):
        NR_solver = solvers.NewtonRaphson(model,
                                          targets[i],
                                          start=start,
                                          tolerance=solver_tolerance,
                                          max_iteration=50)
        IV_result = NR_solver.solver()
        assert abs(IV_result - vol) < tolerance
