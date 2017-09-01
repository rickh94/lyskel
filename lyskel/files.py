"""Classes for files and file info."""
import attr
from lyskel.lynames import Instrument, Ensemble
from lyskel.lynames import validate_mutopia


@attr.s
class Composer():
    """Stores and formats information about a composer."""
    name = attr.ib()

@attr.s
class Headers():
    """Class for storing header info."""
    dedication = attr.ib(default=None)
    title = attr.ib()
    subtitle = attr.ib(default=None)
    subsubtitle = attr.ib(default=None)
    poet = attr.ib(default=None)
    composer = attr.ib(Composer('Anonymous'))
    meter = attr.ib(default=None)
    arranger = attr.ib(default=None)
    tagline = attr.ib(default=None)
    copyright = attr.ib(default=None)

    # def add_mutopia_headers(self, *,
    #                         instruments,
    #                         source,
    #                         style,
    #                         license,
    #                         maintainer,
    #                         maintainerEmail,
    #                         maintainerWeb,
    #                         mutopiatitle=None,
    #                         mutopiapoet=None,
    #                         mutopiaopus=None,
    #                         date=None,
    #                         moreinfo):
    #     """
    #     Set header information for submission to the mutopia project.
    #
    #     Arguments: See mutopiaproject.org/contribute.hmtl for details
    #     """


def validate_instruments(instruments):
    """Validates either a list of instruments or instance of Ensemble."""
    if isinstance(instruments, list):
        if isinstance(instruments[0], Instrument):
            pass
    elif isinstance(instruments, Ensemble):
        pass
    else:
        raise TypeError("'instruments' must be a list of instruments or an "
                        "Ensemble instance.")


def convert_ensemble(instruments):
    """Returns list of instruments for mutopia headers."""
    if isinstance(instruments, Ensemble):
        return instruments.instruments
    return instruments




def _validate_style(style):
    """Calls validate_mutopia with field 'style'"""
    return validate_mutopia(data=style, field='style')


def _validate_composer(comp):
    """Calls validate_mutopia with field 'mutopiacomposer'"""
    return validate_mutopia(data=comp, field='mutopiacomposer')


def _validate_license(license):
    """Calls validate_mutopia with field 'license'"""
    return validate_mutopia(data=license, field='license')




@attr.s
class MutopiaHeaders():
    instruments = attr.ib(validator=validate_instruments,
                          convert=convert_ensemble)
    source = attr.ib(validator=attr.validators.instance_of(str))
    style = attr.ib(validator=_validate_style)