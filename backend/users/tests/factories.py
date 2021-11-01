import factory
from faker import Faker
from users.models import Subscriptions, User

fake = Faker(["ru-Ru"])


class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates User object.
    """

    class Meta:
        model = User
        django_get_or_create = ["username"]

    email = factory.LazyAttribute(lambda obj: f"{obj.username}@foodgram.ru")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(
        lambda n: "user_%d" % (User.objects.count())
    )
    password = "foodgram"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default ``_create`` with our custom call.
        The method has been taken from factory_boy manual. Without it
        password for users is being created without HASH and doesn't work
        right.
        """
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class SubscribeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscriptions
        django_get_or_create = ["user", "author"]

    @factory.lazy_attribute
    def author(self):
        return User.objects.order_by("?").first()

    @factory.lazy_attribute
    def user(self):
        subscriber = (
            User.objects.exclude(id=self.author.id).order_by("?").first()
        )
        return subscriber
