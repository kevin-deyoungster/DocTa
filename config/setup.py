import shutil
import importlib


def initiate(data):
    """
    Checks Dependencies & Do Housekeeping
    """

    _clear_job_dir(data.JOBS_FOLDER, data.PERSIST_JOBS)
    _check_path_dependencies(data.PATH_DEPENDENCIES)
    _check_python_packages_installed(data.PYTHON_PACKAGES)


def _clear_job_dir(job_dir, should_persist):
    """
    Deletes job directory if specified
    """
    if not should_persist:
        shutil.rmtree(job_dir, ignore_errors=True)


def _check_path_dependencies(dependencies):
    """
    Checks whether dependencies are in path
    """
    missing_dependencies = []
    for dependency in dependencies:
        in_path = _is_program_in_PATH(dependency)
        if not in_path:
            print(f"[Config]: Dependency '{dependency}' not found")
            missing_dependencies.append(dependency)

    if len(missing_dependencies) > 0:
        exit()


def _check_python_packages_installed(python_packages):

    missing_python_packages = []

    python_package_bools = [
        True if importlib.find_loader(package) else False for package in python_packages
    ]
    print(python_package_bools)
    for package in python_packages:
        package_found = importlib.find_loader(package)
        if not package_found:
            print(f"[Config]: Python Package '{package.strip()}' not found")
            missing_python_packages.append(package)

    if len(missing_python_packages) > 0:
        exit()


def _is_program_in_PATH(program):
    return shutil.which(program) != None

