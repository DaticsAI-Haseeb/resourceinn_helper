import logging
import random
import time
from datetime import datetime, timedelta

from celery import shared_task

from user.models import User, Log, ActionStatus, ActionChoices
from user.service import login_to_portal, do_check_in, do_check_out, toggle_break

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    logger.info(f"Adding {x} and {y}")
    Log.objects.create(user=User.objects.first(), action=ActionChoices.CHECK_IN, status=ActionStatus.CANCELLED)
    logger.info(f"Log created for user {User.objects.first().name} with action {ActionChoices.CHECK_IN} and status {ActionStatus.CANCELLED} at {datetime.now()}")
    return x + y


@shared_task
def perform_check_out(log_id):
    # Your Selenium script to perform check out
    logger.info(f"perform_check_out: Performing check out for log id {log_id}")
    log = Log.objects.get(pk=log_id)
    log.status = ActionStatus.IN_PROGRESS
    log.save()
    logger.info(f"perform_check_out: Log status updated to {ActionStatus.IN_PROGRESS} for log id {log_id}")
    try:
        logger.info(f"perform_check_out: Trying to perform check out for log id {log_id}")
        user = User.objects.first()
        logger.info(f"perform_check_out: Waiting for 10 seconds for log id {log_id}")
        time.sleep(10)
        logger.info(f"perform_check_out: Logging in to portal with user {user.email} for log id {log_id}")
        driver = login_to_portal(user.email, user.password)
        logger.info(f"perform_check_out: Logged in to portal for log id {log_id}")
        time.sleep(10)
        logger.info(f"perform_check_out: Performing check out for log id {log_id}")
        do_check_out(driver)
        logger.info(f"perform_check_out: Check out performed for log id {log_id}")
        time.sleep(10)
        logger.info(f"perform_check_out: Quitting driver for log id {log_id}")
        driver.quit()
        logger.info(f"perform_check_out: Driver quit for log id {log_id}")
    except Exception as e:
        logger.error(f"perform_check_out: Exception occurred: {e} for log id {log_id}")
        log.status = ActionStatus.FAILED
        log.save()
        logger.info(f"perform_check_out: Log status updated to {ActionStatus.FAILED} for log id {log_id}")
        raise e
    logger.info(f"perform_check_out: Log status updated to {ActionStatus.COMPLETED} for log id {log_id}")
    log.status = ActionStatus.COMPLETED
    log.save()
    logger.info(f"perform_check_out: Log status updated to {ActionStatus.COMPLETED} for log id {log_id}")


@shared_task
def perform_check_in(log_id):
    # Your Selenium script to perform check in
    logger.info(f"perform_check_in: Performing check in for log id {log_id}")
    log = Log.objects.get(pk=log_id)
    log.status = ActionStatus.IN_PROGRESS
    log.save()
    logger.info(f"perform_check_in: Log status updated to {ActionStatus.IN_PROGRESS} for log id {log_id}")
    try:
        logger.info(f"perform_check_in: Trying to perform check in for log id {log_id}")
        user = User.objects.first()
        logger.info(f"perform_check_in: Waiting for 10 seconds for log id {log_id}")
        time.sleep(10)
        logger.info(f"perform_check_in: Logging in to portal with user {user.email} for log id {log_id}")
        driver = login_to_portal(user.email, user.password)
        logger.info(f"perform_check_in: Logged in to portal for log id {log_id}")
        time.sleep(10)
        logger.info(f"perform_check_in: Performing check in for log id {log_id}")
        do_check_in(driver)
        logger.info(f"perform_check_in: Check in performed for log id {log_id}")
        time.sleep(10)
        logger.info(f"perform_check_in: Quitting driver for log id {log_id}")
        driver.quit()
        logger.info(f"perform_check_in: Driver quit for log id {log_id}")
    except Exception as e:
        logger.error(f"perform_check_in: Exception occurred: {e} for log id {log_id}")
        log.status = ActionStatus.FAILED
        log.save()
        logger.info(f"perform_check_in: Log status updated to {ActionStatus.FAILED} for log id {log_id}")
        raise e
    logger.info(f"perform_check_in: Log status updated to {ActionStatus.COMPLETED} for log id {log_id}")
    log.status = ActionStatus.COMPLETED
    log.save()
    logger.info(f"perform_check_in: Log status updated to {ActionStatus.COMPLETED} for log id {log_id}")

    logger.info(f"perform_check_in: Scheduling check out for log id {log_id}")
    log = Log.objects.create(user=User.objects.first(), action=ActionChoices.CHECK_OUT, status=ActionStatus.SCHEDULING)
    logger.info(f"perform_check_in: Log created for user {User.objects.first().name} with action {ActionChoices.CHECK_OUT} and status {ActionStatus.SCHEDULING} at {datetime.now()}")
    # Schedule perform_check_out 9 to 10 hours later
    try:
        logger.info(f"perform_check_in: Scheduling check out for log id {log_id}")
        hours_later = random.randint(9, 10)
        minutes_later = random.randint(0, 59)
        perform_check_out.apply_async(args=[log.id],
                                      eta=datetime.now() + timedelta(hours=hours_later, minutes=minutes_later))
        logger.info(f"perform_check_in: Check out scheduled for log id {log_id} at {datetime.now() + timedelta(hours=hours_later, minutes=minutes_later)}")
    except Exception as e:
        logger.error(f"perform_check_in: Exception occurred: {e} for log id {log_id}")
        log.status = ActionStatus.FAILED
        log.save()
        logger.info(f"perform_check_in: Log status updated to {ActionStatus.FAILED} for log id {log_id}")
        raise e
    logger.info(f"perform_check_in: Log status updated to {ActionStatus.SCHEDULED} for log id {log_id}")
    log.status = ActionStatus.SCHEDULED
    log.save()
    logger.info(f"perform_check_in: Log status updated to {ActionStatus.SCHEDULED} for log id {log_id}")


@shared_task
def toggle_break():
    # Your Selenium script to toggle break
    logger.info(f"toggle_break: Toggling break")
    log = Log.objects.create(user=User.objects.first(), action=ActionChoices.BREAK_IN, status=ActionStatus.IN_PROGRESS)
    try:
        user = User.objects.first()
        time.sleep(10)
        driver = login_to_portal(user.email, user.password)
        time.sleep(10)
        toggle_break(driver)
        time.sleep(10)
        driver.quit()
    except Exception as e:
        log.status = ActionStatus.FAILED
        log.save()
        raise e
    log.status = ActionStatus.COMPLETED
    log.save()


def schedule_check_in():
    logger.info(f"schedule_check_in: Scheduling check in at {datetime.now()}")
    log = Log.objects.create(user=User.objects.first(), action=ActionChoices.CHECK_IN, status=ActionStatus.SCHEDULING)
    now = datetime.now()
    # Calculate the next 2 PM
    next_2_pm = now.replace(hour=14, minute=0, second=0, microsecond=0)
    if now.hour >= 14:
        next_2_pm += timedelta(days=1)

    # Random time between 2 PM and 3 PM
    random_minutes = random.randint(0, 59)
    scheduled_time = next_2_pm + timedelta(minutes=random_minutes)

    # Schedule the task
    perform_check_in.apply_async(args=[log.id], eta=scheduled_time)
    logger.info(f"schedule_check_in: Check in scheduled at {scheduled_time}")
    logger.info(f"schedule_check_in: Log status updated to {ActionStatus.SCHEDULED}")
    log.status = ActionStatus.SCHEDULED
    log.save()
    logger.info(f"schedule_check_in: Log status updated to {ActionStatus.SCHEDULED}")


@shared_task
def daily_schedule_trigger():
    logger.info(f"daily_schedule_trigger: Triggering daily schedule at {datetime.now()}")
    schedule_check_in()
    logger.info(f"daily_schedule_trigger: Daily schedule triggered at {datetime.now()}")
