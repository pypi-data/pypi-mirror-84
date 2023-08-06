import json
import sys
from contextlib import nullcontext
from os import path

from anytree import AnyNode, PreOrderIter
from yaspin import yaspin

from license_sh.helpers import get_initiated_text
from license_sh.project_identifier import ProjectType
from license_sh.runners.abstract_runner import AbstractRunner
from license_sh.runners.runners_shared import fetch_npm_licenses


def flatten_package_lock_dependencies(package_lock_dependencies):
    """
    Flattens package.lock dependencies
    :param package_lock_dependencies:
    :return: tuple(flat_array, dep_mapping)
     WHERE
     array flat_array is a flat array of all dependencies
     dict dep_mapping is a tree representing nested dependencies
    """
    # get the root dependencies
    root_deps = [
        (name, dep.get("version")) for name, dep in package_lock_dependencies.items()
    ]

    for dep in package_lock_dependencies.values():
        version, requires, dependencies = [
            dep.get(k, None) for k in ("version", "requires", "dependencies")
        ]
        if dependencies:
            deps = flatten_package_lock_dependencies(dependencies)
            root_deps += deps

    return set(root_deps)


def add_nested_dependencies(dependency, package_lock_tree, parent):
    for name, version_request in dependency.get("requires", {}).items():
        node = AnyNode(
            name=name,
            version_request=version_request,
            parent=parent,
            dependencies=dependency.get("dependencies"),
        )

        dep = None
        p = node
        names = []
        while p.parent:
            if dep is None and p.dependencies and p.dependencies.get(name):
                dep = p.dependencies.get(name)
            p = p.parent
            names.append(p.name)

        # check the root
        if dep is None and p.dependencies and p.dependencies.get(name):
            dep = p.dependencies.get(name)

        node.version = dep.get("version")

        names = names[:-1]  # let's forget about top level

        # if I'm not already in a tree
        if name not in names:
            if dep:
                add_nested_dependencies(dep, package_lock_tree, node)


def get_dependency_tree(package_json, package_lock_tree):
    root = AnyNode(
        name=package_json.get("name", "package.json"),
        dependencies=package_lock_tree,
        version=package_json.get("version"),
    )

    # load root dependencies from package.json
    for dep_name in package_json.get("dependencies", {}).keys():
        if dep_name not in package_lock_tree:
            print(
                f"{dep_name} package not found in package-lock.json", file=sys.stderr,
            )
            exit(1)
        dependency = package_lock_tree[dep_name]
        version = dependency.get("version")
        parent = AnyNode(
            name=dep_name,
            version=version,
            parent=root,
            dependencies=dependency.get("dependencies"),
        )
        add_nested_dependencies(dependency, package_lock_tree, parent=parent)

    return root


class NpmRunner(AbstractRunner):
    """
    This class checks for dependencies in NPM projects and fetches license info
    for each of the packages (including transitive dependencies)
    """

    def __init__(self, directory: str, silent: bool, debug: bool):
        self.directory = directory
        self.silent = silent
        self.package_json_path = path.join(directory, "package.json")
        self.package_lock_path = path.join(directory, "package-lock.json")
        self.debug = debug

    def check(self):
        with open(self.package_json_path) as package_json_file:
            package_json = json.load(package_json_file)
            project_name = package_json.get("name", "package.json")

        with open(self.package_lock_path) as package_lock_file:
            package_lock = json.load(package_lock_file)
            all_dependencies = (
                package_lock["dependencies"]
                if "dependencies" in package_lock
                else dict()
            )
        if not self.silent:
            print(get_initiated_text(ProjectType.NPM, project_name, self.directory))

        with yaspin(text="Analysing dependencies ...") if not self.silent else nullcontext():
            dep_tree = get_dependency_tree(package_json, all_dependencies)
            flat_dependencies = flatten_package_lock_dependencies(all_dependencies)

        with yaspin(text="Fetching license info from npm ...") if not self.silent else nullcontext():
            license_map = fetch_npm_licenses(flat_dependencies)

        for node in PreOrderIter(dep_tree):
            delattr(node, "dependencies")
            hasattr(node, "version_request") and delattr(node, "version_request")
            node.license = license_map.get(f"{node.name}@{node.version}", None)

        return dep_tree
