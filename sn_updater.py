import os
import json
import urllib
import requests

import bpy
import bpy.utils.previews
from bpy.props import (StringProperty,
                       EnumProperty,
                       BoolProperty,
                       IntProperty,
                       PointerProperty)

import snap
from . import addon_updater_ops


def get_bubble_login_props():
    return bpy.context.window_manager.bubble_api


def set_login_status(status_type, status):
    login_props = get_bubble_login_props()
    login_props.status = status
    login_props.status_type = status_type


class Cache:
    BUBBLE_CACHE_FILE = os.path.join(
        # Use a user path to avoid permission-related errors
        bpy.utils.user_resource("SCRIPTS", "bubble_cache", create=True), ".cache")

    def read():
        if not os.path.exists(Cache.BUBBLE_CACHE_FILE):
            return {}

        with open(Cache.BUBBLE_CACHE_FILE, 'rb') as f:
            data = f.read().decode('utf-8')
            return json.loads(data)

    def get_key(key):
        cache_data = Cache.read()
        if key in cache_data:
            return cache_data[key]

    def save_key(key, value):
        cache_data = Cache.read()
        cache_data[key] = value
        with open(Cache.BUBBLE_CACHE_FILE, 'wb+') as f:
            f.write(json.dumps(cache_data).encode('utf-8'))

    def delete_key(key):
        cache_data = Cache.read()
        if key in cache_data:
            del cache_data[key]

        with open(Cache.BUBBLE_CACHE_FILE, 'wb+') as f:
            f.write(json.dumps(cache_data).encode('utf-8'))


class BubbleApi:
    def __init__(self):
        self.access_token = ''
        self.headers = {}
        self.username = ''
        self.display_name = ''
        self.next_results_url = None
        self.prev_results_url = None

    def build_headers(self):
        self.headers = {'Authorization': 'Bearer ' + self.access_token}

    def login(self, email, password):
        bpy.ops.wm.login_modal('INVOKE_DEFAULT')

    def is_user_logged(self):
        # if self.access_token and self.headers:
        if self.headers:
            return True

        return False

    def logout(self):
        self.access_token = ''
        self.headers = {}
        Cache.delete_key('username')
        Cache.delete_key('access_token')
        Cache.delete_key('key')

    def request_user_info(self):
        url = 'https://bubblecrm.classyclosets.com//api/snaplogin'
        requests.get(url, headers=self.headers, hooks={'response': self.parse_user_info})

    def get_user_info(self):
        return self.username


class BubbleLoginProps(bpy.types.PropertyGroup):
    def update_tr(self, context):
        self.status = ''
        if self.email != self.last_username or self.password != self.last_password:
            self.last_username = self.email
            self.last_password = self.password
            if not self.password:
                set_login_status('ERROR', 'Password is empty')
            bpy.ops.wm.bubble_login('EXEC_DEFAULT')

    email: StringProperty(
        name="email",
        description="User email",
        default="")

    password: StringProperty(
        name="password",
        description="User password",
        subtype='PASSWORD',
        default="",
        update=update_tr)

    access_token: StringProperty(
        name="access_token",
        description="oauth access token",
        subtype='PASSWORD',
        default="")

    status: StringProperty(name='', default='')
    status_type: EnumProperty(
        name="Login status type",
        items=(
            ('ERROR', "Error", ""),
            ('INFO', "Information", ""),
            ('FILE_REFRESH', "Progress", "")),
        description="Determines which icon to use",
        default='FILE_REFRESH')

    last_username: StringProperty(default="default")
    last_password: StringProperty(default="default")
    bubble_api = BubbleApi()


class SN_PT_UpdaterPanel(bpy.types.Panel):
    bl_label = "SNaP Updater"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_order = 0

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='FILE_REFRESH')

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="SNaP Version: {}.{}.{}".format(
            snap.bl_info['version'][0],
            snap.bl_info['version'][1],
            snap.bl_info['version'][2]),
            icon='KEYTYPE_JITTER_VEC')

        # bubble_login = get_bubble_login_props()
        # layout = self.layout.box().column(align=True)

        # if bubble_login.bubble_api.is_user_logged():
        #     login_col = layout.column()
        #     login_col.label(text='Logged in as: {}'.format(bubble_login.bubble_api.get_user_info()))
        #     # login_col.operator('wm.bubble_login', text='Logout', icon='FILE_TICK').authenticate = False
        #     if bubble_login.status:
        #         layout.prop(bubble_login, 'status', icon=bubble_login.status_type)
        # else:
        #     layout.label(text="Login to your account", icon='INFO')
        #     layout.prop(bubble_login, "email")
        #     layout.prop(bubble_login, "password")
        #     ops_row = layout.row()
        #     ops_row.operator('wm.bubble_login', text='Log in', icon="LINKED").authenticate = True
        #     if bubble_login.status:
        #         layout.prop(bubble_login, 'status', icon=bubble_login.status_type)

        addon_updater_ops.update_notice_box_ui(self, context)


class BubbleLogger(bpy.types.Operator):
    bl_idname = 'wm.bubble_login'
    bl_label = 'Bubble Login'
    bl_options = {'INTERNAL'}

    authenticate: BoolProperty(default=True)

    def execute(self, context):
        set_login_status('FILE_REFRESH', 'Login to your Bubble account...')
        wm = context.window_manager
        if self.authenticate:
            wm.bubble_api.bubble_api.login(wm.bubble_api.email, wm.bubble_api.password)
        else:
            wm.bubble_api.bubble_api.logout()
            wm.bubble_api.password = ''
            wm.bubble_api.last_password = "default"
            set_login_status('FILE_REFRESH', '')
        return {'FINISHED'}


class LoginModal(bpy.types.Operator):
    bl_idname = "wm.login_modal"
    bl_label = ""
    bl_options = {'INTERNAL'}

    is_logging: BoolProperty(default=False)
    error: BoolProperty(default=False)
    error_message: StringProperty(default='')

    def exectue(self, context):
        return {'FINISHED'}

    def handle_login(self, r, *args, **kwargs):
        # browser_props = get_sketchfab_props()
        if r.status_code == 200:
        # if r.status_code == 200 and 'access_token' in r.json():
            # browser_props.skfb_api.access_token = r.json()['access_token']
            login_props = get_bubble_login_props()
            # login_props.bubble_api.access_token = r.json()['access_token']
            Cache.save_key('username', login_props.email)
            # Cache.save_key('access_token', login_props.bubble_api.access_token)

            login_props.bubble_api.build_headers()
            set_login_status('INFO', '')
            login_props.bubble_api.username = login_props.email

        else:
            if 'error_description' in r.json():
                set_login_status('ERROR', 'Failed to authenticate: bad login/password')
            else:
                set_login_status('ERROR', 'Failed to authenticate: bad login/password')
                print('Cannot login.\n {}'.format(r.json()))

        self.is_logging = False

    def modal(self, context, event):
        if self.error:
            self.error = False
            set_login_status('ERROR', '{}'.format(self.error_message))
            return {"FINISHED"}

        if self.is_logging:
            set_login_status('FILE_REFRESH', 'Logging in to your account...')
            return {'RUNNING_MODAL'}
        else:
            return {'FINISHED'}

    def invoke(self, context, event):
        self.is_logging = True
        try:
            context.window_manager.modal_handler_add(self)
            login_props = get_bubble_login_props()
            url = 'https://bubblecrm.classyclosets.com//api/snaplogin'
            requests.get(
                url,
                auth=requests.auth.HTTPBasicAuth(
                    login_props.email,
                    login_props.password),
                hooks={'response': self.handle_login})
        except Exception as e:
            self.error = True
            self.error_message = str(e)

        return {'RUNNING_MODAL'}


classes = (
    BubbleLoginProps,
    SN_PT_UpdaterPanel,
    LoginModal,
    BubbleLogger
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.bubble_api = PointerProperty(type=BubbleLoginProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.bubble_api
