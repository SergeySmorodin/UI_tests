import random
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta

import factory
from faker import Faker

fake = Faker('ru_RU')


@dataclass
class ProjectData:
    code: str = ''
    code_project: str = ''
    start_date: str = ''
    stop_date: str = ''
    organisation: str = ''
    status: str = ''
    group: str = ''
    department: str = ''
    type_project: str = ''
    kind_project: str = ''
    note: str = ''

    def to_dict(self) -> dict:
        return asdict(self)

    def __repr__(self):
        return f"ProjectData(code={self.code})"


class ProjectFactory(factory.Factory):
    class Meta:
        model = ProjectData

    code = factory.LazyFunction(
        lambda: f"TEST_PROJ-{fake.unique.random_number(digits=6)}"
    )
    code_project = factory.LazyFunction(
        lambda: f"CODE-{fake.unique.random_number(digits=4)}"
    )
    start_date = factory.LazyFunction(
        lambda: datetime.now().strftime('%d.%m.%Y')
    )
    stop_date = factory.LazyFunction(
        lambda: (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%d.%m.%Y')
    )
    organisation = factory.LazyFunction(
        lambda: f"ООО {fake.company()} ({fake.random_number(digits=2)})"
    )
    note = factory.LazyFunction(
        lambda: fake.sentence(nb_words=10)
    )
