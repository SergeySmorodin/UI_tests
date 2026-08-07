import random
from dataclasses import dataclass, field
from typing import List

import factory
from faker import Faker

fake = Faker('ru_RU')


@dataclass
class ContractData:
    """Датакласс для данных договора"""
    contract_number: str = ''
    contract_date: str = ''
    amount: str = ''
    status: str = ''
    company: str = ''
    manager: str = ''
    work_types: List[str] = field(default_factory=list)
    file_path: str = ''

    def to_dict(self) -> dict:
        return {
            'contract_number': self.contract_number,
            'contract_date': self.contract_date,
            'amount': self.amount,
            'status': self.status,
            'company': self.company,
            'manager': self.manager,
            'work_types': self.work_types,
            'file_path': self.file_path,
        }

    def __repr__(self):
        return f"ContractData(number={self.contract_number})"


class ContractFactory(factory.Factory):
    """Фабрика с ЗАГЛУШКАМИ — реальные значения будут взяты со страницы"""

    class Meta:
        model = ContractData

    contract_number = factory.LazyFunction(
        lambda: f"DOG-{fake.unique.random_number(digits=6)}"
    )

    contract_date = factory.LazyFunction(
        lambda: fake.date_between(start_date='-30d', end_date='+30d').strftime('%Y-%m-%d')
    )

    amount = factory.LazyFunction(
        lambda: f"{round(random.uniform(10000, 10000000), 2):,}".replace(',', ' ')
    )

    # Заглушки
    status = ''
    company = ''
    manager = ''
    work_types = factory.LazyFunction(lambda: [])
    file_path = ''

    @classmethod
    def with_real_data(cls, tdo_page):
        """
        Создать договор с данными из выпадающего списка

        Args:
            tdo_page: страница TdoPage с уже открытой формой
        """
        # Получаем реальные опции со страницы
        statuses = tdo_page.get_status_options()
        companies = tdo_page.get_company_options()

        # Выбираем случайные значения из реальных
        status = random.choice(statuses) if statuses else ''
        company = random.choice(companies) if companies else ''

        # Для менеджера — открываем список и берём первый доступный
        tdo_page.add_manager()
        managers = tdo_page._get_dropdown_options()
        manager = random.choice(managers) if managers else ''
        tdo_page.close_dropdown()

        # Виды работ
        tdo_page.add_work_type()
        work_types_list = tdo_page._get_dropdown_options()
        work_types = random.sample(work_types_list, min(2, len(work_types_list))) if work_types_list else []
        tdo_page.close_dropdown()

        return cls(
            status=status,
            company=company,
            manager=manager,
            work_types=work_types,
        )
