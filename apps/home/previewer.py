from flask import render_template
from flask_login import current_user
from apps.authentication.box_oauth import box_client


def previewer(token: str):
    token = token

    # root_folder = box_client().folder(folder_id='0').get()
    # file_list = root_folder.get_items(limit=10, offset=0)
    # file_id = file_list[0]

    search_results = box_client().search().query(
        'a',
        limit=5,
        offset=0,
        ancestor_folders=[box_client().folder(folder_id='0')],
        file_extensions=['pdf'],
    )

    file_list = []

    for item in search_results:

        item_with_name = item.get(fields=['name'])
        print('matching item: ' + item_with_name.id)
        file_list.append(item_with_name.id)

    else:
        print('no matching items')

    file_id = file_list[0]

    contentSidebarProps = {
        'detailsSidebarProps': {
            'hasNotices': True,
            'hasProperties': True,
            'hasAccessStats': True,
            'hasVersions': True
        },
        'hasActivityFeed': True,
        'hasSkills': True,
        'hasVersions': True,
        'hasMetadata': True
    }

    options = {
        'container': '.ui-element',
        'header': 'light',
        'logoUrl': 'box',

        'collection': file_list,

        'hasHeader': True,
        'showAnnotations': False,
        'showDownload': True,

        'contentSidebarProps': contentSidebarProps,

    }

    isSingle = True if file_list.count == 1 else False

    return render_template('home/previewer.html',
                           segment='previewer',
                           avatar_url=current_user.avatar_url,
                           token=token,
                           file_id=file_id,
                           options=options,
                           isSingle=isSingle
                           )
