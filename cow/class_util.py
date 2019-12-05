def get_subclasses(cls):
    """returns all subclasses of argument, cls"""
    if issubclass(cls, type):
        subclasses = cls.__subclasses__(cls)
    else:
        subclasses = cls.__subclasses__()
    for subclass in subclasses:
        subclasses.extend(get_subclasses(subclass))
    return subclasses


if __name__ == '__main__':
    class A:
        pass


    class B(A):
        pass


    class C(A):
        pass


    class D(B):
        pass


    print(get_subclasses(A))
    print(get_subclasses(B))
