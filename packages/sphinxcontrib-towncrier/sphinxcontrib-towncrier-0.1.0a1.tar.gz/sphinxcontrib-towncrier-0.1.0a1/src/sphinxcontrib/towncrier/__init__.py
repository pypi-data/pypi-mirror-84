"""Sphinx extension for injecting an unreleased changelog into docs."""


import subprocess  # noqa: S404
import sys
from contextlib import suppress as suppress_exceptions
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from sphinx.application import Sphinx
from sphinx.config import Config as SphinxConfig
from sphinx.environment import BuildEnvironment
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nested_parse_with_titles, nodes


# isort: split

# pylint: disable=import-error,no-name-in-module
from towncrier._settings import load_config_from_file  # noqa: WPS436


try:
    # pylint: disable=no-name-in-module
    from towncrier.build import find_fragments  # noqa: WPS433
except ImportError:
    # pylint: disable=import-self
    from towncrier import find_fragments  # noqa: WPS433, WPS440

# Ref: https://github.com/PyCQA/pylint/issues/3817
from docutils import statemachine  # pylint: disable=wrong-import-order

from ._version import __version__  # noqa: WPS436


PROJECT_ROOT_DIR = Path(__file__).parents[3].resolve()
TOWNCRIER_DRAFT_CMD = (
    sys.executable, '-m',  # invoke via runpy under the same interpreter
    'towncrier',
    '--draft',  # write to stdout, don't change anything on disk
)


@lru_cache(typed=True)
def _get_changelog_draft_entries(
        target_version: str,
        allow_empty: bool = False,
        working_dir: str = None,
        config_path: str = None,
) -> str:
    """Retrieve the unreleased changelog entries from Towncrier."""
    extra_cli_args: Tuple[str, ...] = (
        '--version',
        rf'\ {target_version}',  # version value to be used in the RST title
        # NOTE: The escaped space sequence (`\ `) is necessary to address
        # NOTE: a corner case when the towncrier config has something like
        # NOTE: `v{version}` in the title format **and** the directive target
        # NOTE: argument starts with a substitution like `|release|`. And so
        # NOTE: when combined, they'd produce `v|release|` causing RST to not
        # NOTE: substitute the `|release|` part. But adding an escaped space
        # NOTE: solves this: that escaped space renders as an empty string and
        # NOTE: the substitution gets processed properly so the result would
        # NOTE: be something like `v1.0` as expected.
    )
    if config_path is not None:
        # This isn't actually supported by a released version of Towncrier yet:
        # https://github.com/twisted/towncrier/pull/157#issuecomment-666549246
        # https://github.com/twisted/towncrier/issues/269
        extra_cli_args += '--config', str(config_path)
    towncrier_output = subprocess.check_output(  # noqa: S603
        TOWNCRIER_DRAFT_CMD + extra_cli_args,
        cwd=str(working_dir) if working_dir else None,
        universal_newlines=True,  # this arg has "text" alias since Python 3.7
    ).strip()

    if not allow_empty and 'No significant changes' in towncrier_output:
        raise LookupError('There are no unreleased changelog entries so far')

    return towncrier_output


# pylint: disable=fixme
# FIXME: refactor `_lookup_towncrier_fragments` to drop noqas
@lru_cache(maxsize=1, typed=True)  # noqa: WPS210
def _lookup_towncrier_fragments(  # noqa: WPS210
        working_dir: str = None,
        config_path: str = None,
) -> Set[Path]:
    """Emit RST-formatted Towncrier changelog fragment paths."""
    project_path = Path.cwd() if working_dir is None else Path(working_dir)

    final_config_path = project_path / 'pyproject.toml'
    if config_path is not None:
        final_config_path = project_path / config_path
    elif (  # noqa: WPS337
            not final_config_path.is_file() and
            (project_path / 'towncrier.toml').is_file()
    ):
        final_config_path = project_path / 'towncrier.toml'

    towncrier_config = load_config_from_file(str(final_config_path))
    fragment_directory: Optional[str] = 'newsfragments'
    try:
        fragment_base_directory = project_path / towncrier_config['directory']
    except KeyError:
        fragment_base_directory = project_path / towncrier_config['directory']
    else:
        fragment_directory = None

    _fragments, fragment_filenames = find_fragments(
        base_directory=str(fragment_base_directory),
        fragment_directory=fragment_directory,
        definitions=towncrier_config['types'],
        sections=towncrier_config['sections'],
    )
    return set(fragment_filenames)


@lru_cache(maxsize=1, typed=True)
def _get_draft_version_fallback(
        strategy: str,
        sphinx_config: SphinxConfig,
) -> str:
    """Generate a fallback version string for towncrier draft."""
    known_strategies = {'draft', 'sphinx-version', 'sphinx-release'}
    if strategy not in known_strategies:
        raise ValueError(
            'Expected "stragegy" to be '
            f'one of {known_strategies!r} but got {strategy!r}',
        )

    if 'sphinx' in strategy:
        return (
            sphinx_config.release
            if 'release' in strategy
            else sphinx_config.version
        )

    return '[UNRELEASED DRAFT]'


def _nodes_from_rst(
        state: statemachine.State,
        rst_source: str,
) -> List[nodes.Node]:
    """Turn an RST string into a list of nodes.

    These nodes can be used in the document.
    """
    node = nodes.Element()
    node.document = state.document
    nested_parse_with_titles(
        state=state,
        content=statemachine.ViewList(
            statemachine.string2lines(rst_source),
            source='[towncrier-fragments]',
        ),
        node=node,
    )
    return node.children


class TowncrierDraftEntriesDirective(SphinxDirective):
    """Definition of the ``towncrier-draft-entries`` directive."""

    has_content = True  # default: False

    def run(self) -> List[nodes.Node]:  # noqa: WPS210
        """Generate a node tree in place of the directive."""
        target_version = self.content[:1][0] if self.content[:1] else None
        if self.content[1:]:  # inner content present
            raise self.error(
                f'Error in "{self.name!s}" directive: '
                'only one argument permitted.',
            )

        config = self.env.config
        autoversion_mode = config.towncrier_draft_autoversion_mode
        include_empty = config.towncrier_draft_include_empty

        towncrier_fragment_paths = _lookup_towncrier_fragments(
            working_dir=config.towncrier_draft_working_directory,
            config_path=config.towncrier_draft_config_path,
        )
        for path in towncrier_fragment_paths:
            # make sphinx discard doctree cache on file changes
            self.env.note_dependency(str(path))

        try:
            self.env.towncrier_fragment_paths |= (  # type: ignore
                towncrier_fragment_paths
            )
        except AttributeError:
            # If the attribute hasn't existed, initialize it instead of
            # updating
            self.env.towncrier_fragment_paths = (  # type: ignore
                towncrier_fragment_paths
            )

        try:
            self.env.towncrier_fragment_docs |= {  # type: ignore
                self.env.docname,
            }
        except AttributeError:
            # If the attribute hasn't existed, initialize it instead of
            # updating
            self.env.towncrier_fragment_docs = {  # type: ignore
                self.env.docname,
            }

        try:
            draft_changes = _get_changelog_draft_entries(
                target_version or
                _get_draft_version_fallback(autoversion_mode, config),
                allow_empty=include_empty,
                working_dir=config.towncrier_draft_working_directory,
                config_path=config.towncrier_draft_config_path,
            )
        except subprocess.CalledProcessError as proc_exc:
            raise self.error(proc_exc)
        except LookupError:
            return []

        return _nodes_from_rst(state=self.state, rst_source=draft_changes)


class TowncrierDraftEntriesEnvironmentCollector(EnvironmentCollector):
    r"""Environment collector for ``TowncrierDraftEntriesDirective``.

    When :py:class:`~TowncrierDraftEntriesDirective` is used in a
    document, it depends on some dynamically generated change fragments.
    After the first render, the doctree nodes are put in cache and are
    reused from there. There's a way to make Sphinx aware of the
    directive dependencies by calling :py:meth:`~BuildEnvironment.\
    note_dependency` but this will only work for fragments that have
    existed at the time of that first directive invocation.

    In order to track newly appearing change fragment dependencies,
    we need to do so at the time of Sphinx identifying what documents
    require rebuilding. There's :std:event:`env-get-outdated` that
    allows to extend this list of planned rebuilds and we could use it
    by assigning a document-to-fragments map from within the directive
    and reading it in the event handler later (since env contents are
    preserved in cache). But this approach does not take into account
    cleanups and parallel runs of Sphinx. In order to make it truly
    parallelism-compatible, we need to define how to merge our custom
    cache attribute collected within multiple Sphinx subprocesses into
    one object and that's where :py:class:`~EnvironmentCollector` comes
    into play.

    Refs:
    * https://github.com/sphinx-doc/sphinx/issues/8040#issuecomment-671587308
    * https://github.com/sphinx-contrib/sphinxcontrib-towncrier/issues/1
    """

    def clear_doc(
            self,
            app: Sphinx,
            env: BuildEnvironment,
            docname: str,
    ) -> None:
        """Clean up env metadata related to the removed document.

        This is a handler for :std:event:`env-purge-doc`.
        """
        with suppress_exceptions(AttributeError, KeyError):
            env.towncrier_fragment_docs.remove(docname)  # type: ignore

    def merge_other(
            self,
            app: Sphinx,
            env: BuildEnvironment,
            docnames: Set[str],
            other: BuildEnvironment,
    ) -> None:
        """Merge doc-to-fragments from another proc into this env.

        This is a handler for :std:event:`env-merge-info`.
        """
        try:
            other_fragment_docs: Set[str] = (
                other.towncrier_fragment_docs  # type: ignore
            )
        except AttributeError:
            # If the other process env doesn't have documents using
            # `TowncrierDraftEntriesDirective`, there's nothing to merge
            return

        if not hasattr(env, 'towncrier_fragment_docs'):  # noqa: WPS421
            # If the other process env doesn't have documents using
            # `TowncrierDraftEntriesDirective`, initialize the structure
            # at least
            env.towncrier_fragment_docs = set()  # type: ignore

        if not hasattr(env, 'towncrier_fragment_paths'):  # noqa: WPS421
            env.towncrier_fragment_paths = set()  # type: ignore

        # Since Sphinx does not pull the same document into multiple
        # processes, we don't care about the same dict key appearing
        # in different envs with different sets of the deps
        env.towncrier_fragment_docs.update(  # type: ignore
            other_fragment_docs,
        )
        env.towncrier_fragment_paths.update(  # type: ignore
            other.towncrier_fragment_paths,  # type: ignore
        )

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """React to :std:event:`doctree-read` with no-op."""

    # pylint: disable=too-many-arguments
    def get_outdated_docs(  # noqa: WPS211
            self,
            app: Sphinx,
            env: BuildEnvironment,
            added: Set[str],
            changed: Set[str],
            removed: Set[str],
    ) -> List[str]:
        """Mark docs with changed fragment deps for rebuild.

        This is a handler for :std:event:`env-get-outdated`.
        """
        towncrier_fragment_paths = _lookup_towncrier_fragments(
            working_dir=env.config.towncrier_draft_working_directory,
            config_path=env.config.towncrier_draft_config_path,
        )

        fragments_changed = False
        with suppress_exceptions(AttributeError):
            fragments_changed = bool(
                towncrier_fragment_paths
                ^ env.towncrier_fragment_paths,  # type: ignore
            )

        return (
            list(env.towncrier_fragment_docs - changed)  # type: ignore
            if fragments_changed
            else []
        )


def setup(app: Sphinx) -> Dict[str, Union[bool, str]]:
    """Initialize the extension."""
    rebuild_trigger = 'html'  # rebuild full html on settings change
    app.add_config_value(
        'towncrier_draft_config_path',
        default=None,
        rebuild=rebuild_trigger,
    )
    app.add_config_value(
        'towncrier_draft_autoversion_mode',
        default='scm-draft',
        rebuild=rebuild_trigger,
    )
    app.add_config_value(
        'towncrier_draft_include_empty',
        default=True,
        rebuild=rebuild_trigger,
    )
    app.add_config_value(
        'towncrier_draft_working_directory',
        default=None,
        rebuild=rebuild_trigger,
    )
    app.add_directive(
        'towncrier-draft-entries',
        TowncrierDraftEntriesDirective,
    )

    # Register an environment collector to merge data gathered by the
    # directive in parallel builds
    app.add_env_collector(TowncrierDraftEntriesEnvironmentCollector)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        'version': __version__,
    }
