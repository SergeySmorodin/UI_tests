import random
from dataclasses import dataclass, field, asdict
from typing import List

import factory
from faker import Faker

fake = Faker('ru_RU')


@dataclass
class ContractData:
    contract_number: str = ''
    contract_date: str = ''
    amount: str = ''
    status: str = ''
    company: str = ''
    manager: str = ''
    work_types: List[str] = field(default_factory=list)
    file_path: str = ''

    def to_dict(self) -> dict:
        return asdict(self)

    def __repr__(self):
        return f"ContractData(number={self.contract_number})"


class ContractFactory(factory.Factory):
    class Meta:
        model = ContractData

    contract_number = factory.LazyFunction(
        lambda: f"TEST_CONTRACT-{fake.unique.random_number(digits=6)}"
    )
    contract_date = factory.LazyFunction(
        lambda: fake.date_between(start_date='-30d', end_date='+30d').strftime('%Y-%m-%d')
    )
    amount = factory.LazyFunction(
        lambda: str(random.randint(10000, 10000000))
    )
    file_path = factory.LazyFunction(
        lambda: f"test_files/contract_{fake.unique.random_number(digits=6)}.pdf"
    )
