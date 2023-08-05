# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_django']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.2,<4.0.0', 'strawberry-graphql>=0.39.1,<0.40.0']

setup_kwargs = {
    'name': 'strawberry-graphql-django',
    'version': '0.0.2',
    'description': 'Strawberry GraphQL Django extension',
    'long_description': '# Strawberry GraphQL Django extension\n\nThis library provides helpers to generate fields, mutations and resolvers from you Django models.\n\nmodels.py:\n```python\nfrom django.db import models\n\nclass User(models.Model):\n    name = models.CharField(max_length=50)\n    age = models.IntegerField()\n    groups = models.ManyToManyField(\'Group\', related_name=\'users\')\n\nclass Group(models.Model):\n    name = models.CharField(max_length=50)\n```\n\nschema.py:\n```python\nimport strawberry\nfrom strawberry_django import ModelResolver\nfrom .models import User, Group\n\nclass UserResolver(ModelResolver):\n    model = User\n\nclass GroupResolver(ModelResolver):\n    model = Group\n\n@strawberry.type\nclass Query(UserResolver.query(), GroupResolver.query()):\n    pass\n\n@strawberry.type\nclass Mutation(UserResolver.mutation(), GroupResolver.mutation()):\n    pass\n\nschema = strawberry.Schema(query=Query, mutation=Mutation)\n```\n\nurls.py:\n```python\nfrom strawberry.django.views import GraphQLView\nfrom .schema import schema\n\nurlpatterns = [\n    path(\'graphql\', GraphQLView.as_view(schema=schema)),\n]\n```\n\nCreate database and start server\n```shell\nmanage.py runserver\n```\n\nOpen http://localhost:8000/graphql and start testing.\nCreate user and make first query\n```\nmutation {\n  createUser(data: {name: "hello", age: 20} ) {\n    id\n  }\n}\n```\n```\nquery {\n  user(id: 1) {\n    name\n    age\n  }\n  users(filter: ["name__contains=my"]) {\n    id\n    name\n  }\n}\n```\n',
    'author': 'Lauri Hintsala',
    'author_email': 'lauri.hintsala@verkkopaja.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/la4de/strawberry-graphql-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
