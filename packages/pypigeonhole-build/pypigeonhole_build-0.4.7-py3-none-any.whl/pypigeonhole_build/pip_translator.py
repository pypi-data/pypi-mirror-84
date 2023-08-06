import sys

from pypigeonhole_build.dependency import INSTALL, DEV


def get_install_required(libs):
    return _find_dep_for_scope(libs, INSTALL)


def get_test_required(libs):
    return _find_dep_for_scope(libs, DEV)


def _find_dep_for_scope(libs, scope):
    ret = []
    for lib in libs:
        if lib.name.lower() == 'python':
            continue
        if lib.scope == scope:
            # https://stackoverflow.com/a/54794506/7898913
            if lib.url:
                ret.append(f'{lib.name} @ {lib.url}')
            else:
                ret.append(f'{lib.name}{lib.version}')

    print(f'{scope} dependencies: {ret}', file=sys.stderr)
    return ret


def get_python_requires(libs):
    for lib in libs:
        if lib.name.lower() == 'python':
            print('use python version: ' + lib.version, file=sys.stderr)
            return lib.version

    return '>=3.5'


def gen_req_txt(libs, target_file):
    with open(target_file, 'w') as f:
        for lib in libs:
            if lib.name.lower() != 'python' and lib.scope != DEV:
                if lib.url:
                    f.write(lib.url)
                elif lib.version:
                    f.write(f'{lib.name}=={lib.version}\n')
                else:
                    f.write(f'{lib.name}\n')
