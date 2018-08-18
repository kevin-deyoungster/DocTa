import shutil
import importlib


def initiate(data):
    """
    Checks Dependencies & Do Housekeeping
    """
    _clear_job_dir(data.JOBS_FOLDER, data.PERSIST_JOBS)
    proceed = _dependencies_exist_in_path(
        data.PATH_DEPENDENCIES
    ) and _python_packages_installed(data.PYTHON_PACKAGES)

    if not proceed:
        exit()


def _clear_job_dir(job_dir, should_persist):
    """
    Deletes job directory if specified
    """
    if not should_persist:
        shutil.rmtree(job_dir, ignore_errors=True)


def _python_packages_installed(python_packages):
    missing_python_packages = []
    for package in python_packages:
        package_found = importlib.find_loader(package)
        if not package_found:
            print(f"[Config]: Python Package '{package.strip()}' not found")
            missing_python_packages.append(package)

    return len(missing_python_packages) < 1


def _dependencies_exist_in_path(dependencies):
    missing_dependencies = []
    for dependency in dependencies:
        in_path = _is_program_in_PATH(dependency)
        if not in_path:
            print(f"[Config]: Dependency '{dependency}' not found")
            missing_dependencies.append(dependency)

    return len(missing_dependencies) < 1


def _is_program_in_PATH(program):
    return shutil.which(program) != None
