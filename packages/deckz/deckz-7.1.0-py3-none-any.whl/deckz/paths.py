from logging import getLogger
from pathlib import Path
from typing import Optional

from appdirs import user_config_dir
from git import Repo
from git.exc import InvalidGitRepositoryError

from deckz import app_name
from deckz.exceptions import DeckzException


_logger = getLogger(__name__)


class Paths:
    def __init__(self, working_dir: str) -> None:
        self.working_dir = Path(working_dir).resolve()

        if not self.working_dir.relative_to(self.git_dir).match("*/*"):
            raise DeckzException(
                f"Not deep enough from root {self.git_dir}. "
                "Please follow the directory hierarchy root > company > deck and "
                "invoke this tool from the deck directory."
            )

        self.build_dir = self.working_dir / "build"
        self.pdf_dir = self.working_dir / "pdf"
        self.shared_dir = self.git_dir / "shared"
        self.shared_img_dir = self.shared_dir / "img"
        self.shared_code_dir = self.shared_dir / "code"
        self.shared_latex_dir = self.shared_dir / "latex"
        self.templates_dir = self.git_dir / "templates"
        self.yml_templates_dir = self.templates_dir / "yml"
        self.template_targets = self.yml_templates_dir / "targets.yml"
        self.template_global_config = self.yml_templates_dir / "global-config.yml"
        self.template_user_config = self.yml_templates_dir / "user-config.yml"
        self.template_company_config = self.yml_templates_dir / "company-config.yml"
        self.template_deck_config = self.yml_templates_dir / "deck-config.yml"
        self.jinja2_dir = self.templates_dir / "jinja2"
        self.jinja2_main_template = self.jinja2_dir / "main.tex"
        self.jinja2_print_template = self.jinja2_dir / "print.tex"
        self.user_config_dir = Path(user_config_dir(app_name))
        self.global_config = self.git_dir / "global-config.yml"
        self.gdrive_secrets = self.user_config_dir / "gdrive-secrets.json"
        self.gdrive_credentials = self.user_config_dir / "gdrive-credentials.pickle"
        self.user_config = self.user_config_dir / "user-config.yml"
        self.company_config = (
            self.git_dir
            / self.working_dir.relative_to(self.git_dir).parts[0]
            / "company-config.yml"
        )
        self.deck_config = self.working_dir / "deck-config.yml"
        self.session_config = self.working_dir / "session-config.yml"
        self.targets = self.working_dir / "targets.yml"

        self.user_config_dir.mkdir(parents=True, exist_ok=True)

    @property
    def git_dir(self) -> Path:
        if not hasattr(self, "_git_dir"):
            self._git_dir = get_git_dir(self.working_dir)
        return self._git_dir


def get_git_dir(path: Path) -> Optional[Path]:
    try:
        repository = Repo(str(path), search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        raise DeckzException(
            "Could not find the path of the current git working directory. "
            "Are you in one?"
        ) from e
    return Path(repository.git.rev_parse("--show-toplevel")).resolve()
