"""File for automatic testing and checking."""
import tempfile

import nox

locations = "src", "tests", "noxfile.py"
pythons = ["3.7", "3.8", "3.9"]
python = "3.9"


@nox.session(python=pythons)
def tests(session: nox.session) -> None:
    """Run the unit tests."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=python)
def black(session: nox.session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=pythons)
def lint(session: nox.session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-bugbear",
        "flake8-bandit",
        "flake8-annotations",
    )
    session.run("flake8", *args)


@nox.session(python=python)
def safety(session: nox.session) -> None:
    """Check for insecure code. See: https://safety.openfaa.org/."""
    with tempfile.NamedTemporaryFile() as req:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={req.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={req.name}", "--full-report")


@nox.session(python=python)
def mypy(session: nox.session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python=python)
def coverage(session: nox.session) -> None:
    session.install("coverage", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
