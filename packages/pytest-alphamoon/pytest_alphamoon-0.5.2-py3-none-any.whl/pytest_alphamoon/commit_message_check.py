import re
from typing import Optional

import pytest
from git import Repo, exc

PLUGIN_NAME = 'commit-message-check'
CHECK_COMMIT_MESSAGES_FROM_INI = 'check_commit_messages_from'
PYTEST_NESTING_LEVEL = 'pytest_nesting_level'
MAX_LINE_LEN = 100

REGEX = re.compile(
    r'^((?P<alternative_format>Initial commit|Merge branch [\s\S]+?|Revert [\s\S]+?)|'
    r'((?P<header>'
    r'(?P<type>build|ci|chore|docs|dvc|feat|fix|perf|refactor|revert|style|test)?'
    r'(?P<scope>(?:\((?P<scope_text>[\s\S]*?)\)))?'
    r'(?P<breaking_change>!)?'
    r'(?P<colon>[\s\S]*?: ?)?'
    r'(?P<subject>.*))'
    r'(?P<footer>'
    r'((?P<footer_blank_line>(\r\n|\r|\n)(\r\n|\r|\n))|(\r\n|\r|\n))?'
    r'(?P<footer_text>[\s\S]*?))))$'
)


def check_commit_message(commit_message: str, error_msg_format: str) -> Optional[str]:
    match = REGEX.match(commit_message).groupdict()
    if not match.get('alternative_format'):
        if not match.get('type'):
            return error_msg_format.format("Missing or invalid commit type")

        if match.get('scope'):
            if not match.get('scope_text'):
                return error_msg_format.format("Scope must not be empty")
            if not match.get('scope_text').islower():
                return error_msg_format.format("Scope must be lowercase")
            if not match.get('scope_text').isalpha():
                return error_msg_format.format("Scope must be a word")

        if match.get('colon'):
            if not match.get('colon').startswith(':'):
                return error_msg_format.format("Unexpected characters before colon")
            if not match.get('colon').endswith(' '):
                return error_msg_format.format("No space after colon")
        else:
            return error_msg_format.format("Missing colon")

        if match.get('subject'):
            if not match.get('subject')[0].islower():
                return error_msg_format.format("Subject must start with lowercase letter")
            if not match.get('subject')[-1].isalnum():
                return error_msg_format.format("Subject must end with alphanum character")
        else:
            return error_msg_format.format("Missing subject")

        if match.get('footer_text'):
            if not match.get('footer_blank_line'):
                return error_msg_format.format("No blank line leading footer")
            if match.get('footer_text')[0].isspace():
                return error_msg_format.format("Footer must not start with whitespace")
            if match.get('footer_text')[-1].isspace():
                return error_msg_format.format("Footer must not end with whitespace")

    for i, line in enumerate(commit_message.splitlines(), 1):
        if len(line) > MAX_LINE_LEN:
            return error_msg_format.format(f"Too long line no. {i} ({len(line)}/{MAX_LINE_LEN})")


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        f"{PLUGIN_NAME}: Test to check whether git commit messages follow the naming convention")


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        f'--{PLUGIN_NAME}',
        dest=PLUGIN_NAME,
        action='store_true',
        help="Perform git commit messages checks",
    )

    parser.addini(CHECK_COMMIT_MESSAGES_FROM_INI, help=(
        "Specifies a beginning commit hash from which the commit messages are checked"
    ))

    parser.addini(PYTEST_NESTING_LEVEL, default=0, help=(
        "Specifies a pytest nesting level according to git repo directory"
    ))


def pytest_sessionstart(session):
    config = session.config
    if config.getoption(PLUGIN_NAME):
        try:
            level = int(config.getini(PYTEST_NESTING_LEVEL))
        except ValueError:
            raise ValueError(f"{PLUGIN_NAME}::Pytest nesting level must be integer")

        path = config.rootdir + '/..' * level
        try:
            config.repo = Repo(path=path)
        except exc.InvalidGitRepositoryError:
            raise RuntimeError(f"{PLUGIN_NAME}::Invalid Git repository: {path}")

        if config.repo.references:
            commit_rev = config.getini(CHECK_COMMIT_MESSAGES_FROM_INI)
            if commit_rev:
                try:
                    config.rev = f'{config.repo.commit(rev=commit_rev)}..{config.repo.commit()}'
                except (ValueError, exc.BadName):
                    raise ValueError(f"{PLUGIN_NAME}::Invalid beginning commit hash")
            else:
                config.rev = None

        else:
            raise RuntimeError(f"{PLUGIN_NAME}::Git repository must have at least one branch")


def pytest_collect_file(path, parent):
    config = parent.config
    if config.getoption(PLUGIN_NAME):
        return File.from_parent(parent, fspath=path)


class File(pytest.File):
    def collect(self):
        if self.config.repo:
            commits = list(self.config.repo.iter_commits(rev=self.config.rev, paths=self.fspath))
            if commits:
                yield CommitMessageItem.from_parent(self, commits=commits)


class CommitMessageItem(pytest.Item):
    def __init__(self, parent, commits: list):
        super().__init__(PLUGIN_NAME, parent)
        self.add_marker(PLUGIN_NAME)
        self.commits = commits

    def runtest(self):
        for commit in self.commits:
            error_msg_format = f"{{}}: {commit.hexsha} - {repr(commit.message)}"
            error_msg = check_commit_message(commit.message, error_msg_format)

            if error_msg:
                raise CommitMessageError(self.fspath, error_msg)

    def repr_failure(self, exc_info, **kwargs):
        if exc_info.errisinstance(CommitMessageError):
            return exc_info.value.get_message()
        return super().repr_failure(exc_info)

    def reportinfo(self):
        return self.fspath, -1, PLUGIN_NAME


class CommitMessageError(Exception):
    def __init__(self, path, message):
        self._path = path
        self._message = message

    def get_message(self):
        return f"{self._path}: {self._message}"
