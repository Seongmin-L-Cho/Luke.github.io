# 상황1 다른 스토어가 들어오는 경우
# 개선점
# 1. store의 추상화
# 2. 외부에서 의존성을 주입하는 방법으로 코드 리팩토링

# 1. store의 책임을 정의, 캡슐화
# 2. user의 결제 로직의 수정
# 3. user도 캡슐화

# -> 1. store 도메인 기반 언어로 변경함
from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def __init__(self):
        self._money = 0;  # _ 는 private 라는 의미
        self.name = "";
        self._products = {};

    @abstractmethod
    def show_product(self, product_id):  # asis get_product(self)
        pass

    @abstractmethod
    def give_product(self, product_id):
        pass

    @abstractmethod
    def take_money(self, product_id):
        pass


# 일단 대충 한 캡슐화 -> 좀 더 정교한 캡슐화 진행

class GrabStore(Store):
    # 1번 특징 부터 추출한다 -> 돈? 가게를 다루네?
    def __init__(self, products):
        self._money = 0
        self.name = "그랩마켓"
        self._products = products  # 주입

    def set_money(self, money):
        self._money = money

    def set_products(self, products):
        self._products = products

    def show_product(self, product_id):
        return self._products[product_id]

    def give_product(self, products):
        self._products.pop(products)  # product_id를 key로 가지는 value 삭제

    def take_money(self, money):
        self._money += money


class User:
    def __init__(self, store: Store):  # 의존성을 주입. 보통 고수준 코드가 주입된다
        self.money = 0
        self.store = store
        self.belongs = []

    def get_money(self):
        return self.money

    def get_belongs(self, belongs):
        return self.belongs;

    def get_store(self):
        return self.store

    def see_product(self, product_id):
        product = self.store.show_product(product_id=product_id)  # 좀 더 간접 접근
        return product

    def purchase_product(self, product_id):
        product = self.see_product(product_id)
        if self.money >= product["price"]:
            # self.store.products.pop(product_id)  # 상점에서 상품 꺼내기
            self.store.give_product(product_id=product_id)  # 위의 비해 간접적으로 변했다. asis는 더 직접적으로 pop을 제어함
            self.money -= product["price"]  # 사용자가 돈 내기
            # self.store.money += product["price"]  # 상점에서 돈 받기
            self.store.take_money(product["price"])
            self.belongs.append(product)
            return product
        # 직접적으로 제어하지 않고 속성에서 제공해주는 메소드 사용. 결합도 낮아짐
        else:
            raise Exception("잔돈이 부족합니다")


if __name__ == "__main__":
    user = User(store=GrabStore())
    user.set_money(100000)
    user.purchase_product(product_id=1)
