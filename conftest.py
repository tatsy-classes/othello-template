def pytest_addoption(parser):
    parser.addoption("--n_match", action="store", type=int, default=10)
