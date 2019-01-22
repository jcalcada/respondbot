# respondbot

Respondbot can automatically acknowledge and resolve incidents in your PagerDuty domain after a period of time that is randomly chosen from a range you specify. It is designed to run continuously and poll PagerDuty every 30 seconds.

## Notes:
* It will always acknowledge and resolve as the currently assigned user
* Validation and error handling is largely TBD
* "acknowledge" and "resolve" are currently both required (you can't just put one and not the other in a service)

## Installation:

* Clone this repo
* Create a python3 virtual environment: `python3 -m venv venv`
* Activate the virtual environment: `. venv/bin/activate`
* Install the dependencies: `pip install -r requirements.txt`
* Edit respondbot_config.json and add values for your PagerDuty domain
* `python ./respondbot.py`
* Share and Enjoy!

## Sample output:

```
Found triggered incident [#16232] howdy (PWK1CGV), created at 2019-01-22 18:06:24+00:00
  Will acknowledge incident PWK1CGV at 2019-01-22 18:07:27+00:00
Found triggered incident [#16233] hey wat up (PAV73D2), created at 2019-01-22 18:06:41+00:00
  Will acknowledge incident PAV73D2 at 2019-01-22 18:07:53+00:00
Found triggered incident [#16234] was good (PXMLYJK), created at 2019-01-22 18:06:52+00:00
  Will acknowledge incident PXMLYJK at 2019-01-22 18:09:42+00:00
Should ack incident [#16232] howdy (PWK1CGV)
  Acknowledge by Martin Stone - martin@pagerduty.com (P7J8E4T)
Should ack incident [#16233] hey wat up (PAV73D2)
  Acknowledge by Martin Stone - martin@pagerduty.com (P7J8E4T)
Found acknowledged incident [#16232] howdy (PWK1CGV), created at 2019-01-22 18:06:24+00:00
  Will resolve incident PWK1CGV at 2019-01-22 18:10:16+00:00
Found acknowledged incident [#16233] hey wat up (PAV73D2), created at 2019-01-22 18:06:41+00:00
  Will resolve incident PAV73D2 at 2019-01-22 18:10:41+00:00
Should ack incident [#16234] was good (PXMLYJK)
  Acknowledge by Jayne Cobb - martin+jayne@pagerduty.com (PB8YWB8)
Found acknowledged incident [#16234] was good (PXMLYJK), created at 2019-01-22 18:06:52+00:00
  Will resolve incident PXMLYJK at 2019-01-22 18:14:17+00:00
Should resolve incident [#16232] howdy (PWK1CGV)
  Resolve by Martin Stone - martin@pagerduty.com (P7J8E4T)
Found acknowledged incident [#16233] hey wat up (PAV73D2), created at 2019-01-22 18:06:41+00:00
  Will resolve incident PAV73D2 at 2019-01-22 18:10:34+00:00
Found acknowledged incident [#16234] was good (PXMLYJK), created at 2019-01-22 18:06:52+00:00
  Will resolve incident PXMLYJK at 2019-01-22 18:16:40+00:00
Should resolve incident [#16233] hey wat up (PAV73D2)
  Resolve by Martin Stone - martin@pagerduty.com (P7J8E4T)
Should resolve incident [#16234] was good (PXMLYJK)
  Resolve by Jayne Cobb - martin+jayne@pagerduty.com (PB8YWB8)
```