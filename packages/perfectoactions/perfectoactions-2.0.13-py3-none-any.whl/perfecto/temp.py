import json
import re
import time
from datetime import datetime, timedelta

response = '{"reportPdfUrl": "https://ps.app.perfectomobile.com/export/api/v1/test-executions/pdf?externalId[0]=genesist@perfectomobile.com_controller_20-11-04_09_23_28_6163&_timestamp[0]=1604481813918", "executionId": "genesist@perfectomobile.com_controller_20-11-04_09_23_28_6163"}'





status = getTimestamp(
        response,
        r"reportPdfUrl\"\:[\s]?\".*\",[\s]?\"executionId",
        ':[\s]?".*$',
    )
print(status)
