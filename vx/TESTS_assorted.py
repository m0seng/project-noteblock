class Something:
    ...

class SomethingElse:
    ...

def old_main():
    some_list = [Something() for _ in range(5)]
    # print(some_list)

    second_list = []
    for index, item in enumerate(some_list):
        another_item = SomethingElse()
        another_item.attribute = item
        another_item.method = lambda: print(item)
        second_list.append(another_item)

    for item in second_list:
        item.method()

def main():
    my_dict = {
        Something: 1,
        SomethingElse: 2
    }

    print(my_dict[SomethingElse])

if __name__ == "__main__":
    main()