from core_code import Recommender

class result:
    def __init__(self):
        self.test = Recommender()

    def query(self, title):
        r1 = self.test.get_recom_con1(title)
        r2 = self.test.get_recom_con2(title)

        l1 = list(r1)
        l2 = list(r2)

        try:
            r3 = self.test.get_recom_colab(title)
            l3 = list(r3["Name"])
        except:
            l3 = None

        return (l1,l2,l3)

    def food(self):
        return self.test.unique_dishes()
