import time
import base64

from ..filetypes import FILETYPE
MAX_FILE_SIZE = 2 * 1 << 20


class ClientBase:
    client = None

    def __init__(self, address, project_token, auth_key):
        if address.endswith('/'):
            address = address[:-1]
        self.address = address
        self.project_token = project_token
        self.auth_key = auth_key
        self.headers = {
            'Project-Token': project_token,
            'Authenticate': auth_key
        }

    def prepare(self):
        pass

    def prepare_message(self, message, message_type):
        files = message.get('attachments')
        if type(files) is dict:
            files = [files]
        elif not type(files) in (list, tuple):
            files = []
        attachments = []
        for file in files:
            if type(file) is dict:
                content = file.get('content')
                if type(content) is str:
                    content = content.encode('utf8')
                if len(content) < MAX_FILE_SIZE:
                    filetype = file.get('type') or FILETYPE.TEXT
                    if type(filetype) is not str:
                        filetype = filetype.value
                    attachments.append({
                        'name': file.get('name') or '',
                        'content': base64.b64encode(content).decode('utf8'),
                        'type': filetype,
                        'mimetype': file.get('mimetype')
                    })
        return {'type': message_type, 'send_time': time.time(), 'function': '', 'filename': '', **message, 'attachments': attachments}

    def capture_message(self, message, type='message'):
        raise NotImplementedError

    def save_copy(self, message, type):
        pass

    def clean_copy(self, copy_id):
        pass
