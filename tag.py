import re
import json
import asana
import argparse
import requests

# token
_PTA_TOKEN = '1/1199643979967628:e5d4f4a4ec1872a40c0d193cbd662019'


def get_client() -> asana.client.Client:
    return asana.Client.access_token(_PTA_TOKEN)


def create_tag_fields(client: asana.client.Client):
    result = client.custom_fields.create_custom_field({'name': 'Release Tag',
                                                       'resource_subtype': 'text',
                                                       'workspace': '1199643891683737'}, opt_pretty=True)
    # custom_field_id in result
    print(result)


def add_project_tag_field(client: asana.client.Client, project_id: str):
    try:
        client.projects.add_custom_field_setting_for_project(project_id,
                                                             {'custom_field': '1202134364504809'},
                                                             opt_pretty=True)
    except Exception:
        print("INFO: Release Tag exists in this project.")
    else:
        print("INFO: Release Tag added in this project.")


def update_task_tag_field(client: asana.client.Client, task_id: str, tag: str):
    data = {
        "custom_fields": {
            "1202134364504809": tag
        }
    }
    client.tasks.update_task(task_id, data, opt_pretty=True)


def get_task_by_tag(tag: str):
    url = f"https://api.github.com/repos/haiming3/test-monorepo/releases/tags/{tag}"
    res = requests.get(url)
    obj = json.loads(res.text)
    markdown_text = obj['body']
    task_list = []
    pattern = re.compile(r'[(](.*?)[)]', re.S)
    for line in markdown_text.split('\n'):
        result = re.findall(pattern, line)
        for item in result:
            mark_str = 'https://app.asana.com/0/'
            if mark_str in item:
                temp_list = item.split('/')
                task = {
                    'project': temp_list[4],
                    'task': temp_list[5]
                }
                task_list.append(task)
    return task_list


def modify_task_after_release(tag: str):
    task_list = get_task_by_tag(tag)
    for item in task_list:
        print(f"project: {item['project']}")
        add_project_tag_field(get_client(), item['project'])
        print(f"task: {item['task']}")
        update_task_tag_field(get_client(), item['task'], tag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', type=str, required=True,
                        help='tag in monorepo')

    args = parser.parse_args()

    print(args.tag)

    # create_tag_fields(get_client())
    modify_task_after_release(args.tag)

