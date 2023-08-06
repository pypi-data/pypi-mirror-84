"""Pattoo .Agent class.

Description:

    This module:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import textwrap
import sys
import argparse
import ipaddress
import multiprocessing
import os
from datetime import datetime


# PIP3 libraries
from gunicorn.app.base import BaseApplication

# Pattoo libraries
from pattoo_shared.daemon import Daemon, GracefulDaemon
from pattoo_shared import files
from pattoo_shared import encrypt
from pattoo_shared import log
from pattoo_shared.configuration import Config
from pattoo_shared.variables import AgentAPIVariable


class Agent():
    """Agent class for daemons."""

    def __init__(self, parent, child=None, config=None):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon
            config: Config object

        Returns:
            None

        """
        # Initialize key variables (Parent)
        if config is None:
            self.config = Config()
        else:
            self.config = config
        self.parent = parent
        self.pidfile_parent = files.pid_file(parent, self.config)
        self.lockfile_parent = files.lock_file(parent, self.config)

        # Initialize key variables (Child)
        if bool(child) is None:
            self._pidfile_child = None
        else:
            self._pidfile_child = files.pid_file(child, self.config)

    def name(self):
        """Return agent name.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self.parent
        return value

    def query(self):
        """Create placeholder method. Do not delete."""
        # Do nothing
        pass


class EncryptedAgent(Agent):
    """Encrypted Agent class for daemons."""

    def __init__(self, parent, child=None, config=None, directory=None):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon
            config: Config object
            directory: Override the directory for KeyRing storage if provided.

        Returns:
            None

        """
        # Initialize key variables (Parent)
        Agent.__init__(self, parent, child=child, config=config)

        # Create encryption object
        self.encryption = encrypt.Encryption(parent, directory=directory)


class _AgentRun():
    """Class that defines basic run function for AgentDaemons."""

    def run(self):
        """Start Polling

        Args:
            None

        Return:
            None

        """
        # Start polling. (Poller decides frequency)
        while True:
            self.agent.query()


class AgentDaemon(_AgentRun, Daemon):
    """Class that manages base agent daemonization"""

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: agent object

        Returns:
            None

        """
        # Initialize variables to be used by daemon
        self.agent = agent

        # Instantiate daemon superclass
        Daemon.__init__(self, agent)


class GracefulAgentDaemon(_AgentRun, GracefulDaemon):
    """Class that manages graceful agent daemonization."""

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: agent object

        Returns:
            None

        """
        # Initialize variables to be used by daemon
        self.agent = agent

        # Instantiate daemon superclass
        GracefulDaemon.__init__(self, agent)


class AgentCLI():
    """Class that manages the agent CLI.

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.parser = None

    def process(self, additional_help=None):
        """Return all the CLI options.

        Args:
            None

        Returns:
            args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        # Header for the help menu of the application
        parser = argparse.ArgumentParser(
            description=additional_help,
            formatter_class=argparse.RawTextHelpFormatter)

        # CLI argument for starting
        parser.add_argument(
            '--start',
            required=False,
            default=False,
            action='store_true',
            help='Start the agent daemon.'
        )

        # CLI argument for stopping
        parser.add_argument(
            '--stop',
            required=False,
            default=False,
            action='store_true',
            help='Stop the agent daemon.'
        )

        # CLI argument for getting the status of the daemon
        parser.add_argument(
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Get daemon daemon status.'
        )

        # CLI argument for restarting
        parser.add_argument(
            '--restart',
            required=False,
            default=False,
            action='store_true',
            help='Restart the agent daemon.'
        )

        # CLI argument for stopping
        parser.add_argument(
            '--force',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Stops or restarts the agent daemon ungracefully when '
                'used with --stop or --restart.', width=80)
        )

        # Get the parser value
        self.parser = parser

    def control(self, agent, graceful=False):
        """Control the pattoo agent from the CLI.

        Args:
            agent: Agent object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Instantiate agent daemon
        if graceful is False:
            _daemon = AgentDaemon(agent)
        else:
            _daemon = GracefulAgentDaemon(agent)

        # Run daemon
        if args.start is True:
            _daemon.start()
        elif args.stop is True:
            if args.force is True:
                _daemon.force()
            else:
                _daemon.stop()
        elif args.restart is True:
            if args.force is True:
                _daemon.force()
                _daemon.start()
            else:
                _daemon.restart()
        elif args.status is True:
            _daemon.status()
        else:
            parser.print_help()
            sys.exit(2)


class AgentAPI(Agent):
    """pattoo API agent that serves web pages.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, parent, child, app, config=None):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon
            app: Flask App
            config: Config object

        Returns:
            None

        """
        # Initialize key variables
        if config is None:
            _config = Config()
        else:
            _config = config

        # Apply inheritance
        Agent.__init__(self, parent, child=child, config=_config)
        self._app = app
        self._agent_api_variable = AgentAPIVariable(
            ip_bind_port=_config.ip_bind_port(),
            ip_listen_address=_config.ip_listen_address())

    def query(self):
        """Query all remote targets for data.

        Args:
            None

        Returns:
            None

        """
        # Check for lock and pid files
        if os.path.exists(self.lockfile_parent) is True:
            log_message = ('''\
Lock file {} exists. Multiple API daemons running API may have died \
catastrophically in the past, in which case the lockfile should be deleted.\
'''.format(self.lockfile_parent))
            log.log2see(1083, log_message)

        if os.path.exists(self.pidfile_parent) is True:
            log_message = ('''\
PID file: {} already exists. Daemon already running? If not, it may have died \
catastrophically in the past in which case you should use --stop --force to \
fix.'''.format(self.pidfile_parent))
            log.log2see(1084, log_message)

        ######################################################################
        #
        # Assign options in format that the Gunicorn WSGI will accept
        #
        # NOTE! to get a full set of valid options pprint(self.cfg.settings)
        # in the instantiation of _StandaloneApplication. The option names
        # do not exactly match the CLI options found at
        # http://docs.gunicorn.org/en/stable/settings.html
        #
        ######################################################################
        options = {
            'bind': _ip_binding(self._agent_api_variable),
            'accesslog': self.config.log_file_api(),
            'errorlog': self.config.log_file_api(),
            'capture_output': True,
            'pidfile': self._pidfile_child,
            'loglevel': self.config.log_level(),
            'workers': _number_of_workers(),
            'umask': 0o0007,
        }

        # Log so that user running the script from the CLI knows that something
        # is happening
        log_message = (
            'Pattoo API running on {}:{} and logging to file {}.'
            ''.format(
                self._agent_api_variable.ip_listen_address,
                self._agent_api_variable.ip_bind_port,
                self.config.log_file_api()))
        log.log2info(1022, log_message)

        # Run
        _StandaloneApplication(self._app, self.parent, options=options).run()


class EncryptedAgentAPI(AgentAPI):
    """Agent class for daemons."""

    def __init__(self, parent, child, app, config=None, directory=None):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            email: Email address used for encryption
            child: Name of child daemon
            config: Config object
            directory: Override the directory for KeyRing storage if provided.

        Returns:
            None

        """
        # Instantiate daemon superclass
        AgentAPI.__init__(self, parent, child, app, config=config)

        # Create encryption object
        self.encryption = encrypt.Encryption(parent, directory=directory)


class _StandaloneApplication(BaseApplication):
    """Class to integrate the Gunicorn WSGI with the Pattoo Flask application.

    Modified from: http://docs.gunicorn.org/en/latest/custom.html

    """

    def __init__(self, app, parent, options=None):
        """Initialize the class.

        args:
            app: Flask application object of type Flask(__name__)
            parent: Name of parent process that is invoking the API
            options: Gunicorn CLI options

        """
        # Initialize key variables
        self.options = options or {}
        self.parent = parent
        self.application = app
        super(_StandaloneApplication, self).__init__()

    def load_config(self):
        """Load the configuration."""
        # Initialize key variables
        now = datetime.now()
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])

        # Assign configuration parameters
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

        # Print configuration dictionary settings
        print('''{} Agent {} - Pattoo Gunicorn configuration\
'''.format(now.strftime('%Y-%m-%d %H:%M:%S.%f'), self.parent))
        for name, value in self.cfg.settings.items():
            print('  {} = {}'.format(name, value.get()))

    def load(self):
        """Run the Flask application throught the Gunicorn WSGI."""
        return self.application


def _number_of_workers():
    """Get the number of CPU cores on this server."""
    return (multiprocessing.cpu_count() * 2) + 1


def _ip_binding(aav):
    """Create IPv4 / IPv6 binding for Gunicorn.

    Args:
        aav: AgentAPIVariable object

    Returns:
        result: bind

    """
    # Initialize key variables
    ip_address = aav.ip_listen_address
    ip_bind_port = aav.ip_bind_port
    result = None

    # Check IP address type
    try:
        ip_object = ipaddress.ip_address(ip_address)
    except:
        result = '{}:{}'.format(ip_address, ip_bind_port)

    if bool(result) is False:
        # Is this an IPv4 address?
        ipv4 = isinstance(ip_object, ipaddress.IPv4Address)
        if ipv4 is True:
            result = '{}:{}'.format(ip_address, ip_bind_port)
        else:
            result = '[{}]:{}'.format(ip_address, ip_bind_port)

    # Return result
    return result
