import os
import logging
import requests

from ..exception import RestCredentailsError, RestClientConfigurationError
from . import NetRCAuth, RESTAuthentication, AuthConfig
from ..utils import URLValidator


logger = logging.getLogger(__name__)


class CASCredentailsError(RestCredentailsError):
    pass


class CASGrantingTicketError(CASCredentailsError):
    pass


class CASServiceTicketError(CASCredentailsError):
    pass


# ==========================================================================================


class CASAuth(RESTAuthentication):
    """
    Subclass of the RESTAuthentication that is able to use CAS to request and store
    a ticket-granting-ticket and subsequent service tickets.
    """

    # -------------------------------------------------------------------------------------
    def __init__(self, rest_client, auth_config_object):
        """
        CASAuth constructor

        :param rest_client: A reference to the RESTclient object
        :type rest_client: ``RESTclient``

        :param auth_config_object: The configuration object
        :type auth_config_object: ``AuthConfig``

        """

        super(CASAuth, self).__init__(rest_client)

        config = auth_config_object

        # the remote URL for the CAS server
        self.server = None
        self.service = config.service_name
        self.ticket_path = "/".join(config.path)  # the URL path

        self.tgt_volatile_storage = False
        self.tgt_file_name = None
        self.__ticket_granting_ticket = None  # content of the TGT

    # -------------------------------------------------------------------------------------
    def set_credentials(
        self,
        server_url,
        service_name=None,
        verify_ssl=False,
        netrc_path=os.path.expanduser("~/.netrc"),
        username=None,
        password=None,
        tgt_volatile_storage=False,
        granting_ticket_filepath=None,
        ticket_granting_ticket=None,
    ):
        """
        CAS-auth requires a secondary auth, so it has two authentication levels...
        Allow logins via either netRC or user/pass.
        If netrc is true, try this. Else, try user/pass if supplied.
        If neither is available, raise error


        :param server_url: the URL of the CAS server
        :type server_url: ``string_type``

        :param service_name: the name of the service of CAS
        :type service_name: ``string_type``


        :param verify_ssl: Whether the CAS client should verify SSL certificates upon making
            requests
        :type verify_ssl: ``bool``  or `` string_type``

        :param netrc_path: The path to Netrc
        :type netrc_path: ``string_type_or_none``

        :param username: The user for authenticating with the CAS end-point
        :type username: ``string_type_or_none``

        :param password: The password for authenticating with the CAS end-point
        :type password: ``string_type_or_none``

        :param granting_ticket_filepath: The local path where a "ticket getting ticket" will be
            saved
        :type granting_ticket_filepath: ``string_type``

        :param tgt_volatile_storage: Is the TGT stored on the filesystem or handed over to the user
        :type tgt_volatile_storage: ``boolean``
        """

        # the connection parameters
        self.server = server_url
        self.service_name = service_name
        self.verify_ssl = verify_ssl
        parent_auth = NetRCAuth(rest_client=self.rest_client)

        # ---- parameter verification -----
        # TGT in file or attribute
        self.tgt_volatile_storage = tgt_volatile_storage
        if tgt_volatile_storage:
            if not ticket_granting_ticket:
                self.ticket_granting_ticket = None
            try:
                self.ticket_granting_ticket = ticket_granting_ticket
            except CASGrantingTicketError:
                # the TGT was not a valid URL: reset local to None to clear out
                logger.debug(
                    "[CAS] was provided with unusable TGT: '%s', resettign to None"
                    % ticket_granting_ticket
                )
                self.ticket_granting_ticket = None

        else:
            if not granting_ticket_filepath:
                raise RestClientConfigurationError(
                    "TGT path must be set if volatile_storage is False"
                )
            self.tgt_file_name = os.path.expanduser(granting_ticket_filepath)

        # if username/pass are provided, then always request a new TGT
        if self.are_valid_credentials(username, password):
            self.ticket_granting_ticket = self.request_new_tgt(username, password)
        elif netrc_path:
            # try to get creds from parent, in case we may need it later
            # if this request fails, its ok for now
            try:
                parent_auth.set_credentials(netrc_path=netrc_path)
                username = parent_auth.username
                password = parent_auth.password
            except ValueError:
                pass

        # if no TGT, then a new request needs to be made: either using
        # user/pass, or netrc as backup
        if not self.ticket_granting_ticket:
            if not self.are_valid_credentials(username, password):
                raise RestCredentailsError(
                    "no username or password is provided via parameters or in netrc file"
                )
            self.ticket_granting_ticket = self.request_new_tgt(username, password)

        # ok, we should have a TGT, but it may be outdated or otherwise bad
        try:
            self.request_new_service_ticket()
        except CASServiceTicketError as e:
            # we could not get a service ticket, lets try a new tgt
            logger.debug("[CAS] could not get service ticket with old TGT, try to get a new one")
            if not self.are_valid_credentials(
                username, password
            ):  # this uses the netrc creds, but only after trying without first
                raise RestCredentailsError(
                    "[CAS] could not get service ticket, and netrc credentials are invalid or "
                    'absent. Exact error msg="%s"' % str(e)
                )
            try:
                self.ticket_granting_ticket = self.request_new_tgt(username, password)
                self.request_new_service_ticket()
            except CASGrantingTicketError as e2:
                raise RestCredentailsError(
                    '[CAS] could not get TGT while using netrc credentials. Exact error msg="%s"'
                    % str(e2)
                )
            except CASServiceTicketError as e2:
                raise RestCredentailsError(
                    "[CAS] could not get service ticket, despite getting a new TGT. Exact error "
                    'msg="%s"' % str(e2)
                )

        self.credentials_are_set = True

    # -------------------------------------------------------------------------------------
    def request_new_service_ticket(self):
        """Retrieves the service ticket that will ultimately be used inside the
request to the REST end-point.

        :return: The text or token to be used inside the Authorization header of the RESTful
            request
        :rtype: ``string_type``

        """
        logger.debug("[CAS] Requesting new service ticket")

        # allow override of service name
        if self.service_name:
            body = {"service": self.service_name}
        else:
            body = {"service": self.service}

        if not self.ticket_granting_ticket:
            logger.debug("[CAS] No granting ticket available while asking for a service ticket")
            raise CASServiceTicketError("[CAS] No granting ticket available")

        response = requests.post(
            url=self.ticket_granting_ticket, data=body, verify=self.verify_ssl
        )
        if not response.ok:
            logger.debug("[CAS] Service ticket request failed")
            raise CASServiceTicketError(
                "Cannot authenticate against CAS service using service name '{service}'. HTTP "
                "status code: '{status}'".format(
                    status=response.status_code, service=body["service"]
                )
            )

        return response.text

    # -------------------------------------------------------------------------------------
    @property
    def ticket_granting_ticket(self):
        """
        Reads the ticket getting ticket that will ultimately be used inside
        the request to the CAS end-point for retrieving a service ticket.
        The "tgtPath" parameter has to point to an existing location.

        :return: The URL to be used for retrieving a service ticket from the CAS end-point
        :rtype: ``string_type``
        """
        if self.tgt_volatile_storage:
            if not self.__ticket_granting_ticket:
                return None
            logger.debug(
                "[CAS] Reading TGT from memory: contents are '%s'", self.__ticket_granting_ticket
            )  # printing credentials here!
            return self.__ticket_granting_ticket
        else:
            if not self.tgt_file_name:
                logger.warning("[CAS] no tgt file path provided")
                return None
            elif not os.path.isfile(self.tgt_file_name):
                logger.warning("[CAS] File '%s' does not exist.", self.tgt_file_name)
                dirname = os.path.dirname(self.tgt_file_name)
                if not os.path.isdir(dirname):
                    os.mkdir(dirname, 0o700)
                return None
            else:
                with open(self.tgt_file_name, "r") as tgt_file:
                    tgt = tgt_file.read().strip()
                logger.debug(
                    "[CAS] Reading TGT from file: contents are '%s'", tgt
                )  # printing credentials here!
                if tgt == "":
                    os.remove(self.tgt_file_name)
                    raise CASGrantingTicketError(
                        "[CAS] TGT file at '%s' was empty and has been removed."
                        % self.tgt_file_name
                    )
                else:
                    return tgt

    # -------------------------------------------------------------------------------------
    @ticket_granting_ticket.setter
    def ticket_granting_ticket(self, tgt):
        """
        depending on method, store TGT in file or within class instance
        """

        # special case: if TGT is None then clear the underlying variable
        if tgt is None:
            self.__ticket_granting_ticket = None
            return

        # Validate the REST API base URL
        url_validator = URLValidator()
        url_validator.check(tgt)

        # the content of tgt is in a variable
        if self.tgt_volatile_storage:
            self.__ticket_granting_ticket = tgt
        else:
            # tgt is on file on disk
            logger.debug("[CAS] TGT URI is '%s'", tgt)
            tgt_dir = os.path.dirname(self.tgt_file_name)
            if not os.path.isdir(tgt_dir):
                os.makedirs(tgt_dir)
            if os.path.isfile(self.tgt_file_name):
                os.remove(self.tgt_file_name)
            with open(self.tgt_file_name, "w") as tgt_file:
                tgt_file.write(tgt)

    # -------------------------------------------------------------------------------------
    def request_new_tgt(self, username, password):
        """ Retrieves the ticket getting ticket that will ultimately be used inside the request to the CAS
            end-point for retrieving a service ticket.
        If the "tgtPath" parameter isn't pointing to an existing location, that location will be
        created. If the file at "tgtPath" exists, it will be replaced by the newly retrieved TGT.
        """

        if not self.are_valid_credentials(username, password):
            raise CASGrantingTicketError(
                "TGT: no valid username or password available to request a ticket-granting-ticket"
            )

        logger.debug("[CAS] Renewing granting ticket")
        ticket_url = "{server}/{path}".format(server=self.server, path=self.ticket_path)
        response = requests.post(
            url=ticket_url,
            data={"username": username, "password": password},
            verify=self.verify_ssl,
        )

        if response.status_code == 401:
            raise CASGrantingTicketError(
                'TGT: could not login using provided username "%s" and password' % username
            )
        elif (response.status_code < 200) or (response.status_code >= 300):
            raise CASGrantingTicketError(
                "TGT: Cannot authenticate against CAS using provided 'username:{username}' and "
                " 'password'. HTTP status code: '{status}'".format(
                    status=response.status_code, username=username
                )
            )

        tgt = response.headers["location"]
        return tgt

    # -------------------------------------------------------------------------------------
    def __call__(self, r):
        """Is called by the requests library when authentication is needed while
        issuing a RESTful request.

        Will retrieve a new service ticket or token if necessary. Adds the
        Authorization header and supplies the correct service ticket or token
        to it.

        """
        service_ticket = self.request_new_service_ticket()
        logger.debug("[CAS] add service ticket to request header")
        r.headers["Authorization"] = "CAS {service_ticket}".format(service_ticket=service_ticket)
        return r


# ==========================================================================================
class CasAuthConfig(AuthConfig):
    """
    CAS authentication specific for the CLS implementation below
    """

    authentication_module = CASAuth

    # -------------------------------------------------------------------------------------
    def __init__(self, path, service_name):
        """
        :param path: The absolute path for the ticket granting tickets
        :type path: ``list``

        :param service: The service name used to authenticate with the CAS end-point
        :type service: ``string_type``

        """

        self.path = path
        self.service_name = service_name
