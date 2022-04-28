# 상황1 다른 스토어가 들어오는 경우
# 개선점
# 1. store의 추상화
# 2. 외부에서 의존성을 주입하는 방법으로 코드 리팩토링

# 1. store의 책임을 정의, 캡슐화
# 2. user의 결제 로직의 수정
# 3. user도 캡슐화

# -> 1. store 도메인 기반 언어로 변경함

# 3.번 유저가 너무 많은 행위를 책임지고 있다. Store가 판매책임을 가져야하는거 아닌가
# 개선점
# 1. 상점에서 상품을 판매하는 행위를 추상화하고 구체적인 로직을 해당 메서드로 옮긴다.


# 4번 .프로덕트가 책임이 필요할거 같은데
# 개선점
# 1. 딕셔너리 타입을 클래스(데이터클래스) 객체로 변환하자
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int


class Store(ABC):
    @abstractmethod
    def __init__(self):
        self._money = 0;  # _ 는 private 라는 의미
        self.name = "";
        self._products = {};

    @abstractmethod
    def show_product(self, product_id):  # asis get_product(self)
        pass

    # @abstractmethod
    # def give_product(self, product_id):
    #     pass
    #
    # @abstractmethod
    # def take_money(self, product_id):
    #     pass

    def sell_product(self, product_id, money):
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

    def sell_product(self, product_id, money):
        # validation 코드는 일단 최소화
        product = self.show_product(product_id=product_id)
        if not product:
            raise Exception("상품이 존재하지 않는다")

        self._take_money(money=money)
        try:
            _product = self._take_out_product(product_id=product_id)
        except Exception as e:
            self._return_money(money)
            return _product
            raise e

    def _return_money(self, money):
         self._money -= money

    def _take_out_product(self, product_id):
        return self._products.pop(product_id)

    def take_money(self, money):
        self._money += money


class User:
    def __init__(self, store: Store):  # 의존성을 주입. 보통 고수준 코드가 주입된다
        self._money = 0
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

    # asis -> 상품 판매 등등이 전부 user에서 이루어지고 있음
    def purchase_product(self, product_id):
        product = self.see_product(product_id)
        price = product.price
        if self._check_money_enough(price=price) # asis 대비 if에 대해 좀 더 추상화 + 가독성이 좋아진다
            # self.store.products.pop(product_id)  # 상점에서 상품 꺼내기
            # self.store.give_product(product_id=product_id)  # 위의 비해 간접적으로 변했다. asis는 더 직접적으로 pop을 제어함
            self.money -= product["price"]  # 사용자가 돈 내기
            # self.store.money += product["price"]  # 상점에서 돈 받기
            # self.store.take_money(product["price"]) ->  3. 유저 비중 줄이기 위해 삭제
            try:
                my_product = self.store.sell_product(product_id=product_id, money=price)
                self.belongs.append(product)
                return my_product
            except Exception as e:
                self._take_money(money=price)
                print("구매중 문제 발생")

            return product
        # 직접적으로 제어하지 않고 속성에서 제공해주는 메소드 사용. 결합도 낮아짐
        else:
            raise Exception("잔돈이 부족합니다")

    def _check_money_enough(self,price):
        return self._money >= price

    def _give_money(self, money):
        self._money -= money

    def _take_money(self, money):
        self._money += money

    def _add_belong(self, product):
        self.belongs.append(product)

if __name__ == "__main__":
    store =GrabStore(products={1:Product(name="키보드", price=30000),
                               2:Product(name="키보드", price=30000)})

    user = User(money=10000,store=store)
    user.purchase_product(product_id=1)
