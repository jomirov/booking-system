import redis
from datetime import datetime, timezone
from rq import Queue
from rq_scheduler import Scheduler
from ..dependencies import check_expired_bookings

r = redis.Redis(host="redis")
r.flushall()

q = Queue(connection=r)

s = Scheduler(queue=q, connection=r)
s.schedule(scheduled_time=datetime.now(timezone.utc), repeat=None, interval=60, func=check_expired_bookings)