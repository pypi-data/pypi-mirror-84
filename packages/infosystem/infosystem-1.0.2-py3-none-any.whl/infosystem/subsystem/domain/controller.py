import json

import flask

from infosystem.common import exception, utils
from infosystem.common.exception import BadRequest
from infosystem.common.subsystem import controller
from infosystem.subsystem.image.resource import QualityImage


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super(Controller, self).__init__(
            manager, resource_wrap, collection_wrap)

    def _get_name_in_args(self):
        name = flask.request.args.get('name', None)
        if not name:
            raise BadRequest()
        return name

    def domain_by_name(self):
        try:
            name = self._get_name_in_args()
            domain = self.manager.domain_by_name(domain_name=name)
            response = {self.resource_wrap: domain.to_dict()}
            return flask.Response(response=json.dumps(response, default=str),
                                  status=200,
                                  mimetype="application/json")
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def domain_logo_by_name(self):
        try:
            kwargs = {}
            quality = flask.request.args.get('quality', None)
            kwargs['quality'] = \
                QualityImage[quality] if quality else QualityImage.med
            name = self._get_name_in_args()
            folder, filename = self.manager.domain_logo_by_name(
                domain_name=name, **kwargs)
            return flask.send_from_directory(folder, filename)
        except KeyError:
            return self.get_bad_request('Unknown Quality')
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def get_token_id(self):
        return flask.request.headers.get('token')

    def get_token(self, token_id):
        return self.manager.api.tokens.get(id=token_id)

    def get_domain(self, domain_id):
        return self.manager.api.domains.get(id=domain_id)

    def get_domain_id_from_token(self, token):
        user = self.manager.api.users.get(id=token.user_id)
        return user.domain_id

    def get_domain_id(self):
        token = self.get_token(self.get_token_id())
        domain_id = self.get_domain_id_from_token(token)
        return domain_id

    def upload_logo(self, id):
        try:
            token = flask.request.headers.get('token')
            file = flask.request.files.get('file', None)
            if not file:
                raise exception.BadRequest('ERROR! File not found in request.')

            image = self.manager.upload_logo(id=id, token=token, file=file)

            response = {'image': image.to_dict()}
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype="application/json")

    def remove_logo(self, id):
        try:
            self.manager.remove_logo(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")

    def register(self):
        try:
            data = flask.request.get_json()

            username = data.get('username', 'admin').lower()
            email = data.get('email', None)
            password = data.get('password', None)
            domain_name = data.get('domain_name', None)
            domain_display_name = data.get('domain_display_name', None)
            application_name = data.get('application_name', None)

            self.manager.register(
                username=username, email=email,
                password=password, domain_name=domain_name,
                domain_display_name=domain_display_name,
                application_name=application_name)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")

    def activate(self, id1, id2):
        try:
            token_id = flask.request.headers.get('token')
            self.manager.activate(
                token_id=token_id, domain_id=id1, user_admin_id=id2)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")

    def create_setting(self, id):
        try:
            data = flask.request.get_json()

            setting = self.manager.create_setting(id=id, **data)
            response = {'setting': setting.to_dict()}

            return flask.Response(response=utils.to_json(response),
                                  status=201,
                                  mimetype="application/json")
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def update_setting(self, id1, id2):
        domain_id = id1
        setting_id = id2
        try:
            data = flask.request.get_json()

            setting = self.manager.update_setting(id=domain_id,
                                                  setting_id=setting_id,
                                                  **data)
            response = {'setting': setting.to_dict()}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def remove_setting(self, id1, id2):
        domain_id = id1
        setting_id = id2
        try:
            setting = self.manager.remove_setting(id=domain_id,
                                                  setting_id=setting_id)
            response = {'setting': setting.to_dict()}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
