# django softdeletion

基于 django 的软删除插件

## 主要功能

- 支持软删除
- 支持级联软删除
- 软删除的数据不在 django admin 中显示

## 安装

```
pip install django-softdeletion
```

## 使用方法

```
from django.db import models
from django_softdeletion import SoftDeletionModelMixin


class CustomModel(SoftDeletionModelMixin, models.Model):
    ...

```
