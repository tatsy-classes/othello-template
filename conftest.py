def pytest_addoption(parser):
    parser.addoption("--path", action="store", type=str, required=True)
