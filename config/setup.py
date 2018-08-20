import sys
import shutil
import importlib
import logging
import platform


def initiate(data):
    """
    Checks Dependencies & Do Housekeeping
    """
    _clear_job_dir(data.JOBS_FOLDER, data.PERSIST_JOBS)
    proceed = (
        _dependencies_exist_in_path(data.PATH_DEPENDENCIES)
        and _python_packages_installed(data.PYTHON_PACKAGES)
        and _ensure_python_upwards(data.PYTHON_VERSION_MIN)
    )
    _disable_flask_logging()
    if not proceed:
        exit()


def _clear_job_dir(job_dir, should_persist):
    """
    Deletes job directory if specified
    """
    if not should_persist:
        shutil.rmtree(job_dir, ignore_errors=True)


def _ensure_python_upwards(python_version):
    current_python_version = ".".join([str(i) for i in sys.version_info[:2]])
    if current_python_version < python_version:
        print(
            f"[Config]: Python Version must be {python_version}. Detected Python {current_python_version}"
        )
        return False
    else:
        return True


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
    if _system_os_is("linux"):  # For Linux we also need to check for 'tidy'
        dependencies.append("tidy")
    for dependency in dependencies:
        in_path = _is_program_in_PATH(dependency)
        if not in_path:
            print(f"[Config]: Dependency '{dependency}' not found")
            missing_dependencies.append(dependency)

    return len(missing_dependencies) < 1


def _is_program_in_PATH(program):
    return shutil.which(program) != None


def _disable_flask_logging():
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)


def _system_os_is(os):
    return platform.system().lower() == os
