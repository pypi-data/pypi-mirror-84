#!/usr/bin/env python3
import argparse
import os
import sys
import yaml
import glob
import subprocess
import re
from datetime import date

from PyInquirer import prompt

from seckerwiki.install import setup
from seckerwiki.lecture_gen import generate_lecture

# Regex to search for tags in the form of <!-- tags: tag1, tag2, etc -->
# matches the list of tags, relying on string split methods to reduce it into individual tags
TAGS_REGEX = '^(?:<!--\s*tags:\s*)([A-Za-z,\s]+)(?:-->)'


# Terminal Colours
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




def get_tri_from_course(course, courses):
    """
    Given a courses dict, return the trimester of the :param course
    """
    for tri in courses:
        for _course in courses[tri]:
            if course == _course:
                return tri.capitalize()


def get_latest_lecture_num(cfg, course):
    """
    Return the latest lecture number from the filenames in course
    """
    tri = get_tri_from_course(course, cfg['courses'])
    lecture_dir = os.path.join(cfg['wiki-root'], "Uni", tri, course, "Lectures")

    print(lecture_dir)
    files = [f for f in glob.glob(lecture_dir + "**/*.md", recursive=False)]

    # if no files exist, return 0
    if len(files) < 1:
        print("No recent lectures found.")
        return "1"

    last_file = sorted(files)[-1]

    print("Most recent lecture: " + last_file)

    # use regex to match number (get last as most likely to be lecture num if alphabetised)
    last = re.findall(r'\d+', last_file)[-1]

    # suggest the latest lecture num + 1
    suggested = int(last) + 1 if last.isdigit() else "none"

    return str(suggested)


# Lecture command
def lecture(cfg, args):
    # merge all courses from every category into a single list
    courses = [item for key in cfg['courses'].keys() for item in cfg['courses'][key]]

    questions = [
        {
            'type': 'input',
            'name': 'input_file',
            'message': 'Enter path of lecture pdf, or url'
        },
        {
            'type': 'list',
            'name': 'course',
            'message': 'Enter course code',
            'choices': courses
        },
        {
            'type': 'input',
            'name': 'lecture_num',
            'message': 'Enter lecture number',
            'validate': lambda x: x.isdigit(),
            'default': lambda answers: get_latest_lecture_num(cfg, answers['course'])
        },
        {
            'type': 'input',
            'name': 'title',
            'message': 'Enter lecture title',
        }
    ]
    answers = prompt(questions)
    generate_lecture(cfg, answers['input_file'], answers['course'], answers['lecture_num'], title=answers['title'])

# Commit command
def commit(cfg, args):
    # Change working dir to wiki root
    os.chdir(cfg['wiki-root'])

    """
    Commit the files
    args:
    -y : don't confirm
    """

    def convert(line):
        """
        Convert line into a tuple of (root folder, filename)
        """
        line = str(line.decode('utf-8'))
        path = line.split(os.sep)
        root = path[0] if len(path) > 0 else ""
        filename = path[-1]
        return (root, filename)

    # run git diff command
    # if changed more than 3 files, list folders instead
    output = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], stdout=subprocess.PIPE).stdout.splitlines()
    changed = list(map(convert, output))

    if not changed:
        print("No files detected")
        return

    # Make a message using the filenames. If its too long,
    # Set the commit title to the root folders, then the commit description to each of the files changed
    message = " ".join([pair[1] for pair in changed])
    if len(message) > 50:
        message = " ".join(set([pair[0] for pair in changed])) + "\n\n" + "\n".join([pair[1] for pair in changed])

    print("Committing with messsage: \n{0}".format(message))

    confirm = [
        {
            'name': 'confirm',
            'message': 'commit?',
            'type': 'confirm',
            'default': True
        }
    ]

    # Prompt for confirmation
    if not args.y and not prompt(confirm)['confirm']:
        return

    # make the commit
    os.system("git commit -am \"{0}\"".format(message))


def sync(cfg, args):
    """
    git pull and git push
    """
    print("Syncing...")

    # Change working dir to wiki root
    os.chdir(cfg['wiki-root'])

    # Forcefully encrypt the journal
    # print("Encrypting Journal...")
    # encrypt_journal(None)

    os.system("git pull -r && git push")


# Log command
def log(cfg, args):
    # Change working dir to wiki root
    os.chdir(cfg['wiki-root'])

    os.system(
        "git log --graph --pretty=\"%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset\" --abbrev-commit")

def status(cfg, args):
    os.chdir(cfg['wiki-root'])
    os.system("git status")

# Open vscode editor command
def open_editor(cfg, args):
    os.system("{0} {1}".format(cfg['editor-command'], cfg['wiki-root']))


# Build static files command
def build(cfg, args):
    print("Not implemented yet")


# Show TODOs command
def todo(cfg, args):
    # Change working dir to wiki root
    os.chdir(cfg['wiki-root'])
    os.system("grep -r \"TODO\" --include \\*.md {0}".format(cfg['wiki-root']))


def receipt(cfg, args):
    # Change working dir to wiki root
    os.chdir(cfg['wiki-root'])
    options = [
        {
            'type': 'input',
            'message': 'enter product name',
            'name': 'name'
        },
        {
            'type': 'input',
            'message': 'enter date bought',
            'name': 'bought'
        }
    ]

    answers = prompt(options)

    # TODO make a popup here choosing the receipt file


def journal(cfg, args):
    if args.encrypt:
        encrypt_journal(cfg, args)
    elif args.decrypt:
        decrypt_journal(cfg, args)
    else:
        today = date.today().isoformat()
        filename = 'entry-{0}.md'.format(today)
        text = '# Journal Entry -  {0}\n\n - '.format(today)

        path = os.path.join(cfg['wiki-root'], cfg['journal-path'], filename)

        with open(path, 'a') as f:
            f.write(text)
            print("Generated Journal Entry: ", path)


def encrypt_journal(cfg, args):
    journal_dir = os.path.join(cfg['wiki-root'], cfg['journal-path'])

    # check if journal path exists
    if not os.path.isdir(journal_dir):
        print("Journal directory not found: {0}".format(journal_dir))
        return

    print("Encrypting Journal Entries...")
    for root, dirs, files in os.walk(journal_dir):
        for file in files:
            # only encrypt markdown files
            if not file.endswith(".md"):
                print("Skipping: {0}{1}{2}".format(bcolors.OKBLUE, file, bcolors.ENDC))
                continue

            print("Encrypting: {0}{1}{2}".format(bcolors.OKGREEN, file, bcolors.ENDC))
            os.system(
                "gpg -c --armor --batch --passphrase {0} {1}".format(cfg['journal-password'], os.path.join(root, file)))
            # delete the markdown file
            os.remove(os.path.join(root, file))


def decrypt_journal(cfg, args):
    journal_dir = os.path.join(cfg['wiki-root'], cfg['journal-path'])

    # check if journal path exists
    if not os.path.isdir(journal_dir):
        print("Journal directory not found: {0}".format(journal_dir))
        return

    path = os.path.abspath(args.decrypt)

    print("Decrypting Journal Entry: {0}{1}{2}".format(bcolors.OKGREEN, path, bcolors.ENDC), file=sys.stderr)
    os.system("gpg -d --armor --batch --passphrase {0} {1}".format(cfg['journal-password'], path))


def list_tags(cfg, args):
    print(args)

    # Change working dir to wiki root
    os.chdir(cfg['wiki-root'])

    # map of tag => filenames for printing when --print-all arg is supplied
    tag_map = {}

    # list of files that match the supplied tag filter argument
    matching_files = []

    # If no filter tags provided, force printing all tags
    if not args.tags:
        args.print_all = True

    for root, dirs, files in os.walk(cfg['wiki-root']):
        # if root in cfg['excluded-search-dirs']: #TODO
        for filename in files:
            # only search markdown files
            if not filename.endswith(".md"):
                continue
            with open(os.path.join(root, filename), 'r') as f:
                lines = f.readlines(1)
                if len(lines) == 0: # empty file
                    continue

                line = lines[0]

                # Apply regex to the line, continuing if no match found
                match = re.search(TAGS_REGEX, line)
                if not match:
                    continue

                # Split on commas and strip out whitespace
                tags = [x.strip() for x in match.groups()[0].split(',')]

                if args.union:
                    # Add file path to the data structure, grouped by key
                    for tag in tags:
                        # if the key exists, add to the list (creating list if mapping doesn't exist)
                        if tag not in tag_map.keys():
                            tag_map[tag] = []
                        tag_map[tag].append(os.path.join(root, filename))
                else:
                    # if the file has all the tags, add it to the list
                    if all(tag in tags for tag in args.tags):
                        matching_files.append(os.path.join(root, filename))

    if args.union:
        # get matching tags if a filter was provided in arguments
        matching_tags = {key: tag_map[key] for key in args.tags} if args.tags else tag_map

        # print nicely
        for key in matching_tags.keys():
            print("{0}[{1}]{2}:".format(bcolors.OKGREEN, key, bcolors.ENDC))
            # print the whole path. This will make a clickable link in vscode terminal for quick editing
            for value in matching_tags[key]:
                print('    ' + value)
    else:
        print("files matching tags: {0}".format(
            " ".join(["[{0}{1}{2}]".format(bcolors.OKGREEN, x, bcolors.ENDC) for x in args.tags])))
        for filename in matching_files:
            print('    ' + filename)

def links(cfg, args):
    for link in cfg['links']:
        os.system(f"{cfg['browser-command']} {link}")


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Add all the subparsers 
    lecture_parser = subparsers.add_parser('lecture', help='create new lecture slides')
    lecture_parser.add_argument('-b', '--blank', action='store_true', help='Create blank lecture slides.')
    lecture_parser.set_defaults(func=lecture)

    setup_parser = subparsers.add_parser('setup', help='setup wiki CLI')
    setup_parser.set_defaults(func=setup)

    log_parser = subparsers.add_parser('log', help='show git log')
    log_parser.set_defaults(func=log)

    status_parser = subparsers.add_parser('status', help='show git status')
    status_parser.set_defaults(func=status)

    open_parser = subparsers.add_parser('open', help='open editor')
    open_parser.set_defaults(func=open_editor)

    commit_parser = subparsers.add_parser('commit', help='commit wiki')
    commit_parser.add_argument('-y', action='store_true', help='Don\'t ask for confirmation before committing')
    commit_parser.set_defaults(func=commit)

    build_parser = subparsers.add_parser('build', help='generate static html files')
    build_parser.set_defaults(func=open_editor)

    todo_parser = subparsers.add_parser('todo', help='find todos')
    todo_parser.set_defaults(func=todo)

    sync_parser = subparsers.add_parser('sync', help='sync with remote repo')
    sync_parser.set_defaults(func=sync)

    tags_parser = subparsers.add_parser('tags', help='show entries from tags')
    tags_parser.add_argument('-u', '--union', help='print union of supplied tags, rather than filtering',
                             action='store_true')
    # tags_parser.add_argument('-a', '-l' '--list-all', help='list all tags without showing the entries')
    tags_parser.add_argument('tags', nargs='*', help='list of tags to filter search to')
    tags_parser.set_defaults(func=list_tags)

    journal_parser = subparsers.add_parser('journal', help='make journal entry')
    journal_parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt all unencrypted journal entries')
    journal_parser.add_argument('-d', '--decrypt', help='decrypt journal entry')
    journal_parser.set_defaults(func=journal)

    links_parser = subparsers.add_parser('links', help='open common links')
    links_parser.set_defaults(func=links)

    args = parser.parse_args()

    # print help and exit if no arguments supplied
    if not hasattr(args, 'func'):
        parser.print_help()
        exit(0)

    # run setup script without config
    if args.func is setup:
        setup()
        sys.exit()

    # Load custom config if defined in env var
    cfg = None
    try:
        cfg_file = os.environ['WIKI_CONFIG'] if 'WIKI_CONFIG' in os.environ else os.path.expanduser('~/.personal.yml')
        with open(os.path.abspath(cfg_file), 'r') as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        print("Config file not found at ~/.personal.yml or defined in $WIKI_CONFIG. Have you ran `wiki setup`?")
        sys.exit(1)

    # Run the subcommand
    args.func(cfg, args)


if __name__ == "__main__":
    main()