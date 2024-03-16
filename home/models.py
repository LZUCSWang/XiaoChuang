from django.db import models
from django.conf import settings


# from django.db import models
class category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class subcategory(models.Model):
    category = models.ForeignKey(
        category, on_delete=models.CASCADE, related_name="subcategories"
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("category", "name")

    def __str__(self):
        return f"{self.category.name} - {self.name}"

from django.db import models


class music(models.Model):
    #         src: "/static/boyfriend - Anson Seabra.mp3",
    #         poster: "/static/elena.jpg",
    #         name: "Boyfriend",
    #         artist: "Anson Seabra",
    #         lyric: "Lyrics here...",
    #         sublyric: "Translation here...",
    src = models.CharField(max_length=100)
    # poster = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="static/", verbose_name="图片路径")
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    lyric = models.TextField(blank=True)
    sublyric = models.TextField(blank=True)


class item(models.Model):
    CATEGORY_CHOICES = (
        ("科普", "科普"),
        ("问卷", "问卷"),
        ("方案", "方案"),
        # 添加更多分类...
    )

    SUBCATEGORY_CHOICES = (
        ("成瘾问题", "成瘾问题"),
        ("焦虑心理", "焦虑心理"),
        ("恋爱相关", "恋爱相关"),
        ("强迫症", "强迫症"),
        ("适应障碍", "适应障碍"),
        ("睡眠障碍", "睡眠障碍"),
        ("抑郁心理", "抑郁心理"),
        ("自我认知障碍", "自我认知障碍"),
    )

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, choices=SUBCATEGORY_CHOICES)
    name = models.CharField(max_length=100)  # 数据项的名称或标识
    description = models.TextField(blank=True)  # 数据项的详细描述

    def __str__(self):
        return f"{self.category} - {self.subcategory} - {self.name}"


# 定义日记天气选项
WEATHER_CHOICES = [
    ("晴朗", "晴朗"),
    ("多云", "多云"),
    ("阴", "阴"),
    ("小雨", "小雨"),
    ("雨", "雨"),
    ("暴雨", "暴雨"),
    ("雪", "雪"),
    ("雾", "雾"),
    ("龙卷风", "龙卷风"),
    ("雾霾", "雾霾"),
    ("沙尘暴", "沙尘暴"),
]

# 定义日记心情选项
MOOD_CHOICES = [
    ("happy", "开心"),
    ("sad", "伤心"),
    ("angry", "生气"),
    ("calm", "平静"),
]

# 定义日记背景选项
BACKGROUND_CHOICES = [
    ("默认", "默认"),
    ("奶茶", "奶茶"),
    ("猫猫", "猫猫"),
    ("龙龙", "龙龙"),
    ("吃饭", "吃饭"),
]


class diary(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True,null=True)
    weather = models.CharField(
        max_length=20, choices=WEATHER_CHOICES, blank=True, null=True
    )
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES, blank=True, null=True)
    background = models.CharField(
        max_length=100, choices=BACKGROUND_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.title


# class Post(models.Model):
class explore(models.Model):
    # thread = models.ForeignKey('self', related_name='thread_posts', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(
        "self", related_name="replies", on_delete=models.CASCADE, null=True, blank=True
    )
    author = models.CharField(max_length=100)
    post_time = models.DateTimeField()
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:  # 如果是新创建的帖子
            super().save(*args, **kwargs)  # 先保存以确保帖子有 ID
            # if not self.thread:  # 如果没有指定所属讨论主题
            #     self.thread = self  # 将自己设为所属讨论主题
            #     super().save(*args, **kwargs)  # 再次保存以更新 thread 字段
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author}: {self.content[:30]}"  # 返回作者和内容的前30个字符


class account(models.Model):
    username = models.CharField(max_length=200, verbose_name="用户名")
    password_md5 = models.CharField(max_length=200, verbose_name="密码(md5)")

    class Meta:
        db_table = "account"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.username}"


class datasets(models.Model):
    dataset_id = models.CharField(max_length=50, verbose_name="数据集ID")
    dataset_name = models.CharField(max_length=50, verbose_name="数据集名称")
    dataset_created_time = models.DateTimeField(verbose_name="数据集创建时间")
    dataset_updated_time = models.DateTimeField(verbose_name="数据集更新时间")
    account = models.ForeignKey(
        account, on_delete=models.CASCADE, verbose_name="用户"
    )  # 一对多

    class Meta:
        db_table = "datasets"
        verbose_name = "数据集"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.dataset_name}"


class dataset(models.Model):
    data_id = models.CharField(max_length=50, verbose_name="图片ID")
    data_name = models.CharField(max_length=50, verbose_name="图片名称")
    data_created_time = models.DateTimeField(verbose_name="图片创建时间")
    data_class = models.CharField(max_length=50, verbose_name="图片类别")
    data_path = models.ImageField(
        upload_to="static/data/pictures", verbose_name="图片路径"
    )
    dataset = models.ForeignKey(
        datasets, on_delete=models.CASCADE, verbose_name="数据集"
    )  # 一对多
    account = models.ForeignKey(
        account, on_delete=models.CASCADE, verbose_name="用户"
    )  # 一对多

    class Meta:
        db_table = "dataset"
        verbose_name = "数据"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.data_name}"
