"""Functions for configuring pattoo components."""
# Standard imports
import os
import grp
import pwd
import getpass
from collections import defaultdict

# Import dependendices
import yaml

# Import pattoo related libraries
from pattoo_shared import files, log
from pattoo_shared.installation import shared


def _merge_config(default, modified):
    """Merge two lambda dicts together.

    Args:
        default: Default dict
        modified: Modified dict

    Returns:
        result: Merged dictionary

    """
    # Initialize key variables
    result = defaultdict(lambda: defaultdict(dict))

    # Merge configurations
    for key, value in default.items():
        if key in modified:
            if isinstance(value, dict):
                for _key, _value in modified[key].items():
                    result[key][_key] = _value
            else:
                result[key] = value
        else:
            result[key] = value

    # Merge the other way around
    for key, value in modified.items():
        if key not in result:
            result[key] = value

    # Convert to dict to facilitate YAML file processing
    result = dict(result)
    return result


def create_user(user_name, directory, shell, verbose):
    """Create user and their respective group.

    Args:
        user_name: The name and group of the user being created
        directory: The home directory of the user
        shell: The shell of the user
        verbose: A boolean value that a allows the script to run in verbose
        mode

    Returns:
        None

    """
    # Ensure user has sudo privileges
    if getpass.getuser() == 'root':

        # If the group specified does not exist, it gets created
        if not group_exists(user_name):
            shared.run_script('groupadd {0}'.format(user_name), verbose)

        # If the user specified does not exist, they get created
        if not user_exists(user_name):
            shared.run_script(
                'useradd -d {1} -s {2} -g {0} {0}'.format(
                    user_name, directory, shell), verbose)
    else:
        # Die if not root
        shared.log('You are currently not running the script as root')


def group_exists(group_name):
    """Check if the group already exists.

    Args:
        group_name: The name of the group

    Returns
        True if the group exists and False if it does not

    """
    try:
        # Gets group name
        grp.getgrnam(group_name)
        return True
    except KeyError:
        return False


def read_config(filepath, default_config):
    """Read configuration file and replace default values.

    Args:
        filepath: Name of configuration file
        default_config: Default configuration dict

    Returns:
        config: Dict of configuration

    """
    # Initialize key variables
    config = {}

    # Read config
    if os.path.isfile(filepath) is True:
        try:
            f_handle = open(filepath, 'r')
        except PermissionError:
            log.log2die_safe(1078, '''\
Insufficient permissions for reading the file:{}'''.format(filepath))
        else:
            with f_handle:
                yaml_string = f_handle.read()
                file_config = yaml.safe_load(yaml_string)

        # Merge configurations
        config = _merge_config(default_config, file_config)
    else:
        config = default_config
    return config


def check_config(config_file, config_dict):
    """Ensure agent configuration exists.

    Args:
        config: The name of the configuration file
        config_dict: A dictionary containing the primary configuration keys
        and a list of the secondary keys

    Returns:
        None

    """
    # Initialize key variables
    config_directory = os.environ['PATTOO_CONFIGDIR']

    # Print Status
    print('??: Checking configuration parameters.')

    # Retrieve config dict
    config = files.read_yaml_file(config_file)

    # Check main keys
    for primary in config_dict.keys():
        if primary not in config:
            log_message = ('''\
Section "{}" not found in configuration file {} in directory {}. Please fix.\
    '''.format(primary, config_file, config_directory))
            log.log2die_safe(1055, log_message)

    # Print Status
    print('OK: Configuration parameter check passed.')


def user_exists(user_name):
    """Check if the user already exists.

    Args:
        user_name: The name of the user

    Returns
        True if the user exists and False if it does not

    """
    try:
        # Gets user name
        pwd.getpwnam(user_name)
        return True
    except KeyError:
        return False


def pattoo_config(file_name, config_directory, config_dict):
    """Create configuration file.

    Args:
        file_name: Name of the configuration file without its file extension
        config_directory: Full path to the configuration directory
        config_dict: A dictionary containing the configuration values.

    Returns:
        The path to the configuration file

    """
    # Initialize key variables
    config_file = os.path.join(config_directory, '{}.yaml'.format(file_name))

    # Say what we are doing
    print('\nConfiguring {} file.\n'.format(config_file))

    # Get configuration
    config = read_config(config_file, config_dict)

    # Check validity of directories, if any
    if bool(config) is False:
        # Set default
        config = config_dict

    # Iterate over config dict
    for _, value in sorted(config.items()):
        if isinstance(value, dict) is True:
            for secondary_key in value.keys():
                if 'directory' in secondary_key:
                    if os.sep not in value.get(secondary_key):
                        log.log2die_safe(
                            1019, '{} is an invalid directory'.format(value))

                    # Attempt to create directory
                    full_directory = os.path.expanduser(
                        value.get(secondary_key))
                    if os.path.isdir(full_directory) is False:
                        print('Creating: {}'.format(full_directory))
                        files.mkdir(full_directory)

                    # Recursively set file ownership to pattoo user and group
                    if getpass.getuser() == 'root':
                        shared.chown(full_directory)

    # Write file
    try:
        f_handle = open(config_file, 'w')
    except PermissionError:
        log.log2die(1076, '''\
Insufficient permissions for creating the file:{}'''.format(config_file))
    else:
        with f_handle:
            yaml.safe_dump(config, stream=f_handle, default_flow_style=False)

    return config_file


def configure_component(component_name, config_dir, config_dict):
    """Configure individual pattoo related components and check configuration.

    Args:
        component_name: The file name for the component being configured
        config_dir: The directory with the configuration files
        config_dict: A dictionary containing the configuration values

    Returns:
        None

    """
    # Create configuration
    config_file = pattoo_config(component_name, config_dir, config_dict)

    # Check if configuration is valid
    check_config(config_file, config_dict)
