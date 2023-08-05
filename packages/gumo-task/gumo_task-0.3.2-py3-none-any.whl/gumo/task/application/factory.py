import datetime
from typing import Optional

from gumo.datastore import EntityKey
from gumo.datastore import EntityKeyFactory

from gumo.task.domain import GumoTask
from gumo.task.domain import TaskAppEngineRouting


class GumoTaskFactory:
    def build(
            self,
            key: EntityKey,
            relative_uri: str,
            method: str = 'POST',
            payload: Optional[dict] = None,
            headers: Optional[dict] = None,
            schedule_time: Optional[datetime.date] = None,
            in_seconds: Optional[int] = None,
            created_at: Optional[datetime.datetime] = None,
            queue_name: Optional[str] = None,
            service: Optional[str] = None,
            version: Optional[str] = None,
            instance: Optional[str] = None,
    ) -> GumoTask:
        now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

        if schedule_time is not None and in_seconds is not None:
            raise ValueError('schedule_time and in_seconds should be specified exclusively.')

        if in_seconds:
            delta = datetime.timedelta(seconds=in_seconds)
            schedule_time = now + delta

        if schedule_time is None:
            schedule_time = now

        return GumoTask(
            key=key,
            relative_uri=relative_uri,
            method=method,
            payload=payload,
            headers=headers,
            schedule_time=schedule_time,
            created_at=created_at if created_at else now,
            queue_name=queue_name,
            app_engine_routing=TaskAppEngineRouting(
                service=service,
                version=version,
                instance=instance,
            )
        )

    def build_for_new(
            self,
            relative_uri: str,
            method: str = 'POST',
            payload: Optional[dict] = None,
            headers: Optional[dict] = None,
            schedule_time: Optional[datetime.date] = None,
            in_seconds: Optional[int] = None,
            created_at: Optional[datetime.datetime] = None,
            queue_name: Optional[str] = None,
            service: Optional[str] = None,
            version: Optional[str] = None,
            instance: Optional[str] = None,
    ) -> GumoTask:

        return self.build(
            key=EntityKeyFactory().build_for_new(kind=GumoTask.KIND),
            relative_uri=relative_uri,
            method=method,
            payload=payload,
            headers=headers,
            schedule_time=schedule_time,
            in_seconds=in_seconds,
            created_at=created_at,
            queue_name=queue_name,
            service=service,
            version=version,
            instance=instance,
        )
