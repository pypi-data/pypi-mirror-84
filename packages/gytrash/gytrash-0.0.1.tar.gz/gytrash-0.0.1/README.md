`pip install gytrash`

## Set Slack Environment Variables
`export SLACK_BOT_TOKEN="<BOT TOKEN>"`


## Import Gytrash and setup logger
```
import gytrash
import logging
log = logging.getLogger("slack_example")

gytrash.setup_logging(log, log_level=10, log_from_botocore=False, log_to_slack=True, slack_log_channel="<LOG NAME>", slack_log_level=20)

log.info("Test info message")
log.debug("Test debug message")
```