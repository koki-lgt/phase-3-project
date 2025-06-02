import pytest
from click.testing import CliRunner
from models.cli import cli  # adjust import if cli.py location changes
from models.database import Base, engine, SessionLocal

# Fixture to create a clean database for tests
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

# Fixture to provide a runner to invoke CLI commands
@pytest.fixture
def runner():
    return CliRunner()

def test_user_create_and_list(runner):
    # Create user
    result = runner.invoke(cli, ["user", "create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Created user" in result.output

    # Attempt to create same user again (should show already exists)
    result = runner.invoke(cli, ["user", "create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "already exists" in result.output

    # List users and check output contains Alice
    result = runner.invoke(cli, ["user", "list"])
    assert result.exit_code == 0
    assert "Alice" in result.output

def test_food_entry_add_and_list(runner):
    # Add food entry for Alice
    result = runner.invoke(
        cli,
        [
            "entry", "add",
            "--user", "Alice",
            "--food", "Banana",
            "--calories", "100",
            "--date", "2025-06-01"
        ]
    )
    assert result.exit_code == 0
    assert "Added entry" in result.output

    # List entries for Alice and check output contains Banana
    result = runner.invoke(cli, ["entry", "list", "--user", "Alice"])
    assert result.exit_code == 0
    assert "Banana" in result.output

    # List entries filtered by date
    result = runner.invoke(cli, ["entry", "list", "--date", "2025-06-01"])
    assert result.exit_code == 0
    assert "Banana" in result.output
