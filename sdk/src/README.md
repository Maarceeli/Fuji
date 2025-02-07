# Fuji SDK

## Jak używać

Obecnie działa jedynie prometeusz (eduvulcan).

### Techniczny wstęp

Trzeba skorzystać z interfejsu np. `PrometheusInterface`. Dla każdego interfejsu podajemy dwa parametry:

- `auth_context` - są w nim dane logowania, sesje, certyfikaty (ogółem dane, które pozwalają dostać się do dziennika, **pamiętaj, by trzymać je w bezpiecznym miejscu**), 
- `student_context` - są w nim dane ucznia, pozwalające na wykonywanie zapytań do API, których używają interfejsy. (nie jest on konieczny, gdy logujesz się albo pobierasz uczniów)

Typy tych contextów są różne dla każdego dziennika. Jak uzyskać te contexty, dowiesz się niżej.

### Logowanie

#### Prometeusz (eduvulcan)

Musimy stworzyć instancję interfejsu `PrometheusInterface`, na początku musi on zawierać jedynie `auth_context`, który musi zawierać jedynie dane logowania do dziennika.

**UWAGA: Nie loguj się do dziennika od nowa za każdym razem, o tym jak zapisać zalogowane konto niżej.**

```py
from sdk.src.interfaces.prometheus.context import (
    PrometheusAuthContext,
    PrometheusWebCredentials,
)
from sdk.src.interfaces.prometheus.interface import PrometheusInterface

# Tworzymy interfejs prometeuszowy interfejs
interface = PrometheusInterface(
    # Auth context, o tym więcej niżej
    auth_context=PrometheusAuthContext(
        # Dane logowania
        prometheus_web_credentials=PrometheusWebCredentials(
            username="<nazwa użytkownika>", password="<hasło użytkownika>"
        )
    ),
    student_context=None,
)
```

Gdy stworzyliśmy już instancję interfejsu, trzeba się zalogować, jest to bardzo proste. ~~Szkoda tylko, że w środku interfejsu już nie.~~

```py
interface.login()
```

Reszta część będzie wspólna dla wszystkich dzienników.

### Zapisywanie zalogowanego konta

Po zalogowaniu trzeba by było zapisać te dane, bo logowanie za każdym razem od nowa jest czasochłonne.

```py
auth_context = interface.get_auth_context()
```

Później, jak będziesz tworzyć instancję interfejsu, to w parametrze `auth_context` daj właśnie to.

**Pamiętaj, by trzymać to w bezpiecznym miejscu!**

### Pobieranie i wybieranie uczniów

Jak jesteśmy zalogowani, to możemy pobrać uczniów, jest to bardzo proste. **UWAGA! Nie rób tego za każdym razem, tylko zapisz sobie gdzieś te dane.**

```py
students = interface.get_students()
```

Jak dokładnie wygląda to co zwraca `get_students()` możesz sprawdzić w kodzie, to co teraz istotne to to, że każdy uczeń ma w sobie pole `context`. Jak możesz się domyślać jest to pole, które będziemy dawać interfejsowi. Możemy to zrobić albo przy tworzeniu instancji interfejsu:

```py
interface = PrometheusInterface(
    auth_context=...,
    student_context=<tu_to_dajesz>,
)
```

albo, gdy mamy już stworzoną instancję interfejsu:

```py
interface.select_student(<tu_to_dajesz>)
```

### Co dalej?

No możesz pobrać na przykład oceny, możesz to zrobić (gdy jesteś zalogowany i masz wybranego ucznia) tak:

```py
grades = interface.get_grades(<numer semestru>)
```

## Jak dodawać funkcjonalności:

1. Zrób model(e) do danych, nie dawaj zbyt dużo danych, bo pamiętaj, że ma być to uniwersalny model dla wielu dzienników.
2. Zrób funkcje w odpowiednich api do pobierania tych danych.
3. Zrób mappery w modelach dla odpowiednich api.
4. Zrób funkcję we wszystkich interfejsach do pobierania tych danych, przy obsłudze api.

### Przykład dla sprawdzianów (tylko dla Prometeusza)

1 i 3. `sdk/src/models/exam.py`
```py
class ExamType(Enum):
    TEST = 0
    SHORT_TEST = 1
    CLASSWORK = 2
    OTHER = 3

    @staticmethod
    def from_hebe_type_name(type_name: str):
        match type_name:
            case "Sprawdzian":
                return ExamType.TEST
            case "Kartkówka":
                return ExamType.SHORT_TEST
            case "Praca klasowa":
                return ExamType.CLASSWORK
            case _:
                return ExamType.OTHER


@dataclass
class Exam:
    deadline: date
    subject: str
    type: ExamType
    description: str
    creator: str
    created_at: datetime

    @staticmethod
    def from_hebe_dict(data: dict):
        return Exam(
            deadline=datetime.fromtimestamp(data["Deadline"]["Timestamp"] / 1000),
            subject=data["Subject"]["Name"],
            type=ExamType.from_hebe_type_name(data["Type"]),
            description=data["Content"],
            creator=data["Creator"]["DisplayName"],
            created_at=datetime.fromtimestamp(data["DateCreated"]["Timestamp"] / 1000),
        )
```
2. `sdk/src/apis/hebe/client.py`
```py
def get_exams(self, student_id: int, from_: date, to: date):
        envelope = self._send_request(
            "GET",
            ENDPOINT_EXAM_BYPUPIL,
            params={
                "pupilId": student_id,
                "dateFrom": from_,
                "dateTo": to,
            },
        )
        return list(map(Exam.from_hebe_dict, envelope))
```

4. 

4.1. prometheus interface
```py
def get_exams(self, from_: date, to: date):
    self._check_is_auth_context_full()
    self._check_is_student_selected()
    return self._hebe_client.get_exams(self._student_context.student_id, from_, to)
```
4.2. core interface
```py
def get_exams(from_: date, to: date) -> list[Exam]:
    pass
```