# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashFacebookLogin(Component):
    """A DashFacebookLogin component.
DashFacebookLogin provides a Facebook login button for Plotly Dash dashboards.
For details on its configuration, see https://developers.facebook.com/docs/facebook-login/web/login-button/

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- appId (string; required): Your Facebook application ID. If you don't have one find it in the App dashboard
or go there to create a new app.
- language (string; default "en_US"): The language code, such as "en_US".
@default en_US
- version (string; default "v8.0"): Determines which versions of the Graph API and any API dialogs or
plugins are invoked when using the .api() and .ui() functions. Valid
values are determined by currently available versions, such as 'v2.0'.
@default v8.0
- cookie (boolean; default False): Determines whether a cookie is created for the session or not. If enabled,
it can be accessed by server-side code.
@default false
- status (boolean; default False): Determines whether the current login status of the user is freshly retrieved
on every page load. If this is disabled, that status will have to be manually
retrieved using .getLoginStatus().
@default false
- xfbml (boolean; default False): Determines whether XFBML tags used by social plugins are parsed, and
therefore whether the plugins are rendered or not.
@default false
- frictionlessRequests (boolean; default False): Frictionless Requests are available to games on Facebook.com or on mobile
web using the JavaScript SDK. This parameter determines whether they are
enabled.
@default false
- autoLogoutLink (boolean; default False): If enabled, the button will change to a logout button when the user is logged in.
@default false
- scope (string; default "public_profile"): The list of permissions to request during login.
@default public_profile
- size (a value equal to: "small", "medium", "large"; default "small"): Picks one of the size options for the button.
@default small
- defaultAudience (a value equal to: "everyone", "friends", "only_me"; default "friends"): Determines what audience will be selected by default, when requesting write permissions.
@default friends
- layout (a value equal to: "default", "rounded"; default "default"): Determines the display type of the button.
@default default
- buttonType (a value equal to: "continue_with", "login_with"; default "continue_with"): Determines the type of button text.
@default continue_with
- useContinueAs (boolean; default False): Determines whether to show the user's profile picture when available.
@default false
- className (string; default "fb-login-button"): A custom class to add to the button.
@default fb-login-button
- facebookLoginResponse (dict; optional): The properties returned by the Facebook login callback."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, appId=Component.REQUIRED, language=Component.UNDEFINED, version=Component.UNDEFINED, cookie=Component.UNDEFINED, status=Component.UNDEFINED, xfbml=Component.UNDEFINED, frictionlessRequests=Component.UNDEFINED, autoLogoutLink=Component.UNDEFINED, scope=Component.UNDEFINED, size=Component.UNDEFINED, defaultAudience=Component.UNDEFINED, layout=Component.UNDEFINED, buttonType=Component.UNDEFINED, useContinueAs=Component.UNDEFINED, className=Component.UNDEFINED, facebookLoginResponse=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'appId', 'language', 'version', 'cookie', 'status', 'xfbml', 'frictionlessRequests', 'autoLogoutLink', 'scope', 'size', 'defaultAudience', 'layout', 'buttonType', 'useContinueAs', 'className', 'facebookLoginResponse']
        self._type = 'DashFacebookLogin'
        self._namespace = 'dash_facebook_login'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'appId', 'language', 'version', 'cookie', 'status', 'xfbml', 'frictionlessRequests', 'autoLogoutLink', 'scope', 'size', 'defaultAudience', 'layout', 'buttonType', 'useContinueAs', 'className', 'facebookLoginResponse']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['appId']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashFacebookLogin, self).__init__(**args)
