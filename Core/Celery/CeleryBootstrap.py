"""Import every model module so SQLAlchemy mappers are configured in Celery workers."""

import Modules.Auth.Models  # noqa: F401
import Modules.Stock.Models  # noqa: F401
import Modules.Addresses.Models  # noqa: F401
import Modules.Order.Models  # noqa: F401
import Modules.Payment.Models  # noqa: F401
