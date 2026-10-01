from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

redis = Redis(host="redis", port=6379)

s = Scheduler(connection=redis)

booking_task = "dependencies.check_expired_bookings"
s.schedule(
    scheduled_time=datetime.now(),
    func=booking_task,
    interval=60,
)

q = Queue(connection=redis)
q.enqueue(booking_task)