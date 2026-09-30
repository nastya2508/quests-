
#Документообіг ч.1

from abc import ABC, abstractmethod


class Document(ABC):

    @abstractmethod
    def render(self) -> str:
        pass


class Report(Document):

    def render(self) -> str:
        return "Звіт: Аналітика продажів за місяць сформована."


class Invoice(Document):

    def render(self) -> str:
        return "Рахунок: Сума до сплати — 2500 грн."


class Contract(Document):

    def render(self) -> str:
        return "Контракт: Договір підписано двома сторонами."


class NullDocument(Document):

    def render(self) -> str:
        return "Помилка: Невідомий тип документа!"


class DocumentFactory:

    @staticmethod
    def create(doc_type: str) -> Document:
        documents = {
            "report": Report,
            "invoice": Invoice,
            "contract": Contract,
        }

        doc_class = documents.get(doc_type.lower(), NullDocument)
        return doc_class()


if __name__ == "__main__":
    requested_docs = ["report", "invoice", "contract", "unknown_type"]

    for doc_type in requested_docs:
        doc = DocumentFactory.create(doc_type)
        print(doc.render())