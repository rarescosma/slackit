"""Google Docs service."""
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, List, Tuple

from google.auth import load_credentials_from_file
from googleapiclient.discovery import build

from .. import Message, Service
from .._config import Config

SCOPES = ["https://www.googleapis.com/auth/documents"]
Indexes = Tuple[int, int]


@dataclass(frozen=True)
class Api:
    """Api abstraction."""

    service: Any
    doc_id: str

    def append_styled(
        self, text: str, style: str = "NORMAL_TEXT", add_break: bool = True
    ) -> Indexes:
        """Append a styled element."""
        _indexes = self._last_indexes()
        if not text:
            return _indexes

        start_index = _indexes[1] - 1
        start_index, end_index = self._update(
            [
                {
                    "insertText": {
                        "location": {
                            "index": start_index,
                        },
                        "text": text,
                    }
                }
            ]
        )
        requests = [
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": start_index,
                        "endIndex": end_index - 1,
                    },
                    "paragraphStyle": {
                        "namedStyleType": style,
                    },
                    "fields": "namedStyleType",
                }
            }
        ]
        if add_break:
            requests.append(
                {
                    "insertSectionBreak": {
                        "sectionType": "CONTINUOUS",
                        "location": {"index": end_index - 1},
                    }
                }
            )
        return self._update(requests)

    def append_list(self, paragraphs: List[str]) -> Indexes:
        """Append a list element."""
        start_index, end_index = self._last_indexes()[1] - 1, 0
        non_empty = [_ for _ in paragraphs if _]
        for paragraph in non_empty[:-1]:
            self.append_styled(paragraph)

        end_index = self.append_styled(non_empty[-1], add_break=False)[1] - 1

        self._update(
            [
                {
                    "createParagraphBullets": {
                        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                        "range": {
                            "startIndex": start_index,
                            "endIndex": end_index,
                        },
                    }
                }
            ]
        )
        indexes = self.append_styled("\n")
        return self._update(
            [
                {
                    "deleteParagraphBullets": {
                        "range": {
                            "startIndex": indexes[0],
                            "endIndex": indexes[1],
                        }
                    }
                }
            ]
        )

    def _last_indexes(self) -> Indexes:
        document = self._get()
        last_el = document["body"]["content"][-1]
        return last_el["startIndex"], last_el["endIndex"]

    def _get(self) -> dict:
        return self.service.documents().get(documentId=self.doc_id).execute()

    def _update(self, requests: List[dict]) -> Indexes:
        self.service.documents().batchUpdate(
            documentId=self.doc_id, body={"requests": requests}
        ).execute()
        return self._last_indexes()


class GdocService(Service):
    """Google Docs Service."""

    def send_many(self, messages: List[Message]) -> None:
        for message in messages:
            self.send_one(message)

    def send_one(self, message: Message) -> None:
        api = _get_api(doc_id=self._receiver_id)

        if message.style != "LIST":
            api.append_styled(message.text, style=message.style)
        else:
            api.append_list(paragraphs=list(message.items))


@lru_cache(maxsize=128)
def _get_api(doc_id: str) -> Api:
    creds_file = str(Config.get("gdocs_creds_json"))
    creds, _ = load_credentials_from_file(creds_file, SCOPES)
    return Api(service=build("docs", "v1", credentials=creds), doc_id=doc_id)
