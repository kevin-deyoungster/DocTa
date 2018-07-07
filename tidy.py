import subprocess


def tidy_document(document):
    process = subprocess.Popen(
        ['modules/tidy.exe', '-config', 'tidy-config.txt', '-q'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf8')
    out, err = process.communicate(document)
    return out, err
