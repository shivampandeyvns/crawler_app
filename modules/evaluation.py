import numpy as np


class IREvaluator:

    def precision(self, retrieved, relevant):

        if len(retrieved) == 0:
            return 0

        return len(set(retrieved) & set(relevant)) / len(retrieved)


    def recall(self, retrieved, relevant):

        if len(relevant) == 0:
            return 0

        return len(set(retrieved) & set(relevant)) / len(relevant)


    def f1(self, precision, recall):

        if precision + recall == 0:
            return 0

        return 2 * precision * recall / (precision + recall)


    def precision_at_k(self, retrieved, relevant, k):

        retrieved = retrieved[:k]

        if len(retrieved) == 0:
            return 0

        return len(set(retrieved) & set(relevant)) / len(retrieved)


    def recall_at_k(self, retrieved, relevant, k):

        retrieved = retrieved[:k]

        if len(relevant) == 0:
            return 0

        return len(set(retrieved) & set(relevant)) / len(relevant)


    def average_precision(self, retrieved, relevant):

        score = 0

        hits = 0

        for i, doc in enumerate(retrieved):

            if doc in relevant:

                hits += 1

                score += hits / (i + 1)

        if hits == 0:
            return 0

        return score / len(relevant)


    def reciprocal_rank(self, retrieved, relevant):

        for i, doc in enumerate(retrieved):

            if doc in relevant:

                return 1 / (i + 1)

        return 0


    def ndcg(self, retrieved, relevant):

        dcg = 0

        for i, doc in enumerate(retrieved):

            if doc in relevant:

                dcg += 1 / np.log2(i + 2)

        ideal = len(relevant)

        idcg = sum(
            1 / np.log2(i + 2)
            for i in range(ideal)
        )

        if idcg == 0:
            return 0

        return dcg / idcg