from django.db.models import Q

from ai_assistant.models import KnowledgeDocument


class KnowledgeRetriever:
    STOP_WORDS = {
        "when",
        "what",
        "where",
        "who",
        "why",
        "how",
        "is",
        "are",
        "the",
        "a",
        "an",
        "of",
        "for",
        "to",
        "in",
        "on",
        "at",
        "does",
        "do",
    }

    def search(self, query):
        keywords = [
            word.lower().strip("?.!,")
            for word in query.split()
            if word.lower().strip("?.!,") not in self.STOP_WORDS
        ]

        if not keywords:
            return KnowledgeDocument.objects.filter(
                is_active=True
            )

        query_filter = Q()

        for keyword in keywords:
            query_filter |= (
                Q(title__icontains=keyword)
                | Q(content__icontains=keyword)
                | Q(source__icontains=keyword)
            )

        return KnowledgeDocument.objects.filter(
            query_filter,
            is_active=True,
        ).distinct()