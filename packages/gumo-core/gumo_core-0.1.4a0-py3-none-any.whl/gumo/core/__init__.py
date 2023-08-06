from gumo.core._configuration import configure
from gumo.core._configuration import get_config

from gumo.core.exceptions import ConfigurationError

from gumo.core.infrastructure.configuration import GumoConfiguration
from gumo.core.domain.configuration import GoogleCloudProjectID

from gumo.core.domain.entity_key import EntityKey
from gumo.core.domain.entity_key import NoneKey
from gumo.core.domain.entity_key import EntityKeyFactory

from gumo.core.application.entity_key import EntityKeyGenerator

from gumo.core.infrastructure import MockAppEngineEnvironment
from gumo.core.infrastructure.credential import get_google_oauth_credentials
from gumo.core.infrastructure.credential import get_google_id_token_credentials


# backward compatibility
get_google_oauth_credential = get_google_oauth_credentials
get_google_id_token_credential = get_google_id_token_credentials


__all__ = [
    configure.__name__,
    get_config.__name__,

    ConfigurationError.__name__,

    GumoConfiguration.__name__,
    GoogleCloudProjectID.__name__,

    EntityKey.__name__,
    NoneKey.__name__,
    EntityKeyFactory.__name__,

    EntityKeyGenerator.__name__,

    MockAppEngineEnvironment.__name__,
    get_google_oauth_credentials.__name__,
    get_google_id_token_credentials.__name__,

    # backward compatibility:
    get_google_oauth_credential.__name__,
    get_google_id_token_credential.__name__,
]


configure()
