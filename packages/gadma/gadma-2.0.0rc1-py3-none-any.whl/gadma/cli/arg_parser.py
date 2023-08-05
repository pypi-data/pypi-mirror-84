import tempfile
from ..version import __version__
from .settings_storage import HOME_DIR
from . import SettingsStorage
from ..core import SUPPORT_STRING
from ..utils import ensure_dir_existence

import warnings
import copy
import argparse
import sys
import os

TEST_SETTINGS = os.path.join(HOME_DIR, "test_settings")


def version():
    '''
    Returns string with current version.
    '''
    return "GADMA version " + str(
        __version__
    ) + "\tby Ekaterina Noskova (ekaterina.e.noskova@gmail.com)" + "\n"


def usage():
    '''
    Returns usage of tool.
    '''
    return version() + "" \
        "Usage: \n\tgadma\t-p/--params <params_file>\n"\
        "\t\t-e/--extra <extra_params_file>\n"\
        "\n\n"\
        "Instead/With -p/--params and -e/--extra option you can set:\n"\
        "\t-o/--output <output_dir>\toutput directory.\n"\
        "\t-i/--input <in.fs>/<in.txt>\tinput file with AFS or in dadi "\
        "format.\n"\
        "\t--resume <resume_dir>\t\tresume another launch from "\
        "<resume_dir>.\n"\
        "\t--only_models\t\t\tflag to take models only from another launch "\
        "(--resume option).\n\n"\
        "\t-h/--help\t\tshow this help message and exit.\n"\
        "\t-v/--version\t\tshow version and exit.\n"\
        "\t--test\t\t\trun test case.\n" + SUPPORT_STRING


class ArgParser(argparse.ArgumentParser):
    """
    Overrided class for argument parser.
    """
    def format_help(self):
        """
        Returns usage by calling :func:`usage`.
        """
        return usage()


def test_args():
    '''
    Put default args for test case.
    '''
    # Create storage from test settings
    settings_storage = SettingsStorage.from_file(TEST_SETTINGS)
    # Input test file
    curent_dir = os.path.dirname(os.path.abspath(__file__))
    settings_storage.input_file = os.path.join(curent_dir,
                                               "../../fs_examples/test.fs")
    # There is no output_directory, we put it to temporary directory
    settings_storage.output_directory = tempfile.mkdtemp("gadma_test_dir")
    # And put path to input file
    settings_storage.input_file = os.path.join(HOME_DIR,
                                               settings_storage.input_file)
    return settings_storage


def get_settings():
    '''
    Parse args from command line and store them in options_storage.

    :returns: tuple of parsed arguments and settings storage.
    '''
    usage = str(sys.argv[0]) + " -p <params_file>"

    # Create arguments parser
    parser = ArgParser(add_help=False)
    parser.add_argument('-p', '--params', metavar="<params_file>",
                        required=False, default=None)
    parser.add_argument('-e', '--extra', metavar="<extra_params_file>",
                        required=False, default=None)
    parser.add_argument('--resume', metavar="<dir>",
                        required=False, default=None)
    parser.add_argument('--only_models', action='store_true')
    parser.add_argument('-o', '--output', metavar="<dir>",
                        required=False, default=None)
    parser.add_argument('-i', '--input',
                        metavar="<filename.fs>/<filename.txt>",
                        required=False, default=None)
    parser.add_argument('-v', '--version', action='version',
                        version=version(), default=argparse.SUPPRESS)
    parser.add_argument('--test', action='store_true')
    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS)

    # If not enough arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # 1. Parse arguments
    args = parser.parse_args()

    # 2. Create Settings storage
    if args.test:
        print("--Running test case--")
        settings_storage = test_args()
        # We return as we do not need to check
        return settings_storage, args
    else:
        settings_storage = SettingsStorage.from_file(args.params, args.extra)

    # Check for resume
    if args.resume is not None:
        args.resume = os.path.abspath(os.path.expanduser(args.resume))
        if (settings_storage.resume_from is not None and
                settings_storage.resume_from != args.resume):
            raise ValueError(f"Resume directory in parameters file "
                             f"({settings_storage.resume_from}) doesn't "
                             f"match to one from the --resume option "
                             f"({args.resume})")
        settings_storage.resume_from = args.resume

    if args.only_models:
        settings_storage.only_models = True

    if settings_storage.resume_from is not None:
        old_params_file = os.path.join(settings_storage.resume_from,
                                       'params_file')
        old_extra_file = os.path.join(settings_storage.resume_from,
                                      'extra_params_file')
        if not os.path.exists(old_params_file):
            warnings.warn("There is no saved params file in resume directory. "
                          "Resume option will be ignored.")
            settings_storage.resume_from = None
            settings_storage.only_models = False
        else:
            if not os.path.exists(old_extra_file):
                old_extra_file = None
            resume_from_settings = SettingsStorage.from_file(
                old_params_file, old_extra_file)
            if (settings_storage.output_directory is None and
                    args.output is None):
                resume_from_settings.output_directory += "_resumed"
            else:
                resume_from_settings.output_directory = None
            settings_storage = copy.copy(resume_from_settings)
            settings_storage = settings_storage.update_from_file(args.params,
                                                                 args.extra)
            settings_storage.only_models = False
            if args.resume:
                settings_storage.resume_from = args.resume

    if args.output is not None:
        if (settings_storage.output_directory is not None and
                settings_storage.output_directory != args.output):
            warnings.warn("Output directory in parameters file doesn't match "
                          "to one from the -o/--output option. "
                          "The last is taken.")
        settings_storage.output_directory = args.output

    if args.input is not None:
        if (settings_storage.input_file is not None and
                settings_storage.input_file != args.input):
            warnings.warn("Input file in parameters file doesn't match to one"
                          " from -i/--input option. The last is taken.")
        settings_storage.input_file = args.input

    # 3. Checks that we have got all required
    if (settings_storage.input_file is None and
            settings_storage.resume_from is None):
        raise AttributeError("Input file is required. It could be set by "
                             "-i/--input option or via parameters file.")
    if (settings_storage.output_directory is None and
            settings_storage.resume_from is None):
        raise AttributeError("Output directory is required. It could be set "
                             "by -o/--output option or via parameters file.")
    assert settings_storage.output_directory is not None

    ensure_dir_existence(settings_storage.output_directory,
                         check_emptiness=True)

    if settings_storage.custom_filename is not None:
        if (settings_storage.lower_bound is None or
                settings_storage.upper_bound is None):
            raise AttributeError("Please specify either `Lower bound` and "
                                 "`Upper bound` or `Parameter identifiers` "
                                 "for custom model")
    else:
        if (settings_storage.initial_structure is None and
                settings_storage.final_structure is None):
            raise AttributeError("Please specify either structure of "
                                 "demographic history or filename with custom"
                                 " model.")

    if settings_storage.resume_from is not None:
        old_settings = SettingsStorage.from_file(
            os.path.join(settings_storage.resume_from, 'params_file'),
            os.path.join(settings_storage.resume_from, 'extra_params_file'))
        # check what have changed and can we deal with it
        if not settings_storage == old_settings:
            data_settings = ['input_file', 'projections', 'population_labels',
                             'outgroup']
            engine_settings = ['engine', 'pts', 'lower_bound', 'upper_bound',
                               'upper_bound_of_first_split',
                               'upper_bound_of_second_split']
            if_true_settings = ['no_migrations', 'only_sudden',
                                'symmetric_migrations', 'split_fractions']
            forbiden_settings = ['custom_filename', 'initial_structure']

            def differ_in_element(attr_list):
                for attr in attr_list:
                    if getattr(settings_storage, attr) !=\
                            getattr(old_settings, attr):
                        yield attr
            for attr in differ_in_element(data_settings + engine_settings):
                settings_storage.generate_x_transform = True
                if not settings_storage.only_models:
                    warnings.warn(f"Setting {attr} is different in new "
                                  "settings and all likelihoods should be "
                                  "recalculated in new run. Check option only_"
                                  "models maybe it should be set to True.")
                    break
            for attr in differ_in_element(if_true_settings):
                if getattr(settings_storage, attr):
                    settings_storage.generate_x_transform = True
                    if not settings_storage.only_models:
                        warnings.warn(f"Setting {attr} was changed from False "
                                      "to True in new settings and all "
                                      "likelihoods should be recalculated in "
                                      "new run. Check option only_models maybe"
                                      " it should be set to True.")
                    break
            for attr in differ_in_element(forbiden_settings):
                raise ValueError(f"Setting {attr} could not be changed in "
                                 "resumed run.")

    else:
        if settings_storage.only_models:
            warnings.warn("Option `only models`/--only_models  must be used "
                          " --resume option only. It would be ignored.")
    return settings_storage, args
