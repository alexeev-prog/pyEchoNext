#!/usr/bin/env python3
import os
import re


class GitVersion:
    def __init__(self):
        self._default_version = "0.0.1.0a"
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

    @property
    def tag(self):
        stream = os.popen("git describe --match v[0-9]* --abbrev=0 --tags")
        return stream.read().strip()

    @property
    def version(self):
        version = f"{self.tag[1:]}.{self.build}"

        if version == ".":
            return self._default_version

        return version

    @property
    def default_branch(self):
        stream = os.popen("git config --get init.defaultBranch")
        result = stream.read().strip()

        if not result:
            result = "main"

        return result

    @property
    def build(self):
        stream = os.popen("git rev-list {}.. --count".format(self.tag))
        return stream.read().strip()

    @property
    def branch(self):
        stream = os.popen("git branch --show-current")
        return stream.read().strip()

    @property
    def full(self):
        return f"{self.version}-{self.branch}"

    @property
    def standard(self):
        standard = f"{self.version}-{self.branch}"
        if self.branch == self.default_branch or re.match("release/.*", self.branch):
            standard = f"{self.version}"
        return standard

    @property
    def commit(self):
        stream = os.popen("git rev-parse HEAD")
        return stream.read().strip()

    @property
    def commit_hash(self):
        stream = os.popen("git rev-parse --short HEAD")
        return stream.read().strip()

    def __str__(self):
        return f"""
Tag: {self.tag}
Version: {self.version}
Full: {self.full}
Branch: {self.branch}
Build: {self.build}
Standard: {self.standard}
Commit: {self.commit}

Current: {self.full} {self.commit_hash}
"""


if __name__ == "__main__":
    git_version = GitVersion()
    print(git_version)
