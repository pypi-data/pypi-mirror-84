"""Mercurial extension for committing clean Jupyter notebooks.

Development Notes:

Tags vs Bookmarks: At several points we need to mark changesets.  Tags
  seem like the correct thing to do, but one cannot tag the null
  revision.  This means we must go through some contortions to get our
  code to work on an empty repo.  Instead, we use bookmarks.  The
  potential problem with bookmarks is that they are like branches - if
  you make commits on top, the bookmark will advance.  This can be
  disabled by making sure the bookmarks are inactive.  Since the null
  revision can be bookmarked, this simplifies our code.

API vs hglib: This code contains two paths of execution.  One use the
  Mercurial API and the other uses the hglib module.

  Mercurial API:
    Advantages:
      * Faster (not much though 12s instead of 10s for test suite)
      * More flexible (full access to internals)
    Disadvantages:
      * Not officially supported.  If the package is released
        publicly, then it must be tested with each major version.
      * Sometimes overly complicated.
      * Definitely requires extension to be GPLv2+.

  hglib:
    Advantages:
      * API claimed to be stable.  Hopefully this means we don't need
        to test against every version.
      * Released under MIT license.  In principle this gives more
        flexibility, but in practice it might not help much since one
        needs to use a portion of the Mercurial API to define the
        extension anyway.
      * Quite simple interface.
    Disadvantages:
      * Requires an extra install.  (Not a bit deal - it pip installs
        quite nicely.)
      * Slower (not much though 12s instead of 10s for test suite)
      * Cannot be used to define extensions on its own.
"""
from contextlib import contextmanager
import functools
import inspect
import operator
import os
import shlex
import subprocess
import sys

import hglib

from mercurial.dispatch import dispatch, request
from mercurial import commands, hook, registrar, cmdutil

from mercurial.i18n import _    # International support

cmdtable = {}

try:
    command = registrar.command(cmdtable)
except AttributeError:
    command = cmdutil.command(cmdtable)


testedwith = '5.2.2'


######################################################################
# Helpers
_COMMANDS = []
_AUTOCOMMIT_MESSAGE = "...: Automatic commit with .ipynb output"

API = False


class Status(object):
    modified = []
    added = []
    removed = []
    deleted = []
    unknown = []
    ignored = []
    clean = []
    
    def __repr__(self):
        return "Status({})".format(
            ','.join([
                "{}={}".format(_k, repr(getattr(self, _k)))
                for _k in dir(self)
                if not _k.startswith('_')]))


def cleandoc(doc):
    """Remove 4 spaces from start of doc. The main point is to remove
    one level of indentation since we use a class here.
    """
    lines = inspect.cleandoc(doc).splitlines()
    for _n, _line in enumerate(lines):
        if _n == 0:
            continue
        lines[_n] = "    {}".format(_line)
    return "\n".join(lines)


class NBCleanState(object):
    """Class to encapsulate the state needed by the commands.

    The initial goal here is to provide a simple way to do the
    following:

    * Write functions using the mercurial command-line syntax. This is
      done by using mercurial.dispatch, and shlex.strip to convert
      commands into a simple format.
    * Suppress output in an easy way.

    """
    def __init__(self, ui, repo, client=None):
        self.ui = ui
        self.repo = repo
        self.client = client

        self.devnull = open(os.devnull, 'w')

        # The following tags/branch names are used:
        _tags = [
            'checkpoint',  # This is a checkpoint of the initial
                           # working copy with all output etc.  After
                           # any operation this state of the working
                           # copy should be restored.
            'parent',  # This points to the revision that is/should be
                       # the parent of the working copy.  If commits
                       # are made, it will be updated.
            'new',  # If a new commit is required for the checkpoint,
                    # then this will refer to it.  It should
                    # ultimately be striped.
        ]
        _prefix = '_nbclean'

        self.tags = dict((_t, '_'.join([_prefix, _t])) for _t in _tags)

    def __del__(self):
        self.devnull.close()

    def dispatch(self, cmd, fout=None, ferr=None):
        """Wrapper to run a command and deal with output."""
        # Note: There are two ways to interact with mercurial.  The most
        # stable is with the command lined interface which can be accesed
        # using dispatch(requst(commandline)) as mentioned here:
        # http://stackoverflow.com/a/8972531/1088938
        #
        # Here are some notes about these:
        #
        # request(args, ui=None, repo=None, fin=None, fout=None, ferr=None)
        # dispatch(req)
        #
        # Dispatch returns:
        # -1: Abort was raised or ParseError.
        if API:
            if ferr is False:
                ferr = self.devnull
            if fout is False:
                fout = self.devnull

            if isinstance(cmd, str):
                cmd = shlex.split(cmd)

            self.cmd = cmd
            self.req = request(cmd, fout=fout, ferr=ferr)
            self.result = dispatch(self.req)

        else:
            from hglib.util import b, BytesIO

            out, err = BytesIO(), BytesIO()
            outchannels = {b('o'): out.write, b('e'): err.write}

            inchannels = {}
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            cmd = list(map(b, cmd))
            self.result = self.client.runcommand(
                cmd, inchannels, outchannels)
            if fout is None:
                self.ui.status(out.getvalue())
            if ferr is None:
                self.ui.warn(err.getvalue())

        # result is an errorcode.  We negate it to return a boolean
        # indicating if the command succeded
        return not self.result

    ######################################################################
    # Internal Commands
    #
    # These are shortcuts for the commands we use.  They are not
    # exposed to the user.  The default values are different from the
    # usual versions of the commands so that the main part of our code
    # is cleaner.

    def msg(self, msg, err=False):
        if API:
            msg = _(msg)        # Internationalization
        msg = msg + "\n"

        if err:
            self.ui.warn(msg.encode())
        else:
            self.ui.status(msg.encode())

    def isquiet(self):
        """Return True if the user has specified the global -q flag."""
        return self.config('quiet', section='ui')

    def status(self, clean=False):
        if API:
            status = self.repo.status(clean=clean)
        else:
            status = Status()
            res = self.client.status(added=True, modified=True, clean=True)
            status.added = [_f for _s, _f in res if _s == b'A']
            status.clean = [_f for _s, _f in res if _s == b'C']
            status.modified = [_f for _s, _f in res if _s == b'M']
        return status

    def isclean(self):
        """Return True if the repository is clean.

        Replaces the shell command::

            hg summary | grep -q 'commit: (clean)'
        """
        if API:
            ctx = self.repo[None]
            subs = [s for s in ctx.substate if ctx.sub(s).dirty()]
            status = self.repo.status()
            return not (status.modified or status.added or status.removed
                        or subs or self.repo.dirstate.copies())
        else:
            return self.client.summary()[b'commit']

    def setparent(self, parent, ferr=None):
        """Set the parent node without changing the working copy.

        This is something like calling update followed by revert.
        """""
        self.dispatch('debugsetparents "{}"'.format(parent), ferr=ferr)
        self.dispatch('debugrebuilddirstate', ferr=ferr)

    def bookmark(self, name, inactive=True, delete=False):
        """We use inactive bookmarks by default so they act like tags
        and do not advance.
        """
        if API:
            opts = []
            if delete:
                opts.append('--delete')
            elif inactive:
                opts.append('-i')
            self.dispatch('bookmarks {} {}'.format(' '.join(opts), name))
        else:
            if delete:
                inactive = False
            self.client.bookmark(name.encode(), inactive=inactive, delete=delete)

    def bookmarks(self):
        """Return the set of bookmark names"""
        if API:
            raise NotImplementedError
        else:
            return [_b[0] for _b in self.client.bookmarks()[0]]

    def strip(self, name, nobackup=True, ferr=False):
        """Force strip a changeset without a backup and suppressing
        the error messages."""
        opts = []
        if nobackup:
            opts.append('--no-backup')
        self.dispatch('strip {} {}'.format(name, ' '.join(opts)), ferr=False)

    def revert(self, rev, files=(), all=True, nobackup=True):
        """Revert all files to the specified revision without backup
        files (.orig) and without any messages."""
        if API:
            opts = ['-q']
            if all:
                opts.append('--all')
            if nobackup:
                opts.append('-C')
            return self.dispatch('revert {} -r {} {}'.format(
                ' '.join(opts), rev, ' '.join(files)))
        else:
            files = [_f.encode() for _f in files]
            return not self.client.revert(
                files, rev=rev.encode(), all=all, nobackup=nobackup)

    def identify(self):
        """Return the revision number of the parent node."""
        if API:
            raise NotImplementedError
        else:
            return self.client.identify(id=True)[:12].decode()

    def update(self, rev, clean=True, quiet=True):
        """Update (clean by default) quietly"""
        if True or API:
            opts = ['-q'] if quiet else []
            if clean:
                opts.append('-C')
            return self.dispatch('update {} {}'
                                 .format(' '.join(opts), rev),
                                 ferr=False)
        else:
            try:
                res = self.client.update(rev, clean=clean)
                if not quiet:
                    self.msg(", ".join("{} files updated",
                                       "{} files merged",
                                       "{} files removed",
                                       "{} files unresolved").format(*res))
                result = True
            except hglib.error.CommandError:
                result = False
            return result

    def branch(self, name):
        """Create branch"""
        if not self.isquiet():
            self.msg("marked working directory as branch {}".format(name))

        if API:
            with self.suppress_output:
                return self.dispatch('branch -q "{}"'.format(name))
        else:
            self.client.branch(name.encode())

    def checkpoint(self, force=False):
        """Create a checkpoint of the current working copy.

        See also:
            hg nbrestore
        """
        # Preconditions
        #   * None
        # Postconditions
        #   EITHER
        #     * remove tags and bookmarks (if they were present)
        #     * exit(-1)
        #   OR
        #     * The current working copy is stored in a node with
        #       bookmark 'checkpoint'
        #     * If a new node was created to do this, it has tag 'new'

        # Remove any old bookmarks first.
        bookmarks = self.bookmarks()
        for bookmark in [self.tags['parent'],
                         self.tags['checkpoint']]:
            if bookmark in bookmarks:
                if force:
                    self.bookmark(bookmark, delete=True)
                else:
                    self.msg(
                        "Aborting... bookmark {} exists! ".format(bookmark)
                        + "(run 'hg nbclean --force' to force cleaning)",
                        err=True)
                    sys.exit(-1)

        self.bookmark(self.tags['parent'])
        try:
            if API:
                if self.dispatch('commit -qm "CHK: auto checkpoint"'):
                    self.dispatch('tag -fl {}'.format(self.tags['new']))
            else:
                try:
                    self.client.commit(message=b"CHK: auto checkpoint")
                except hglib.error.CommandError as err:
                    if err.ret != 1:
                        self.msg(
                            "\n".join([
                                "Aborting... could not create checkpoint commmit!",
                                err.out.rstrip().decode(),
                                err.err.rstrip().decode()]),
                            err=True)
                        sys.exit(-1)
                else:
                    try:
                        self.client.tag(names=self.tags['new'].encode(),
                                        local=True, force=True)
                    except hglib.error.CommandError:
                        pass

            self.bookmark(self.tags['checkpoint'])
        except:
            # Delete any bookmarks on failure
            bookmarks = self.bookmarks()
            for bookmark in [self.tags['parent'],
                             self.tags['checkpoint']]:
                if bookmark in bookmarks:
                    self.bookmark(bookmark, delete=True)
            raise

    @property
    @contextmanager
    def suppress_output(self):
        """Context to suppress output"""
        _q = self.ui.quiet
        self.ui.quiet = True
        yield
        self.ui.quiet = _q

    def quiet_commit(self, message):
        """Helper function that does a quiet commit without hooks.

        Returns True if a commit was made.
        """
        # For some reason, global options like quiet=True
        # cannot be passed through the commands.commit
        # interface.  We could call self.dispatch('_commit') as an
        # alias here but not self.dispatch('commit') since the latter
        # might call hooks.  We do this so we do not need an alias.
        if API:
            with self.suppress_output:
                res = commands.commit(self.ui, self.repo,
                                      message=message)
        else:
            try:
                res = self.client.commit(message=message)
            except hglib.error.CommandError:
                res = False

        return bool(res)

    def run_with_hooks(self, cmd, *pats, **opts):
        """Runs the specified command with the pre and post hooks."""
        fullargs = sys.argv[1:]   # This is a guess...
        args = " ".join(fullargs)

        hook.hook(self.ui, self.repo, "pre-{}".format(cmd),
                  True, args=args, pats=pats, opts=opts)

        ret = getattr(commands, cmd)(self.ui, self.repo, *pats, **opts)

        # run post-hook, passing command result
        hook.hook(self.ui, self.repo, "post-{}".format(cmd),
                  False, args=args, result=ret, pats=pats, opts=opts)
        return ret

    def automerge(self, src, dest, checkpoint):
        """Merges revision src onto dest keeping working copy exactly
        as in checkpoint.

        Equivalent to (modulo message suppression etc.)::

            hg update checkpoint
            hg update dest
            hg merge src
            hg revert --all checkpoint
        """
        # Makes sure any files are added then removed properly
        self.update(checkpoint)
        self.update(dest)
        if API:
            self.dispatch('merge -q {} --tool :other'.format(src), ferr=False)
        else:
            self.client.merge(rev=src, tool=":other")

        # We do this twice because of bug 5052:
        # https://bz.mercurial-scm.org/show_bug.cgi?id=5052
        self.revert(checkpoint)
        self.revert(checkpoint)

    def config(self, name, default='', section='nbclean'):
        """Return the value of nbclean.name from the configuration
        file."""
        if API:
            return self.ui.config(section, name, default=default)
        else:
            try:
                config = self.client.config(b'nbclean')
            except hglib.error.CommandError:
                config = []

            res = dict((_key.decode(), _value.decode())
                       for _section, _key, _value
                       in config)
            return res.get(name, default)

    @contextmanager
    def clean_restore(self, force=False, **kw):
        # Preconditions
        #   * Nothing
        # Postconditions
        #   EITHER
        #     * remove tags and bookmarks (if they were present)
        #     * raise Abort
        #   OR
        #     * Current state checkpointed
        #     * Specified output cleaned from notebooks.
        self.checkpoint(force=force)
        try:
            yield self.clean_output(force=force, **kw)
        finally:
            self.nbrestore()

    def clean_output(self, clean_all=False, force=False):
        """Clean output from all added or modified .ipynb notebooks.

        See also:
           hg nbrestore
        """
        # Preconditions
        #   * Nothing - this is an entrypoint.
        # Postconditions
        #   EITHER
        #     * remove tags and bookmarks (if they were present)
        #     * raise Abort
        #   OR
        #     * Current self checkpointed in revision with tag 'checkpoint'
        #     * Potentially new checkpoint commit with tag 'checkpoint'
        #     * All A or M .ipynb have output stripped
        #     * Desired parent node has tag 'parent'.  (This might
        #       be the original parent, or might be a new commit.)
        self.msg("cleaning output")
        self.update(self.tags['parent'])
        self.revert(self.tags['checkpoint'])

        # hg status -man0 | xargs -0 nbstripout

        status = self.status(clean=clean_all)
        filenames = status.modified + status.added
        if clean_all:
            filenames.extend(status.clean)
        notebooks = [_f.decode() for _f in filenames if _f.endswith(b'.ipynb')]
        if notebooks:
            self.msg('cleaning {}'.format(', '.join(notebooks)))
            subprocess.run(args=['nbstripout'] + notebooks, shell=False)
        return True

    def commit_output(self, branch):
        """Commit the output to the specified branch."""
        if not branch:
            branch = self.config('output_branch')
        if branch:
            self.bookmark(self.tags['parent'])
            self.revert(self.tags['checkpoint'])
            if self.isclean():
                self.msg("no output to commit")
            else:
                if self.update(branch):
                    # Before merging, check if there are differences!
                    self.revert(self.tags['checkpoint'])
                    if not self.isclean():
                        # Only merge if there are changes!
                        self.automerge(src=self.tags['parent'],
                                       dest=branch,
                                       checkpoint=self.tags['checkpoint'])
                        self.msg("automatic commit of output")
                        self.quiet_commit(_AUTOCOMMIT_MESSAGE)
                else:
                    # No auto_output branch exists yet.
                    self.setparent('c_parent', ferr=False)
                    self.branch(branch)
                    self.msg("automatic commit of output")
                    self.quiet_commit(_AUTOCOMMIT_MESSAGE)
        else:
            self.bookmark(self.tags['parent'])
            self.revert(self.tags['checkpoint'])
            self.revert(self.tags['checkpoint'])

            if self.quiet_commit(_AUTOCOMMIT_MESSAGE):
                self.msg("automatic commit of output")
            else:
                self.msg("no output to commit")

    def nbrestore(self):
        """Restore a repository from a checkpoint.

        See also:
           hg checkpoint
        """
        # Preconditions
        #   * Working copy stored in a node with tag 'checkpoint'
        #   * This might be a new node with tag 'new'
        # Postconditions
        #   * Working copy restored to state in 'checkpoint'
        #   * If there was a node with tag 'new', it is stripped
        #   * Both tags 'checkpoint' and 'new' are removed
        self.msg("restoring output")
        self.update(self.tags['parent'])
        self.revert(self.tags['checkpoint'])
        self.strip(self.tags['new'])
        self.bookmark(self.tags['parent'], delete=True)
        self.bookmark(self.tags['checkpoint'], delete=True)
                

######################################################################
# Commands
#
# These are the new commands provided to mercurial
def _cmd(opts=[], synopsis=_(''), **kw):
    """Decorator like command that uses the function name and ensures a state
    is created in the ui with state.ui, state.repo, and state.client.

    These are passed to the various commands as `state`, which is an instance
    of NBCleanState.
    """
    def wrap(f):
        @functools.wraps(f)
        def wrapper(ui, repo, *pats, **opts):
            if not hasattr(ui, '_nbclean_state'):
                args = dict(ui=ui, repo=repo)
                if not API:
                    args['client'] = hglib.open(repo.pathto(b''))
                ui._nbclean_state = NBCleanState(**args)
            return f(ui._nbclean_state, *pats, **opts)

        name = f.__name__.encode()
        _COMMANDS.append((name, opts, synopsis, kw, wrapper))
        wrapper.__doc__ = cleandoc(f.__doc__)
        return wrapper
    return wrap


@_cmd()
def nbrestore(state):
    """Restore a repository from a checkpoint.

    See also:
       hg checkpoint
    """
    return state.nbrestore()


@_cmd(opts=[(b'', b'clean-all', False,
             _('clean all managed .ipynb files')),
            (b'f', b'force', False,
             _('force removal of managed bookmarks etc.'))])
def nbclean(state, clean_all=False, force=False):
    """Clean output from all added or modified .ipynb notebooks.

    See also:
       hg nbrestore
    """
    # Preconditions
    #   * Nothing - this is an entrypoint.
    # Postconditions
    #   EITHER
    #     * remove tags and bookmarks (if they were present)
    #     * raise Abort
    #   OR
    #     * Current state checkpointed in revision with tag 'checkpoint'
    #     * Potentially new checkpoint commit with tag 'checkpoint'
    #     * All A or M .ipynb have output stripped
    #     * Desired parent node has tag 'parent'.  (This might
    #       be the original parent, or might be a new commit.)
    state.checkpoint(force=force)
    return state.clean_output(clean_all=clean_all, force=force)



# Get standard commit options from commands.table
@_cmd(opts=commands.table[b'commit|ci'][1]
      + [(b'', b'clean-all', False,
          _('clean all managed .ipynb files')),
         (b'b', b'branch', b'',
          _('commit output to this branch (create if needed)'))],
      synopsis=commands.table[b'commit|ci'][2],
      inferrepo=True)
def ccommit(state, *pats, **opts):
    """Clean cleaned notebooks.

    This will clean all changed and added .ipynb notebooks, then
    commit them, and finally restore the output.

    The notebooks with output will also be committed to a child
    node with a message "...: Automatic commit with .ipynb output"
    that can later be stripped.  If the `--branch` option is used,
    these automatic commits will be merged into the named branch.
    """
    branch = opts.pop('branch')
    clean_all = opts.pop('clean_all')
    with state.clean_restore(clean_all=clean_all):
        isclean = state.isclean()
        if isclean:
            state.msg("nothing changed")
        else:
            isclean = (state.run_with_hooks('commit', *pats, **opts) is None)

        if isclean:
            state.commit_output(branch)


@_cmd(opts=commands.table[b'update|up|checkout|co'][1],
      synopsis=commands.table[b'update|up|checkout|co'][2])
def cupdate(state, *pats, **opts):
    """Like hg update but restore cleaned notebooks with their output.

    This the equivalent to `hg update` followed by `hg revert
    --all` to the most recent auto-committed child with output.
    """
    state.run_with_hooks('update', *pats, **opts)
    rev = state.identify()
    auto_commits = sorted([
        _r for _r in state.client.log('children(.)')
        if _r[-2].decode() == _AUTOCOMMIT_MESSAGE
    ], key=operator.attrgetter('date'))
    if not auto_commits:
        return
    state.msg("updating notebook outputs")
    auto_node = auto_commits[-1].node.decode()

    # Do this to get a nice message
    state.update(rev=auto_node, clean=opts['clean'], quiet=False)
    state.update(rev=rev, clean=opts['clean'], quiet=True)
    state.revert(rev=auto_node, all=True, nobackup=True)


@_cmd(opts=[
    (b'', b'clean-all', False,
     _('clean all managed .ipynb files')),
    (b'b', b'branch', b'',
     _('commit output to this branch (create if needed)'))])
def crecord(state, *pats, **opts):
    """Record cleaned notebooks.

    See also:
        hg record
        hg ccommit
    """
    # branch = opts.pop('branch')
    clean_all = opts.pop('clean_all')
    with state.clean_restore(clean_all=clean_all):
        isclean = state.isclean()
        if isclean:
            state.msg("nothing changed")
        else:
            state.dispatch('record')


# Get standard status options from commands.table
@_cmd(opts=commands.table[b'status|st'][1] +
      [(b'', b'clean-all', False,
        _('clean all managed .ipynb files'))],
      synopsis=commands.table[b'status|st'][2])
def cstatus(state, *pats, **opts):
    """Status of cleaned notebooks.

    See also:
        hg status
    """
    clean_all = opts.pop('clean_all')
    with state.clean_restore(clean_all=clean_all):
        state.run_with_hooks('status', *pats, **opts)


# Get standard diff options from commands.table
@_cmd(opts=commands.table[b'diff'][1] +
      [(b'', b'clean-all', False,
        _('clean all managed .ipynb files'))],
      synopsis=commands.table[b'diff'][2])
def cdiff(state, *pats, **opts):
    """Diff of cleaned notebooks.

    See also:
        hg diff
    """
    clean_all = opts.pop('clean_all')
    with state.clean_restore(clean_all=clean_all):
        state.run_with_hooks('diff', *pats, **opts)


# Register commands with mercurial
for name, opts, synopsis, kw, function in _COMMANDS:
    command(name, opts, synopsis, **kw)(function)
