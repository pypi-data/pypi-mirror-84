import argparse
import os
from pathlib import Path

from PyInquirer import prompt

from subbot.lib.main_functions import check_mkv_properties, check_projects, check_subtitles
from subbot.lib.config import clean_upload_queue, SubbotConfig, upload_question
from subbot.lib.main_functions import update_subtitles, replace_subtitles, upload_mkv, move_mkv
from subbot.lib.mkv import create_mkv_properties
from subbot.utils.dictionaries import PathDict, pathdict_factory
from subbot.utils.jsonutils import read_json_dict
from subbot.utils.misc import get_hash

def cli():
    script_path = Path(__file__).parent.absolute()
    config = SubbotConfig(path=script_path / "config.json")
    main(config)

def main(config, args_list=[]):
    parser = argparse.ArgumentParser(description='automate subtitles management for lazy subbers')
    parser.add_argument('-m', '--manual', action='store_true', help='activate manual mode')
    if not args_list:
        args = parser.parse_args()
    else:
        parser.parse_args(args_list)

    config.check()

    properties_path = config.get("properties_path", Path())
    mkv_properties = read_json_dict(properties_path / "mkv_properties.json", object_pairs_hook=pathdict_factory)

    if not mkv_properties:
        mkv_properties = create_mkv_properties(properties_path)
    else:
        # Go through this pain only if the properties file has changed.
        properties_hash = get_hash(properties_path)
        if properties_hash != config.get("properties_hash", ""):
            print(f"Checking for changes in the MKV properties file...")
            config = check_mkv_properties(config, mkv_properties)

    config = check_projects(config, mkv_properties)

    config = check_subtitles(config)

    main_questions = [
        {
            'type': 'rawlist',
            'name': 'action',
            'message': 'What do you want to do?',
            'choices': [
                'Update the subtitles list but not their MKVs.',
                'Update the subtitles list and their MKVs.',
                'Upload MKVs (currently only Google Drive and MEGA are supported).',
                'Move MKVs into their directories.',
                'Exit.',
            ]
        }
    ]

    while True:
        action = prompt(main_questions)["action"]

        mux_queue = config.get("mux_queue", PathDict())
        projects = config.get("projects", PathDict())

        if action == "Update the subtitles list but not their MKVs.":
            if len(mux_queue) == 0:
                print("There's nothing to do here.")
            else:
                projects = update_subtitles(mux_queue, projects)
                print("Cleaning up the mux queue... ", end="")
                mux_queue.clear()
                print("Done.")
                config.save()

        elif action == "Update the subtitles list and their MKVs.":
            if len(mux_queue) == 0:
                print("There's nothing to do here.")
            else:
                config = replace_subtitles(config, mkv_properties)
                config.save()

        elif action == "Upload MKVs (currently only Google Drive and MEGA are supported).":
            upload_queue = config.get("upload_queue", PathDict())
            output_path = config.get("output_path", Path())

            if args.manual:
                print("Updating upload queue with the new files... ", end="")
                mkv_list = [file_ for file_ in output_path.iterdir() if file_.is_file() and file_.suffix == ".mkv"]

                for mkv in mkv_list:
                    for project in mkv_properties:
                        if upload_settings := mkv_properties[project].get(mkv, PathDict()).get("upload", PathDict()):
                            config.update_upload_queue(mkv, upload_settings)
                config.save() # Is it really needed here?

            question = upload_question(upload_queue)
            if question[0]["choices"]:
                answers = prompt(question) # add a style
                upload_queue = clean_upload_queue(upload_queue, answers=answers["upload"])
                secrets_path = config.get("secrets_path", Path())

                new_upload_queue = upload_mkv(upload_queue, secrets_path, output_path)

                config["upload_queue"] = new_upload_queue
                config.save()
            else:
                print("There are no files to upload.")

        elif action == "Move MKVs into their directories.":
            config = move_mkv(config)
            config.save()

        elif action == "Exit.":
            config.save()
            print("All right, see you!")
            break


if __name__ == '__main__':
    cli()
